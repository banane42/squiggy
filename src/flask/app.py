from flask import Flask

app = Flask(__name__)

@app.route("/wahapedia")
def index():
	return "<p>Hello, World!</p>"
