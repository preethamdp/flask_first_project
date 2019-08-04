from flask import Flask,render_template
from flask_cors import CORS
from flask import jsonify
from flask import request
import partial_bot
import noun_extractor
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
@app.route("/api/",methods=['GET'])
def home():
    req = (request.args.get('r'))  
    print(str(req))
    req = noun_extractor.convert_to_noun(str(req))
    res = (partial_bot.chat(req))
    print(res)
    return jsonify(res)

@app.route("/about")
def about():
    return render_template('about.html',title = 'About')

if __name__ == "__main__":
    app.run(debug=True)