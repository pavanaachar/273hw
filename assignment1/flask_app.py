from flask import Flask

app=Flask(__name__)

@app.route("/")
def hello():
	return "hello from dockerized Flask app"

if __name__ == "__main__":
	app.run(debug=True,host='0.0.0.0')
