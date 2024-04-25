# Filename - server.py
# Import flask and datetime module for showing date and time
import logging
import datetime
import os
import json
import configparser

from bson import json_util, ObjectId
from flask import Blueprint, Flask, flash, request, redirect, url_for, session, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
#from PDFembedding import load_pdf
from factory import create_app
from plats_api import movies_api_v1
from db import get_movie, get_movies, get_plats

#from flask_cors import CORS

x = datetime.datetime.now()

# taken from https://www.mongodb.com/compatibility/setting-up-flask-with-mongodb
config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join( ".ini")))


# Initializing flask app
app = Flask(__name__)

#pp.register_blueprint(movies_api_v1, url_prefix="/all_movies")
#app.register_blueprint(movies_api_v1, url_prefix="/id/<id>")

app.secret_key = os.urandom(24)
app.config['MONGO_URI'] = config['PROD']['DB_URI']

CORS(app, origins="*")

plat_list = []

class MongoJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        if isinstance(obj, ObjectId):
            return str(obj)
        return json_util.default(obj, json_util.CANONICAL_JSON_OPTIONS)
    
app.json_encoder = MongoJsonEncoder

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


DOWNLOAD_DIRECTORY ='./pdfUploads/test_docs'
# to download files from the flask API
# to download these files directly run 'http://127.0.0.1:5000/upload/DOCUMENT NAME'
@app.route('/upload/<path:path>', methods=['GET'])
def get_files(path):
    try: 
      response = {
          'directory': DOWNLOAD_DIRECTORY, 
          'path': path
      }
      return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)
    except FileNotFoundError:
        print(FileNotFoundError)

@app.route('/upload', methods=['GET'])
def index():
    json_data = read_json_file('platList.json')
    return jsonify(json_data)
    #return {}
# functions to upload PDFs to the testfolder on a local machine 

@app.route('/upload', methods=['POST'])
@cross_origin()
def fileUpload():
    filePrompt = request.form['filename']
    target=os.path.join(UPLOAD_FOLDER,'test_docs')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("welcome to upload`")
        # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file'] 
    #file_read = file.read()
    print(file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
        
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        destination="/".join([target, filename])
        print(destination)
        file.save(destination)
        session['uploadFilePath']=destination
        #return("success")

        #request.post()
        file_features_dict = dict({'File Path': filename, 
                                   'File': destination, 
                                   'Prompt':  filePrompt
                                   
                               }) 
        #load_pdf(destination)
    
    file_path = 'platList.json'   
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            plat_list = data['plat_list']
    except FileNotFoundError:
            # If the file does not exist, initialize an empty list
        plat_list = []
    except json.JSONDecodeError:
            # If the file is empty or corrupted, initialize an empty list
        plat_list = []
    
    plat_list.append(file_features_dict)

    with open(file_path, 'w') as file: 
            json.dump({'plat_list': plat_list}, file, indent=4, sort_keys=True)
    
    return redirect(url_for('index'))


def read_json_file(file_path):
    """
    Reads a JSON file and returns its contents.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    dict: The contents of the JSON file.
    """
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        # Return None or raise an exception if the file doesn't exist
        print(f"No file found at {file_path}")
        return None
    except json.JSONDecodeError:
        # Handle the case where the file is empty or improperly formatted
        print(f"Error decoding JSON from {file_path}")
        return None

#TESTING MONGODB CONNECTION TO DATABASE
'''@app.route('/all_movies', methods=['GET'])
def api_get_movies():
    MOVIES_PER_PAGE = 20
    response ="flask api working"
    (movies, total_num_entries) = get_movies(
        None, page=0, movies_per_page=MOVIES_PER_PAGE)

    response = {
        "movies": movies,
        "page": 0,
        "filters": {},
        "entries_per_page": MOVIES_PER_PAGE,
        "total_results": total_num_entries,
    }
    #return("flask api is working")
    #return jsonify(response)
    data = json_util.dumps(response)
    return json.loads(data)'''

@app.route('/all_plats', methods=['GET'])
def api_get_plats():
    (plats) = get_plats(page=0, items_per_page=20)

    response = {
        "plats": plats,
    }

    data = json_util.dumps(response)
    return json.loads(data)


# Running app
if __name__ == '__main__':
	#app.run(debug=True)
    #app.secret_key = os.urandom(24)
    
    #app.config['MOGO_URI'] = config['PROD']['DB_URI']
    app.run(debug=True,use_reloader=False)

#cross_origin.CORS(app, expose_headers='Authorization')

