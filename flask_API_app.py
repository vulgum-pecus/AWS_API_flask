import tensorflow as tf
import tensorflow_hub as hub
import pickle
import numpy as np
import spacy
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def bienvenue():
    message = ''' *** Bienvenue sur l'API de prédiction de tags pour une question du site StackOverFlow ! *** \n \n 

    Veuillez entrer, SVP, le endpoint /predict_tags/ à la suite de l'URL de l'API et poser votre question. \n \n 

    Le modèle vous suggérera des tags représentatifs du thème de votre question.'''
    return "<pre>{}</pre>".format(message)

@app.route('/predict_tags/<string:question>')
def predict_tags(question):
    
    # 1. tokenization, lemmatization  et conversion en liste
    nlp = spacy.load("en_core_web_sm")
    tokenized_question = nlp(question)
    lemmatized_question = [token.lemma_ for token in tokenized_question if not (token.is_stop or token.is_space)]
    lemmatized_question= [" ".join(lemmatized_question)]
    
   # 2. recupération des pickles pour le classifier et le multilabel binarizer
    chemin_mlbinarizer = '230817_mlbinarizer.pkl'
    with open(chemin_mlbinarizer, 'rb') as file:
        mlbinarizer = pickle.load(file)

    chemin_classifier = '230817_USEclassifier.pkl'
    with open(chemin_classifier, 'rb') as file:
        classifier = pickle.load(file)

    # 3. transformer la question en un vecteur UniversalSentenceEncoder
    ## import trained USE model
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    embedding_model = hub.load(module_url)
    
    ## generate embeddings for our question
    embedded_question = embedding_model(lemmatized_question)
    print(embedded_question.shape)

    # 4. prédictions
    tag_pred = classifier.predict(embedded_question)

    ## Transform predicted tags back to original format
    prediction = mlbinarizer.inverse_transform(tag_pred)

    response=jsonify({'Voici une suggestion de tags pour le contenu de votre question' : prediction})
    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0")