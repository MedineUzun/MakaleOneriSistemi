import fasttext
from flask import session
import numpy as np 
from scipy.spatial.distance import cosine

class FastTextRecommender:

  def __init__(self, clientt):
        
        model_path = 'C:\\Users\\user\\Desktop\\crawl-300d-2M-subword\\crawl-300d-2M-subword.bin'
        self.model = fasttext.load_model(model_path)
        self.client = clientt
        self.db = clientt.db
        self.top_articles = []

  def calculate_recommendations(self):
        
        words = session.get('interests')
        interest_words = words.split()
        if not interest_words:
            return []
        
        print(interest_words)
        recommended_articles = []
        interest_embeddings = []

        
        for word in interest_words:
            embedding = self.model.get_word_vector(word)
            if np.linalg.norm(embedding) != 0:  
                interest_embeddings.append(embedding)
            
        
        if interest_embeddings:
            user_embedding = np.mean(interest_embeddings, axis=0)
           
        else:
            return []

        articles = self.db.makaleicerik.find()
        
        
        for article in articles:
            article_text = ' '.join(article.get('cleaned_text', []))
            article_vector = self.model.get_sentence_vector(article_text)
            if np.linalg.norm(article_vector) != 0:
                similarity = 1 - cosine(user_embedding, article_vector)
                article_keys = article.get('keys', '')
                recommended_articles.append((article['original_text'], similarity, article_keys))

       
        recommended_articles.sort(key=lambda x: x[1], reverse=True)
        self.top_articles = recommended_articles[:5]

        return self.top_articles
    
  def calculate_recommendations2(self):

        interest_words = session.get('interests2')
        if not interest_words:
            return []
        
        print(interest_words)
        recommended_articles = []
        interest_embeddings = []

        for word in interest_words:
            embedding = self.model.get_word_vector(word)
            if np.linalg.norm(embedding) != 0: 
                interest_embeddings.append(embedding)

        if interest_embeddings:
            user_embedding = np.mean(interest_embeddings, axis=0)
        else:
            return []

        articles = self.db.makaleicerik.find()
        
        for article in articles:
            article_text = ' '.join(article.get('cleaned_text', []))
            article_vector = self.model.get_sentence_vector(article_text)
            if np.linalg.norm(article_vector) != 0:
                similarity = 1 - cosine(user_embedding, article_vector)
                article_keys = article.get('keys', '')
                recommended_articles.append((article['original_text'], similarity, article_keys))

        recommended_articles.sort(key=lambda x: x[1], reverse=True)
        #top_articles = recommended_articles[:5]

        #return top_articles
        self.top_articles = recommended_articles[:5]  
        return self.top_articles 
  
  def calculate_recommendations3(self,query):
    words = query.split()
   
    interest_embeddings = []

       
    for word in words:
        embedding = self.model.get_word_vector(word)
        if np.linalg.norm(embedding) != 0:  
           interest_embeddings.append(embedding)

       
    if not interest_embeddings:
        return []
    user_embedding = np.mean(interest_embeddings, axis=0)

    recommended_articles = []
    articles = self.db.makaleicerik.find()

        
    for article in articles:
        article_text = ' '.join(article.get('cleaned_text', []))
        article_vector = self.model.get_sentence_vector(article_text)
        if np.linalg.norm(article_vector) != 0:
            similarity = 1 - cosine(user_embedding, article_vector)
            article_keys = article.get('keys', '')
            recommended_articles.append((article['original_text'], similarity, article_keys))

        
    recommended_articles.sort(key=lambda x: x[1], reverse=True)
    top_articles = recommended_articles[:5]
    return top_articles
  
  def calculate_precision(self):
    interest_words = session.get('interests')
    user_interests_set = set(interest_words.split())
    recommended_keys = set()

   

    for article_text, similarity, article_keys in self.top_articles:
        recommended_keys.update(article_keys.split())

    true_positives = len(user_interests_set & recommended_keys)
    false_positives = len(recommended_keys - user_interests_set)

    #print("True Positives:", true_positives)
    #print("False Positives:", false_positives)

    if true_positives + false_positives == 0:
        print("No matches found, returning zero precision.")
        return 0

    precision = true_positives / (true_positives + false_positives)
    return precision