import os
import json
import re

from flask import Flask, request, jsonify

from modules.GenerateText import GenerateText
from modules.rhyme_distance_meter import RhymeDistanceMeter

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
w2v_model_path = os.path.join(data_dir, 'jawiki.word_vectors.200d.bin')
chain_db_path  = os.path.join(data_dir, 'chain.db')
chara_word = '野球'
rdm = RhymeDistanceMeter(chara_word=chara_word)
generator = GenerateText(chara_word=chara_word, w2v_model_path=w2v_model_path, chain_db_path=chain_db_path)

@app.route('/')
def hello():
    return 'Hello world!'

@app.route('/rap', methods=['POST'])
def rap():
    if request.form:
        verse = request.form['verse']
    elif request.data:
        jsons = str(request.data, encoding='utf-8')
        data = json.loads(jsons)
        verse = data['verse']

    v1, v2 = re.split('\W+', verse)

    vd = rdm.throw(v1, v2)

    gen_txt, distance = generator.generate(verse, reverse=True)
    print(f'{verse}')
    print(f'{vd=}')
    print('----')
    print(f'{gen_txt}')
    print(f'{distance=}')

    return jsonify({
        "receive_distance": vd,
        "gen_text": gen_txt,
        "gen_distance": distance
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0')
