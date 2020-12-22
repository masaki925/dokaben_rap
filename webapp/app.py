import os
import json
import re

from flask import Flask, request

from modules.GenerateText import GenerateText
from modules.rhyme_distance_meter import RhymeDistanceMeter

app = Flask(__name__)
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
w2v_model_path = os.path.join(data_dir, 'jawiki.word_vectors.200d.bin')
chain_db_path  = os.path.join(data_dir, 'chain.db')
chara_word = '野球'

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/rap', methods=['POST'])
def rap():
    generator = GenerateText(chara_word=chara_word, w2v_model_path=w2v_model_path, chain_db_path=chain_db_path)
    if request.form:
        verse = request.form['verse']
    elif request.data:
        jsons = str(request.data, encoding='utf-8')
        data = json.loads(jsons)
        verse = data['verse']

    v1, v2 = re.split('\W+', verse)

    rdm = RhymeDistanceMeter(chara_word=chara_word)
    vd = rdm.throw(v1, v2)

    gen_txt, distance = generator.generate(verse, reverse=True)
    print(f'{verse}')
    print(f'{vd=}')
    print('----')
    print(f'{gen_txt}')
    print(f'{distance=}')

    return gen_txt


if __name__ == '__main__':
    app.run(host='0.0.0.0')
