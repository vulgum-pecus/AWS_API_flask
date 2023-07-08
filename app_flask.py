import pickle

from flask import Flask, jsonify
import numpy as np

app = Flask(__name__)


### TODO ### Modifier le chemin pour récupérer le modèle entrainé
# model = pickle.load(open('path/to/model/model.pkl', 'rb'))
### END TODO ###

@app.route('/')
def welcome():
    return "Bienvenue dans l'API de prédiction des tags"


@app.route('/predict_tags/<string:question>')
def predict_tags(question):
    ### TODO ### Mettre toutes les étapes de prétraitements permettant de réaliser la prédiction de tag de la question
    all_tags = ['python', 'c++', 'java']  # A SUPPRIMER
    # tag = model.predict(question)  # A ADAPTER
    ### END TODO ###
    return jsonify(np.random.choice(all_tags))  # A REMPLACER PAR : jsonify(tag)


if __name__ == '__main__':
    app.run(host="0.0.0.0")
