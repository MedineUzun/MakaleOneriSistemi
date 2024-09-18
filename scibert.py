import torch
from transformers import AutoTokenizer, AutoModel
from flask import session
from scipy.spatial.distance import cosine
import numpy as np

class SciBERTRecommender:
   
    def __init__(self, clientt):
        self.tokenizer = AutoTokenizer.from_pretrained('allenai/scibert_scivocab_uncased')
        self.model = AutoModel.from_pretrained('allenai/scibert_scivocab_uncased')
        self.client = clientt
        self.db = clientt.db

    def get_embedding(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state
        embeddings = torch.mean(embeddings, dim=1).squeeze()
        return embeddings.numpy()

    def calculate_similarity(self):
    
        words = session.get('interests')
        interest_words = words.split()
        print(interest_words)
        if not interest_words:
          return []

    
        user_embeddings = [self.get_embedding(word) for word in interest_words]
        user_embedding = np.mean(user_embeddings, axis=0) if user_embeddings else None
       
        if user_embedding is None:
           return []

        similarity_scores = []

        articles = self.db.makaleicerik.find()
        
        for article in articles:
          article_text = ' '.join(article.get('cleaned_text', []))
          article_keys = article.get('keys')
          if article_text:
            article_embedding = self.get_embedding(article_text)
            similarity = 1 - cosine(user_embedding, article_embedding)
            
            similarity_scores.append((article['original_text'], similarity,article_keys))
        top_articles = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[:5]

        return top_articles 
    

    def calculate_similarity2(self):
   
        words = session.get('interests2')
        interest_words = words.split()
        print(interest_words)
        if not interest_words:
            return []

   
        user_embeddings = [self.get_embedding(word) for word in interest_words]
        user_embedding = np.mean(user_embeddings, axis=0) if user_embeddings else None
        print("kullanıcı embedding: " , user_embedding.shape)
        if user_embedding is None:
         return []

        similarity_scores = []

        articles = self.db.makaleicerik.find()
        
        for article in articles:
          article_text = ' '.join(article.get('cleaned_text', []))
          article_keys = article.get('keys')
          if article_text:
            article_embedding = self.get_embedding(article_text)
            similarity = 1 - cosine(user_embedding, article_embedding)
            
            similarity_scores.append((article['original_text'], similarity,article_keys))
        top_articles = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[:5]

        return top_articles 
    
    

    def calculate_similarity3(self,query):

        words = query.split()
        interest_words = words.split()
        print(interest_words)
        if not interest_words:
          return []

        user_embeddings = [self.get_embedding(word) for word in interest_words]
        user_embedding = np.mean(user_embeddings, axis=0) if user_embeddings else None
        if user_embedding is None:
         return []

        similarity_scores = []

        articles = self.db.makaleicerik.find()
        
        for article in articles:
          article_text = ' '.join(article.get('cleaned_text', []))
          article_keys = article.get('keys')
          if article_text:
            article_embedding = self.get_embedding(article_text)
            similarity = 1 - cosine(user_embedding, article_embedding)
            
            similarity_scores.append((article['original_text'], similarity,article_keys))
        top_articles = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[:5]

        return top_articles