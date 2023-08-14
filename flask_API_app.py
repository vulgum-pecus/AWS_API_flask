<<<<<<< HEAD
# version retrogradée pour compatibilité EC2

import tensorflow as tf
import tensorflow_hub as hub
import pickle
import numpy as np
=======
# version classifier sur corpus tokenizé et lemmatisé

# import tensorflow as tf
import tensorflow_hub as hub
import pickle
import numpy as np
import spacy
>>>>>>> d95da4fa118f9242bd4a551ab7fc63cd740caad1
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/')
def bienvenue():
<<<<<<< HEAD
    message = " *** Bienvenue sur l'API de prédiction de tags pour une question du site StackOverFlow ! *** \n \n Veuillez entrer, SVP, le endpoint predict_tags/ à la suite de l'URL de l'API et poser votre question. Le modèle vous suggérera des tags représentatifs du thème de votre question"
    return "<pre>{}</pre>".format(message)

@app.route('/predict_tags/<string:question>')
def predict_tags(question):

    # 1. recupération des pickles pour le classifier et le multilabel binarizer
    chemin_mlbinarizer = 'mlbinarizer.pkl'
    with open(chemin_mlbinarizer, 'rb') as file:
        mlbinarizer = pickle.load(file)

    chemin_classifier = 'USEclassifier.pkl'
    with open(chemin_classifier, 'rb') as file:
        USEclassifier = pickle.load(file)

    # 2. transform the question into USE vector
    ## import trained USE model
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    embedding_model = hub.load(module_url)

    ## define the question as a list 
    print(question)
    question_list=[question]
    
    ## generate embeddings for our question
    embedded_question = embedding_model(question_list)
    print(embedded_question.shape)

    # prédictions
    # Predict on the tag using the best classifier
    tag_pred = USEclassifier.predict(embedded_question)

    # Transform predicted tags back to original format
    prediction = mlbinarizer.inverse_transform(tag_pred)
=======
    return "Bienvenue sur l'API de prédiction de tags pour une question du site StackOverFlow"
>>>>>>> d95da4fa118f9242bd4a551ab7fc63cd740caad1

@app.route('/predict_tags/<string:question>')
def predict_tags(question):
    
    # 1. tokenization, lemmatization  et conversion en liste
    nlp = spacy.load("en_core_web_sm")
    tokenized_question = nlp(question)
    lemmatized_question = [token.lemma_ for token in tokenized_question if not (token.is_stop or token.is_space)]
    lemmatized_question= [" ".join(lemmatized_question)]
    
    # 2. recupération des pickles pour le classifier et le multilabel binarizer
    chemin_mlbinarizer = 'mlbinarizer.pkl'
    with open(chemin_mlbinarizer, 'rb') as file:
        mlbinarizer = pickle.load(file)

<<<<<<< HEAD
    response = {'Voici une suggestion de tags pour le contenu de votre question' : prediction}
    
    return jsonify(response)
=======
    chemin_classifier = 'USEclassifier.pkl'
    with open(chemin_classifier, 'rb') as file:
        USEclassifier = pickle.load(file)

    # 3. transformer la question en un vecteur UniversalSentenceEncoder
    ## import trained USE model
    module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
    embedding_model = hub.load(module_url)
    
    ## generate embeddings for our question
    embedded_question = embedding_model(lemmatized_question)
    print(embedded_question.shape)

    # 4. prédictions
    ## Predict on the tag using the best classifier
    tag_pred = USEclassifier.predict(embedded_question)

    ## Transform predicted tags back to original format
    prediction = mlbinarizer.inverse_transform(tag_pred)

    data = {'suggested tags for your question' : prediction}

    response=jsonify(data)
    return response
>>>>>>> d95da4fa118f9242bd4a551ab7fc63cd740caad1

if __name__ == '__main__':
    app.run(host="0.0.0.0")
