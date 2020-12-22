import os
import json

from flask import Flask, request

from modules.GenerateText import GenerateText

app = Flask(__name__)
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
w2v_model_path = os.path.join(data_dir, 'jawiki.word_vectors.200d.bin')
chain_db_path  = os.path.join(data_dir, 'chain.db')

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/rap', methods=['POST'])
def rap():
    generator = GenerateText(w2v_model_path=w2v_model_path, chain_db_path=chain_db_path)
    if request.form:
        verse = request.form['verse']
    elif request.data:
        jsons = str(request.data, encoding='utf-8')
        data = json.loads(jsons)
        verse = data['verse']

    gen_txt = generator.generate(verse)
    return gen_txt


if __name__ == '__main__':
    app.run(host='0.0.0.0')
