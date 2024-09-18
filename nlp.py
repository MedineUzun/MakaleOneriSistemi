import os
from flask import jsonify
import spacy
import string

nlp = spacy.load("en_core_web_sm") 
punctuations = string.punctuation

class DocumentProcessor:
    def _init_(self, clientt):
        #self.db = db  # MongoDB bağlantısı
        self.client = clientt
        self.db = clientt.db

    def process_documents(self):
        directory_path = 'C:\\Users\\user\\Desktop\\Inspec\\Inspec\\docsutf8'
        for filename in os.listdir(directory_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory_path, filename)
                with open(file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                doc = nlp(text)
                cleaned_tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha and len(token.text) > 1]

                document = {
                    'original_text': text,
                    'cleaned_text': cleaned_tokens,
                    'file_name': filename
                }
                result = self.db.makaleicerik.insert_one(document)
                print(f"Processed {filename}: ID {result.inserted_id}")
                return {'message': 'All documents processed and stored successfully.'}

    

    def document_keys(self):
        key_directory_path = 'C:\\Users\\user\\Desktop\\Inspec\\Inspec\\keys' 

            
        documents = self.db.makaleicerik.find()
        for document in documents:
            text_filename = document['file_name']
            base_name = text_filename.split('.txt')[0]  
            key_filename = f"{base_name}.key"  
            print(key_filename)
            key_file_path = os.path.join(key_directory_path, key_filename)

            if os.path.exists(key_file_path): 
                with open(key_file_path, 'r', encoding='utf-8') as key_file:
                   keys = key_file.read()  

            
                self.db.makaleicerik.update_one(
                    {'_id': document['_id']},
                    {'$set': {'keys': keys}}
                )
                print(f"Updated document {text_filename} with keys.")
            else:
                print(f"No key file found for {text_filename}.")