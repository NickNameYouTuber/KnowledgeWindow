from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from app.config.database import VectorizedKnowledgeBase

model = SentenceTransformer('all-MiniLM-L6-v2')

def text_to_vector(text):
    return model.encode(text).tolist()
