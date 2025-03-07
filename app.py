from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user
from flask_mail import Mail
from flask_bcrypt import Bcrypt
import json
import pickle as pkl
import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv() 



app = Flask(__name__)


with open('config.json', 'r') as c:
    params = json.load(c)["params"]


local_server = params['local_server']
app.secret_key = os.getenv("secret_key")  


if(local_server == "True"):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("production_URI")


app.config.update(                                       # Sending mail
    MAIL_SERVER = params['MAIL_SERVER'],                 # Default gmail server
    MAIL_PORT = params['MAIL_PORT'],                     # Default gmail port
    MAIL_USE_SSL = True,                                 # Using authentication
    MAIL_USERNAME = os.getenv("MAIL_USERNAME"),             # fetching mail
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD"),             # fetching app pass
)


mail = Mail()
login_manager = LoginManager()
Bcrypt = Bcrypt()
db = SQLAlchemy()


login_manager.init_app(app)
Bcrypt.init_app(app)
db.init_app(app)  
mail.init_app(app)


class users(UserMixin, db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    Username = db.Column(db.String(80), unique=True, nullable=False)
    Password = db.Column(db.String(80), nullable=False)
    Phone_num = db.Column(db.String(80), nullable=False)
    Mail_id = db.Column(db.String(80), unique = True, nullable=False)
    
    def get_id(self):
        return str(self.sno)


class contact(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    contact_name = db.Column(db.String(220), nullable=False)
    contact_email = db.Column(db.String(220), nullable=False)
    contact_phone_num = db.Column(db.String(220), nullable=False)
    contact_message = db.Column(db.String(220), nullable=False)


with app.app_context():
    db.create_all()
    
    
@login_manager.user_loader
def load_user(sno):
    return users.query.get(int(sno))


@app.route("/")
def initial_page():
    return render_template("initial_page.html", params = params)


@app.route('/login_page', methods = ['GET', 'POST'])
def login_page():
    if(request.method == 'POST'):
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        user = users.query.filter_by(Username = Username).first()
        if(user):
            valid = Bcrypt.check_password_hash(user.Password, Password)
            if(valid):
                login_user(user)
                return redirect(url_for('home_page'))
            flash('Invalid Username or Password. Please Check your Username or Password.')
            return redirect(url_for('login_page'))
        else:
            flash('You are not registered. Please Sign Up.')
            return redirect(url_for('login_page'))
                
    return render_template('login_page.html', params = params)


@app.route('/signup_page', methods = ['GET', 'POST'])
def signup_page():
    if(request.method == 'POST'):
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        Phone_num = request.form.get('Phone_num')
        Mail_id = request.form.get('Mail_id')
        user = users.query.filter_by(Username = Username).first()
        mail = users.query.filter_by(Mail_id = Mail_id).first()
        if(user):
            flash('Username already exists. Please try another Username.')
            return redirect(url_for('signup_page'))
        elif(mail):
            flash('Mail Id already exists. Please try another Mail Id.')
            return redirect(url_for('signup_page'))
        else:
            entry = users(Username = Username, Password = Bcrypt.generate_password_hash(Password).decode('utf-8'), Phone_num = Phone_num, Mail_id = Mail_id)
            db.session.add(entry)
            db.session.commit()
            return redirect(url_for('login_page'))
            
    return render_template("signup_page.html", params = params)


@app.route('/contact_page', methods = ['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        contact_name = request.form.get('contact_name')
        contact_email = request.form.get('contact_email')
        contact_phone_num = request.form.get('contact_phone_num')
        contact_message = request.form.get('contact_message')
        
        entry = contact(contact_name = contact_name, contact_email = contact_email, contact_phone_num = contact_phone_num, contact_message = contact_message)
        db.session.add(entry)
        db.session.commit()
        #sending mail
        mail.send_message('CONTACT MESSAGE RECEIVED',
                          sender = params['MAIL_USERNAME'],
                          recipients = [contact_email, params['MAIL_USERNAME']],
                          body = "Here are your contents: " + "\n" + "\n" + 
                          "Name: " + contact_name + "\n" +
                          "Email: " + contact_email + "\n" +
                          "Phone number: " + contact_phone_num + "\n" +
                          "Message sent: " + contact_message)
        return redirect(url_for('home_page'))
        
    return render_template('contact_page.html', params = params)


@app.route('/features_page')
def features_page():
    return render_template('features_page.html', params = params)

@app.route('/predictions', methods = ['GET', 'POST'])
def predictions():
    ans = None
    if request.method == 'POST':
        Age = request.form.get('Age')
        Pregnancies = request.form.get('Pregnancies')
        Glucose = request.form.get('Glucose')
        BloodPressure = request.form.get('BloodPressure')
        Insulin = request.form.get('Insulin')
        Bmi = request.form.get('BMI')
        SkinThickness = request.form.get('SkinThickness')
        Dpf = request.form.get('DPF')
        
        def predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, Bmi, Dpf, Age):
            input_data = pd.DataFrame([[Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, Bmi, Dpf, Age]])
            scaler = pkl.load(open('scaler.pkl', 'rb'))
            input_data = scaler.transform(input_data)
            model = pkl.load(open('nb.pkl', 'rb'))
            prediction = model.predict(input_data)
            if prediction == 1:
                return f"You have high chances of Diabetes! <br> Please consult a Doctor"  # Person is Diabetic
            else:
                return "You have low chances of Diabetes <br> Please maintain a healthy life style"  # Person is Non-Diabetic

        ans = predict(Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, Bmi, Dpf, Age)
        return redirect(url_for('detailed_predictions', ans = ans))

    return render_template('predictions.html', ans=ans)


@app.route("/detailed_predictions", methods = ['GET', 'POST'])
def detailed_predictions():
    ans = request.args.get('ans', default = "Try again", type = str)
    return render_template("detailed_predictions.html", params = params, ans = ans)
        

@app.route('/home_page', methods = ['GET', 'POST'])
def home_page():
    return render_template('home_page.html', params = params)


@app.route('/detailed_analysis')
def detailed_analysis():
    return render_template('detailed_analysis.html', params = params)


@app.route('/change_pass', methods = ['GET', 'POST'])
def change_pass():
    if request.method == 'POST':
        Username = request.form.get('Username')
        old_pass = request.form.get('old')
        new_pass = request.form.get('new')
        print(Username, old_pass, new_pass)
        user = users.query.filter_by(Username = Username).first()
        if(user):
            valid = Bcrypt.check_password_hash(user.Password, old_pass)
            if(valid):
                user.Password = Bcrypt.generate_password_hash(new_pass).decode('utf-8')
                db.session.commit()
                return redirect(url_for('login_page'))
            flash('Invalid Username or Password. Please Check your Username or Password.')
            return redirect(url_for('change_pass'))
        else:
            flash('You are not registered. Please Sign Up.')
            return redirect(url_for('change_pass'))
    return render_template('change_pass.html', params = params)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('initial_page'))


if __name__ == "__main__":
    app.run(debug=True)
