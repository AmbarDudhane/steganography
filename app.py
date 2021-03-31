from flask import Flask, render_template, request, flash
from flask_mysqldb import MySQL
from werkzeug.utils import secure_filename
import os
from ImageStegno import ImageStegno
from VideoStegno import VideoStegno
from textstegno import TextStegno

app = Flask(__name__)

app.config['SECRET_KEY'] = "random string"
# app.config['MYSQL_HOST'] = '127.0.0.1'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'mysql123'
# app.config['MYSQL_DB'] = 'assignment2'

app.config['MYSQL_HOST'] = 'mysql://bcbe3ecbe657e9:9bc1f7f8@us-cdbr-iron-east-05.cleardb.net/heroku_8f20dfbc3cc6da2?reconnect=true'
app.config['MYSQL_USER'] = 'bcbe3ecbe657e9'
app.config['MYSQL_PASSWORD'] = '9bc1f7f8'
app.config['MYSQL_DB'] = 'heroku_8f20dfbc3cc6da2'



app.config['UPLOAD_FOLDER'] = "temp"

mysql = MySQL(app)


@app.route('/')
def hello_world():
    return render_template('homepage.html')


@app.route('/login')
def login():
    return render_template('Login.html')


@app.route('/index')
def index():
    return render_template('Index.html')


@app.route('/showregister')
def showregister():
    return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['first_name']
        lastname = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO tbluser (email, first_name, last_name, password) VALUES (%s, %s, %s, %s)",
                    (email, firstname, lastname, password))
        mysql.connection.commit()
        cur.close()
        flash('Record was successfully added')
        print(request.form['first_name'], " Record added successfully")
    return render_template('Index.html')


@app.route('/checklogin', methods=['POST'])
def checklogin():
    if request.method == 'POST':
        result = request.form
        print("Email: ", result["login"])
        print("Password: ", result["password"])
        temp = (result["login"], result["password"])
        cur = mysql.connection.cursor()
        cur.execute("SELECT email, password FROM tbluser")
        rv = cur.fetchall()
        print(rv)
        if temp in rv:
            return render_template("HideMessage.html")
        else:
            return "Login unsuccessful"

    return render_template('Index.html')


@app.route('/ProcessEncryption', methods=['POST'])
def processEncryption():
    fileobj = request.files['myfile']

    filename = secure_filename(fileobj.filename)
    fileobj.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # img.save(secure_filename(img.filename))     #save it to temp location
    # filename = img.filename
    print("File Name:", filename, " Secret msg: " + request.form['secretmessage'])
    filetype = checkExtensionType(filename)
    if filetype == 'image':
        imgsteg = ImageStegno()
        imgsteg.encode_text(request.form['secretmessage'], filename)
    elif filetype == 'text':
        txtsteg = TextStegno()
        txtsteg.encodetext(request.form['secretmessage'], filename)
    elif filetype == "video":
        vidsteg = VideoStegno()
        vidsteg.loadVideo(request.form['secretmessage'], filename)
    return ""


def checkExtensionType(filename):
    img_extensions = ['png', 'jpg', 'jpeg']
    txt_extensions = ['txt']
    video_extensions = ["mp4", "avi", "wmv"]
    splitlist = filename.split(".")

    if splitlist[1] in img_extensions:
        return "image"
    elif splitlist[1] in txt_extensions:
        return "text"
    elif splitlist[1] in video_extensions:
        return "video"


if __name__ == '__main__':
    # db.create_all()
    app.run()
