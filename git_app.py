import sys
from github import Github
from flask import Flask,jsonify
import yaml,json

app=Flask(__name__)

path =  sys.argv[1].split("/")
user = path[3]
repo = path[4]

global d

@app.route("/v1/<filename>")

def hello(filename):
	
	fileContent = Github().get_user(user).get_repo(repo).get_contents(filename).decoded_content

	if filename.endswith('.yml'):
		return yaml.load(msg)	

	if filename.endswith('.json'):	
		d =  json.loads(msg)
		return jsonify(d) 


if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
	
