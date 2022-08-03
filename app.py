from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase


config = {
  "apiKey": "AIzaSyDaCr-50_N3lORl1nwcHqfKgA7gXN1I830",
  "authDomain": "classroom-f0484.firebaseapp.com",
  "projectId": "classroom-f0484",
  "storageBucket": "classroom-f0484.appspot.com",
  "messagingSenderId": "552127108692",
  "appId": ":552127108692:web:8fb2c5e12d42de9d937fc1",
  "measurementId": "G-7SXDX14H3Z",
  "databaseURL": "https://classroom-f0484-default-rtdb.europe-west1.firebasedatabase.app/"
}


 

firebase = pyrebase.initialize_app(config)
auth = firebase.auth ()
db = firebase.database()


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'






@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error=""
    if request.method == 'GET':
        return render_template("signup.html")
    else:
        email = request.form['email']
        password = request.form["password"]
        login_session['user']= auth.create_user_with_email_and_password(email, password)
        student =  {"email": request.form['email'], "password": request.form['password']}

        db.child("Users").child(login_session['user']['localId']).set(student)

        return redirect(url_for('classes'))
        # except:
        #     print("sorry")
        #     return render_template("signup.html")






@app.route('/', methods=['GET', 'POST'])
def signin():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form["password"]
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('classes'))
        except:
            error = "Authentication failed"
            return render_template("signin.html")
    else:
      return render_template("signin.html")



@app.route('/classes', methods=['GET', 'POST'])
def classes():
    error=""
    if request.method =="POST":
        name = request.form['name']
        text = request.form['text']
        image_link = request.form['image link']
    

        new_class = {"name": request.form['name'], "text": request.form['text'], "image_link": request.form['image link']}
        db.child("new_class").push(new_class)
            
        return redirect (url_for("new_class"))

    else:

        print ("class can't be created")
        return render_template ("home.html")




if __name__ == '__main__':
    app.run(debug=True)
