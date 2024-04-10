# Filename - server.py
# Import flask and datetime module for showing date and time
import logging
import datetime
import os

from flask import Flask, flash, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin


#from flask_cors import CORS

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)
CORS(app, origins="*")


# Route for seeing a data
@app.route('/data')
def get_time():
    
	# Returning an api for showing in reactjs
	return {
		'Name':"Plat 1", 
		"Date":x, 
		"Embeddings": "123", 
		"pdf": "OCR-22"
		}

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('HELLO WORLD')



UPLOAD_FOLDER = './pdfUploads'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET','POST'])
def fileUpload():
    if request.method == 'POST':
        target=os.path.join(UPLOAD_FOLDER,'test_docs')
        if not os.path.isdir(target):
            os.mkdir(target)
        logger.info("welcome to upload`")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file'] 
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
        #filename = secure_filename(file.filename)
        #destination="/".join([target, filename])
        #file.save(destination)
        #session['uploadFilePath']=destination
        response={
             'file': file, 
             'filename': filename
        }
    else:
          response=response={
             'file': 'file', 
             'filename': 'filename'
        }      
    return response
	
# Running app
if __name__ == '__main__':
	app.run(debug=True)

flask_cors.CORS(app, expose_headers='Authorization')