from flask import Flask,render_template
from flask_cors import CORS
from flask import jsonify
app = Flask(__name__)
CORS(app)


posts = [
    {
        'title':'test1',
        'author':'Name1',
        'content':'loerm ipsum'
    },
    {
        'title':'test2',
        'author':'Name2',
        'content':'ipsum lorem'
    }
]
@app.route("/home")
@app.route("/api/")
def home():
    return jsonify(posts)

@app.route("/about")
def about():
    return render_template('about.html',title = 'About')

if __name__ == "__main__":
    app.run(debug=True)