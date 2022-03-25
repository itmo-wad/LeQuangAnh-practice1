from flask import Flask, render_template ,redirect, url_for, request, make_response,flash,url_for,send_from_directory
from pymongo import MongoClient
from werkzeug.utils import secure_filename
import os 

UPLOAD_FOLDER = './upload'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app=Flask(__name__)
app.config['SECRET_KEY'] = "ngacnhienchua"
client = MongoClient("mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&directConnection=true&ssl=false")
db = client['web_course']
collection = db['practice']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/')
def profile():
    return render_template('profile.html')

@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = collection.find_one({'username':request.form['username']})
        if username == user['username']:
            if password == user['password']:
                response = make_response(redirect(url_for('profile')))
                return response
            else:
                flash('Username or password is invalid', 'error')
        else:
            flash('Username or password is invalid!', 'error')

    return render_template('login.html')

@app.route('/signup',methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user = collection.find_one({'username':request.form['username']})
        if user:
            flash('Username is already existed', 'error')
        else:
            collection.insert_one({
                'username': request.form['username'],
                'password': request.form['password']
            })

        return render_template("signup.html",)

    return render_template('signup.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded', filename=filename))
        else:
            return 'invalid file'
    return render_template('upload.html')

@app.route('/uploaded/<filename>')
def uploaded(filename):
    print(filename)
    return send_from_directory('upload', filename)

app.run(host='localhost',port=5000,debug=True)
