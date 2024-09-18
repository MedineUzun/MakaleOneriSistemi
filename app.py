from flask import Flask, jsonify, render_template, request, redirect, url_for, flash, session
from mongo import Client
from nlp import DocumentProcessor
from fastText import FastTextRecommender
from scibert import SciBERTRecommender
app = Flask(__name__)

app.secret_key = '1289euhfhfhdjlshfhusehfsuowehdaouwehdawşuefgawegufhq7632973498q'
mongo = Client("mongodb+srv://admin:1234@cluster0.bulzlww.mongodb.net/akademikmakale")


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process',methods=['GET','POST'])
def process_and_store_articles():
    
    doc_processor = DocumentProcessor(mongo)
    doc_processor.process_documents()
    doc_processor.document_keys()
    return jsonify({'message': 'All documents processed and stored successfully.'})



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = mongo.users_collection.find_one({'email': email})
        if user and user['password'] == password:
            session['email'] = email
            session['password'] = password
            session['user_id'] = str(user['_id'])
            session['interests'] = user.get('interests', [])
            session['interests2'] = user.get('interests2', [])  
            return redirect(url_for('anasayfa'))
        else:
            
            flash('Giriş bilgileri hatalı. Lütfen tekrar deneyiniz.')

    return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        interests = request.form['interests']

        user_data = {
            'username': username,
            'email': email,
            'password': password,
            'interests': interests
        }
        mongo.users_collection.insert_one(user_data)
        return redirect(url_for('anasayfa'))
    return render_template('signup.html')


@app.route('/anasayfa')
def anasayfa():
    return render_template('anasayfa.html')


@app.route('/pdfoner')
def pdfoner_view():
  recommender1 = FastTextRecommender(mongo)
  top_articles1 = recommender1.calculate_recommendations()
  recommender2 = SciBERTRecommender(mongo)
  top_articles2 = recommender2.calculate_similarity()
  return render_template('pdfoner.html', top_articles1=top_articles1, top_articles2=top_articles2)
  

@app.route('/pdfoner2')
def pdfoner2_view():
  recommender3 = FastTextRecommender(mongo)
  top_articles3 = recommender3.calculate_recommendations2()
  recommender4 = SciBERTRecommender(mongo)
  top_articles4 = recommender4.calculate_similarity2()
  return render_template('pdfoner2.html', top_articles3=top_articles3,top_articles4=top_articles4 )
  
@app.route('/pdfoner3')
def pdfoner3_view():
  
  
  return render_template('pdfoner3.html')
  

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
       search_term = request.form.get('search')  
       email = session.get('email') 
    
       if email and search_term:
            recommendations3 = FastTextRecommender(mongo)
            top_articles3 = recommendations3.calculate_recommendations3(search_term)
            recommendations4 = SciBERTRecommender(mongo)
            top_articles4 = recommendations4.calculate_similarity3(search_term)
            mongo.users_collection.update_one(
                {'email': email},
                {'$addToSet': {'interests3': search_term}}
            )
            return render_template('pdfoner3.html',top_articles3=top_articles3, top_articles4=top_articles4)
    return render_template('search.html')

   


@app.route('/save_selected_articles', methods=['POST'])
def save_selected_articles():

    email = session.get('email')
    
    selected_articles = []
    article_keys = []


    for key in request.form:
        if key.startswith('selected_articles_'):
            idx = key.split('_')[-1]  
            if request.form[key]: 
                selected_articles.append(request.form[key])
                article_keys.append(request.form.get('article_keys_' + idx, ''))

   
    if selected_articles:
        update_result = mongo.users_collection.update_one(
            {'email': email}, 
            {'$addToSet': {'saved_articles': {'$each': selected_articles}, 'interests2': {'$each': article_keys}}}
        )
    if update_result.modified_count == 0:
        flash('Seçilen makaleler zaten kaydedilmiş veya bir hata oluştu.')
    else:
        flash('Makaleler başarıyla kaydedildi.')

    return redirect(url_for('hesap_view'))

   

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password= request.form['password']
        age = request.form['age']
        age = int(age) if age.isdigit() else None 
        gender = request.form['gender']
        interests = request.form['interests']

        print("Updating user:", email) 
        user = mongo.find_user(email)
        print("Found user:", user)  
        if not user:
            print("No user found with the email:", email)
            return "No user found with the provided email!", 404

        
        result = mongo.users_collection.update_one(
            {'email': email},
            {'$set': {
                'username': username,
                'password': password,
                'age': age,
                'gender': gender,
                'interests': interests
            }}
        )
        print("Update result:", result.modified_count) 
        return redirect(url_for('profile'))
    return render_template('profile.html')


@app.route('/hesap')
def hesap_view():
    recommender = FastTextRecommender(mongo)
    recommender.calculate_recommendations()  
    precision_value = recommender.calculate_precision()  
    return render_template('precision.html', precision_value=precision_value)




if __name__ == '__main__':
    app.run(port=8000, debug=True)