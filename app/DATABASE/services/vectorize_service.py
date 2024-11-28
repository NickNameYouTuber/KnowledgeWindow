from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')

def text_to_vector(text):
    return model.encode(text).tolist()
