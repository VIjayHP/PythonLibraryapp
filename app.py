from flask import Flask, render_template, json, flash, request
from flask.ext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField

mysql = MySQL()
app = Flask(__name__)
class BooksData(Form):
    name = TextField('Name:', validators=[validators.required()])

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'jay'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()
@app.route("/", methods=['GET', 'POST'])
def hello():
    form = BooksData(request.form)
    print form.errors
    if request.method == 'POST':
        Bookname=request.form['name']
        print Bookname
        Authorname=request.form['name']
        print Authorname
        if form.validate():
            # Save the comment here.
            flash('Hello')
        else:
            flash('All the form fields are required. ')
            return render_template('hello.html', form=form)

if __name__ == "__main__":
    app.run(port=5002)
