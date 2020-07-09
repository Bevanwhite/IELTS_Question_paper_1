from flask import Flask, request, jsonify
from keras.models import Sequential
from keras.layers.recurrent import LSTM, SimpleRNN
from keras.layers import Dropout, Dense
from sklearn.model_selection import train_test_split
from keras import backend as K
import nltk
# nltk.download('punkt')
from pymagnitude import Magnitude
import numpy as np
# C: // Users/Bevan/Downloads/research
model = Magnitude(
    'C://Users/Bevan/Downloads/research/GoogleNews-vectors-negative300.magnitude')

app = Flask(__name__)


def load_model():

    K.clear_session()
    nmodel = Sequential()
    nmodel.add(LSTM(units=96, return_sequences=True, input_shape=(30, 300)))
    nmodel.add(Dropout(0.2))
    nmodel.add(LSTM(units=96, return_sequences=True))
    nmodel.add(Dropout(0.2))
    nmodel.add(LSTM(units=96, return_sequences=True))
    nmodel.add(Dropout(0.2))
    nmodel.add(LSTM(units=96, return_sequences=False))
    nmodel.add(Dropout(0.2))
    nmodel.add(Dense(units=5, activation='softmax'))
    nmodel.compile(loss='categorical_crossentropy',
                   optimizer='adam', metrics=['accuracy'])
    nmodel.load_weights('Cohesion LSTM V2.h5')

    return nmodel


@app.route('/', methods=['POST'])
def home():
    return(jsonify(results="Successfull"))


@app.route('/get_prediction', methods=['POST', 'GET'])
def get_prediction():

    category_dict = {0: 0, 1: 25, 2: 50, 3: 75, 4: 100}

    User_json = request.json
    paragraph = User_json['para']

    data_tok = nltk.word_tokenize(paragraph)

    data_vector = [model.query(word) for word in data_tok]

    sentence_end = np.ones((300,), dtype=np.float32)

    data_vector[29:] = []  # limitting the words in a sentence to 30
    data_vector.append(sentence_end)

    if(len(data_vector) < 30):
        for i in range(30-len(data_vector)):
            # filling the empty words from vector of ones
            data_vector.append(sentence_end)

    data_vector = np.array(data_vector)

    data_vector = data_vector.reshape(1, 30, 300)

    nmodel = load_model()
    results = nmodel.predict(data_vector)

    marks_category = np.argmax(results, axis=1)[0]

    print(results, marks_category)

    marks = [{"marks": category_dict[marks_category]}]

    return(jsonify(results=marks))


app.run(debug=True)
