# Filename - server.py

# Import flask and datetime module for showing date and time
from flask import Flask
import datetime
#from flask_cors import CORS

x = datetime.datetime.now()

# Initializing flask app
app = Flask(__name__)
#CORS(app, origins="*")


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

	
# Running app
if __name__ == '__main__':
	app.run(debug=True)
