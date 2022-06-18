from face_reg import encode_image, image_search
from flask import Flask,render_template,url_for,request,flash,redirect
from werkzeug.utils import secure_filename
# from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
import pickle
import os

UPLOAD_FOLDER = 'static/uploads/'
OUTPUT_FOLDER = 'static/output/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image(file, fullname, upload_folder):
    print(file.filename)
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        file.filename = fullname+'.jpeg'
        filename = secure_filename(file.filename)
        file.save(os.path.join(upload_folder, filename))
        # name = os.path.join(app.config['UPLOAD_FOLDER'], fullname+'.jpeg')
        #print('upload_image filename: ' + filename)
        
        
        return filename
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite' #os.environ['DATABASE_URL']  #
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column('user_id', db.Integer, primary_key = True)
    fname = db.Column(db.String(100))
    mname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    gender = db.Column(db.String(10))
    date = db.Column(db.String(20))
    bvn = db.Column(db.String(50))
    email = db.Column(db.String(50))
    marital = db.Column(db.String(50))
    nationality = db.Column(db.String(50))
    motherName = db.Column(db.String(50))
    addr = db.Column(db.String(200))
    nokName = db.Column(db.String(50))
    nokRelationship = db.Column(db.String(50))
    phone = db.Column(db.String(12))
    nokPhone = db.Column(db.String(12))
    nokaddr = db.Column(db.String(200))
    password = db.Column(db.String(50))
    picture = db.Column(db.String(20))
    

def __init__(self, fname, mname, lname, gender, date, bvn, email, marital, nationality, motherName,  addr,
nokName, nokRelationship, phone, nokPhone, nokaddr, password, picture):
    self.fname = fname
    self.mname = mname
    self.lname = lname
    self.gender = gender
    self.date = date
    self.bvn = bvn
    self.email = email
    self.marital = marital
    self.nationality = nationality
    self.motherName = motherName
    self.addr = addr
    self.nokName = nokName
    self.nokRelationship = nokRelationship
    self.phone = phone
    self.nokPhone = nokPhone
    self.nokaddr = nokaddr
    self.password = password
    self.picture = picture


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/info/<string:user>')
def info(user):
    user = User.query.filter_by(fname = user).first_or_404(description='There is no data with {}'.format(user))
    print(user.fname)
    print(user.picture)
    return render_template('info.html', user = user, filename = user.picture)

# @app.route('/search', methods = ['GET', 'POST'])
# def search_file():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#                 flash('No image part')
#                 return redirect(request.url)
#         fullname = request.form['fullname']
#         file = request.files['file']
#         saved_image = upload_image(file, fullname, app.config['OUTPUT_FOLDER'] )
#         output_image = image_search(saved_image)
#         print(output_image[1][0])
#         picture = '{}.jpeg'.format(output_image[1][0])
#         # flash('Found image of {}' .format(output_image[1]))
#         criminal = User.query.filter_by(picture = picture).first_or_404(description='There is no data with {}'.format(output_image[1][0]))
        
        # criminal = Criminals.query.filter_by(name = fullname).first_or_404(description='There is no data with {}'.format(fullname))
        # print(criminal.picture)
        # print(criminal.name)
        # print(criminal)

        # return render_template('search.html', output = output_image[0], criminal = criminal)

@app.route('/info/<string:login_user>', methods = ['GET', 'POST'])
def get_info(login_user):
    user = User.query.filter_by(fname = login_user).first_or_404(description='There is no data with {}'.format(login_user))
    print(user)
    print(user.fname)
    print(user.picture)
    return render_template('info.html', user = user)


@app.route('/', methods=['POST'])
def upload():

    # if 'file' not in request.files:
    #         flash('No image part')
    #         return redirect(request.url)
# Recieves the input from the html file
    if request.method == "POST":
        
        
        # print(file)
        # print(file.filename)

        # if 'Check' in request.form:
        if request.form.get('create'):
            file = request.files['image']
            bvn = request.form['bvn']
            
            phone = request.form['mobileNumber']
            fname = request.form['fname']
            print(fname)
            mname = request.form['mname']
            lname = request.form['lname']
            gender = request.form.get('gender')
            date = request.form['date']
            email = request.form['email']
            marital = request.form.get('marital')
            nationality = request.form['nationality']
            motherName = request.form['motherName']
            address = request.form['address']
            nokName = request.form['nokName']
            nokRelationship = request.form['nokRelationship']
            nokNumber = request.form['nokNumber']
            nokAddress = request.form['nokAddress']
            password = request.form['password2']

            saved_image = upload_image(file, fname, app.config['UPLOAD_FOLDER'])
            print('it got in here')

            user = User(bvn = bvn, fname =fname, mname = mname, lname = lname, gender =gender, date =date, addr = address, phone =phone, password =password, picture = saved_image, nokaddr = nokAddress, nokName = nokName, nokRelationship = nokRelationship, nokPhone = nokNumber, email = email, marital = marital, nationality = nationality, motherName = motherName)

            db.session.add(user)
            db.session.commit()

            encoded_image = encode_image(saved_image)
            flash('Image successfully uploaded and displayed')
            return redirect(url_for('info', user = user.fname)) #render_template('info.html', user = user)
        elif request.form.get('login'):
            file = request.files['image']
            # email = request.form['email']
            saved_image = upload_image(file, 'image', app.config['OUTPUT_FOLDER'] )
            output_image = image_search(saved_image)
            name = output_image[1][0]
            picture = '{}.jpeg'.format(output_image[1][0])
            return redirect(url_for('get_info', login_user = name)) #render_template('info.html', user = user)
    #     print(output_image[1])
    #     flash('Found image of {}' .format(output_image[1]))
    #     return render_template('index.html', output = output_image[0])
    # else:
    #     return 'Bad paramters'



@app.route('/display/<filename>', methods=['GET'])
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=302)

@app.route('/display/<output>', methods=['GET'])
def display_output(output):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', output='output/result/' + output), code=302)


if __name__ == '__main__':
    db.create_all()
    app.run(port=5000, debug=True)