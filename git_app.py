import sys
from github import Github
from flask import Flask,jsonify,abort,make_response
import yaml,json

app=Flask(__name__)

path =  sys.argv[1].split("/")
user = path[3]
repo = path[4]


@app.route("/v1/<filename>")
def hello(filename):
	
	try:
		fname = filename.split(".")[0]
		fname= fname+".yml"

		fileContent = Github().get_user(user).get_repo(repo).get_file_contents(fname).decoded_content

		if filename.endswith('.yml'):
			return fileContent 

		elif filename.endswith('.json'):	
			return json.dumps(yaml.load(fileContent),sort_keys=True,indent=2)

		else:
			return "Invalid file type"
		
		
	except:
		abort(404)

@app.errorhandler(404)
def FileNotFound(e):
	return make_response("error : file not found")
	

		

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
	
