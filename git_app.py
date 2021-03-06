# git_app.py
#
# A flask application to retrieve and display .yml or .json config files.
#
# Author: Pavana Achar
#
# CMPE 273, Spring 2017

import sys
from github import Github, UnknownObjectException
from flask import Flask,abort,make_response

app = Flask(__name__)

path = sys.argv[1].split("/")
user = path[3]
repo = path[4]

errstr = ""

@app.route("/v1/<filename>")
def FetchFileContents(filename):
	global errstr
	try:
		fileContent = Github().get_user(user).get_repo(repo).get_file_contents(filename).decoded_content

		if filename.endswith('.yml') or filename.endswith('.json'):
			return fileContent 
		else:
			raise TypeError()
		
	except UnknownObjectException:
		errstr = "ERROR : File not found."
		abort(404)

	except TypeError:
		errstr = "ERROR : Invalid File Type."
		abort(500)
	
	except Exception as e:
		print e
		errstr = "ERROR : Generic error."
		abort(500)


def GetRespObj(errcode):
        global errstr
        r = make_response(errstr, errcode)
        errstr = ""
        return r

@app.errorhandler(404)
def FileNotFound(e):
        return GetRespObj(404)

@app.errorhandler(500)
def GenericError(e):
        return GetRespObj(500)


if __name__ == "__main__":
	app.run(debug=True, host='0.0.0.0')
