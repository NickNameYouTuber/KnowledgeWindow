import os

import PyPDF2
import openpyxl
from flask import jsonify
from keras.src.losses import cosine_similarity
from werkzeug.utils import secure_filename

from app.DATABASE.config.database import VectorizedKnowledgeBase
from app.DATABASE.services.llm_service import search_together
from app.DATABASE.services.vectorize_service import text_to_vector
import tensorflow as tf


def upload_txt_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".txt"):
        file_content = file.read().decode('utf-8')
        vector = text_to_vector(file_content)  # Преобразуем контент в вектор
        new_entry = VectorizedKnowledgeBase(title=file.filename, content=file_content, vector=vector)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "File processed and vectorized successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .txt files are allowed."}), 400

def upload_csv_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".csv"):
        file_content = file.read().decode('utf-8')
        vector = text_to_vector(file_content)  # Преобразуем контент в вектор
        new_entry = VectorizedKnowledgeBase(title=file.filename, content=file_content, vector=vector)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "File processed and vectorized successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .csv files are allowed."}), 400

def upload_docx_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".docx"):
        file_content = file.read().decode('utf-8')
        vector = text_to_vector(file_content)  # Преобразуем контент в вектор
        new_entry = VectorizedKnowledgeBase(title=file.filename, content=file_content, vector=vector)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "File processed and vectorized successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .docx files are allowed."}), 400

def upload_xlsx_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".xlsx"):
        # Сохраняем файл во временное место
        temp_file_path = secure_filename(file.filename)
        file.save(temp_file_path)

        # Открываем файл с помощью openpyxl
        wb = openpyxl.load_workbook(temp_file_path)
        sheet = wb.active
        content = "\n".join([f"{cell.value}" for row in sheet.iter_rows() for cell in row])

        # Удаляем временный файл
        os.remove(temp_file_path)

        # Преобразуем контент в вектор
        vector = text_to_vector(content)
        new_entry = VectorizedKnowledgeBase(title=file.filename, content=content, vector=vector)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "File processed and vectorized successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .xlsx files are allowed."}), 400

def upload_pdf_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".pdf"):
        # Сохраняем файл во временное место
        temp_file_path = secure_filename(file.filename)
        file.save(temp_file_path)

        # Извлекаем текст из PDF-файла
        pdf_reader = PyPDF2.PdfReader(temp_file_path)
        content = "\n".join([pdf_reader.pages[i].extract_text() for i in range(len(pdf_reader.pages))])

        # Удаляем временный файл
        os.remove(temp_file_path)

        # Преобразуем контент в вектор
        vector = text_to_vector(content)
        new_entry = VectorizedKnowledgeBase(title=file.filename, content=content, vector=vector)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "File processed and vectorized successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .pdf files are allowed."}), 400

def upload_md_file(request, db):
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename.endswith(".md"):
        file_content = file.read().decode('utf-8')
        vector = text_to_vector(file_content)  # Преобразуем контент в вектор
        new_entry = VectorizedKnowledgeBase(title=file.filename, content=file_content, vector=vector)
        db.session.add(new_entry)
        db.session.commit()
        return jsonify({"message": "File processed and vectorized successfully"})
    else:
        return jsonify({"error": "Invalid file type. Only .md files are allowed."}), 400


import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

def convert_to_numpy_array(vector):
    """
    Safely convert various vector formats to numpy array with proper shape.
    Ensures the output is a 2D array compatible with cosine similarity.
    """
    try:
        # Convert TensorFlow tensors or lists to NumPy arrays
        if isinstance(vector, list) or isinstance(vector, (np.ndarray, tf.Tensor)):
            vector = np.array(vector, dtype=np.float32)

        # Wrap scalars into a 2D array
        if np.isscalar(vector):
            vector = np.array([[vector]], dtype=np.float32)

        # Ensure the vector is 2D
        if len(vector.shape) == 1:
            vector = vector.reshape(1, -1)

        return vector
    except Exception as e:
        print(f"Error converting vector: {e}")
        return np.zeros((1, 384), dtype=np.float32)  # Adjust to match your vector dimension.

def calculate_similarity(vec1, vec2):
    """
    Calculate cosine similarity between two vectors.
    """
    try:
        # Convert inputs to 2D NumPy arrays
        vec1_np = convert_to_numpy_array(vec1)
        vec2_np = convert_to_numpy_array(vec2)

        # Debugging information
        print(f"Vec1 shape: {vec1_np.shape}")
        print(f"Vec2 shape: {vec2_np.shape}")

        # Validate dimensions match
        if vec1_np.shape[1] != vec2_np.shape[1]:
            print(f"Dimension mismatch: {vec1_np.shape[1]} vs {vec2_np.shape[1]}")
            return 0.0

        # Compute cosine similarity
        similarity = cosine_similarity(vec1_np, vec2_np)[0][0]
        return float(similarity)
    except Exception as e:
        print(f"Error calculating similarity: {e}")
        return 0.0



def find_relevant_files(query_vector, db):
    """
    Find relevant files using vector similarity
    """
    try:
        all_vectors = VectorizedKnowledgeBase.query.all()
        similarities = []

        # Convert query vector once
        query_vector_np = convert_to_numpy_array(query_vector)
        print(f"Query vector shape: {query_vector_np.shape}")

        for entry in all_vectors:
            try:
                if entry.vector is None:
                    continue

                # Print debug info for database vector
                print(f"Processing entry {entry.id}")
                print(f"Entry vector type: {type(entry.vector)}")
                if hasattr(entry.vector, 'shape'):
                    print(f"Entry vector shape: {entry.vector.shape}")

                similarity = calculate_similarity(query_vector_np, entry.vector)
                similarities.append((entry, similarity))
            except Exception as e:
                print(f"Error processing entry {entry.id}: {str(e)}")
                continue

        # Sort by similarity score in descending order
        similarities.sort(key=lambda x: x[1], reverse=True)

        # Return top 3 most similar entries
        return [entry for entry, _ in similarities[:3]]
    except Exception as e:
        print(f"Error in find_relevant_files: {str(e)}")
        raise


def search_knowledge_base(query, template, db):
    """
    Search the knowledge base using vector similarity
    """
    try:
        # Get query vector
        query_vector = text_to_vector(query)
        if query_vector is None:
            raise ValueError("Failed to vectorize query")

        print("Query vector type:", type(query_vector))
        if hasattr(query_vector, 'shape'):
            print("Query vector shape:", query_vector.shape)

        # Find relevant files
        relevant_files = find_relevant_files(query_vector, db)
        if not relevant_files:
            return {"response": "No relevant documents found"}

        # Prepare data for together API
        data = {str(entry.id): {"title": entry.title, "content": entry.content}
                for entry in relevant_files}

        # Process query using Together API
        together_response = search_together(query, data, template)

        return {"response": together_response}
    except Exception as e:
        print(f"Error in search_knowledge_base: {str(e)}")
        raise