### version tutoriel 

from flask import Flask

app = Flask(__name__)


@app.route('/')
def salut():
    return 'Salut tout le Monde !'


@app.route('/salut_perso/<string:first_name>')
def salut_toi(first_name):
    return f"Salut {first_name} !"


if __name__ == '__main__':
    app.run(host="0.0.0.0")