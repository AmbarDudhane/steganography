from flask import Flask, render_template, request, flash, send_file
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

app.config['MYSQL_HOST'] = 'us-cdbr-east-03.cleardb.com'
app.config['MYSQL_USER'] = 'b569df9f38e2c9'
app.config['MYSQL_PASSWORD'] = 'd0501f82'
app.config['MYSQL_DB'] = 'heroku_e288a286b7783b3'


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
    # List all files in a directory using os.listdir
    basepath = './encrypted/'
    filelist = []
    for entry in os.listdir(basepath):
        if os.path.isfile(os.path.join(basepath, entry)):
            filelist.append(entry)
    print("File List:", filelist)
    return render_template('Index.html', filelist=filelist)


@app.route('/download/<fileName>')
def downloadFile(fileName):
    print("File name to download: ", fileName)
    try:
        return send_file(r'./encrypted/' + fileName, as_attachment=True)
    except Exception as e:
        return str(e)


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
        # flash('Record was successfully added')
        print(request.form['first_name'], " Record added successfully")
    return render_template('success_register.html')


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

    return ""


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
