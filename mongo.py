from pymongo import MongoClient

class Client:
    def __init__(self, uri):

        self.client = MongoClient(uri)
        self.db = self.client.yazlab2_3
        self.users_collection = self.db.kullanicilar
        self.articles_collection = self.db.makaleicerik

    def find_user(self, email):
        return self.db.kullanicilar.find_one({"email": email})

    def add_user(self, user_data):
        return self.db.kullanicilar.insert_one(user_data).inserted_id

    def get_articles(self):
        return self.db.makaleicerik.find()

    def add_article(self, article_data):
        return self.db.makaleicerik.insert_one(article_data).inserted_id

    def close(self):
        self.client.close()
