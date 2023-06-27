from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)


@app.route('/')
def salut():
    return 'Salut tout le Monde !'


@app.route('/salut_perso/<string:first_name>')
def salut_toi(first_name):
    return f"Salut {first_name} !"


@app.route('/predict_tags/<string:question>')
def predict_tags(question):
    all_tags = ['python', 'c++', 'java']
    return jsonify(np.random.choice(all_tags))


if __name__ == '__main__':
    app.run(host="0.0.0.0")
