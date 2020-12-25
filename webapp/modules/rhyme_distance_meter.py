
import os, sys
from logging import getLogger, basicConfig, DEBUG

from bert_score import BERTScorer
from fugashi import GenericTagger

from .utils import romanize, romanize_sentence, vowelize

# basicConfig(level=DEBUG)
logger = getLogger(__name__)

tagger = GenericTagger()

class RhymeDistanceMeter:
    def __init__(self, chara_word='野球'):
        self.c = chara_word
        data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
        self.baseline_file_path = os.path.join(data_dir, 'bert-base-multilingual-cased.tsv')
        self.scorer = BERTScorer(model_type=os.path.join(data_dir, 'bert-base_mecab-ipadic-bpe-32k_whole-word-mask'), num_layers=11, lang='ja', rescale_with_baseline=True, baseline_path=self.baseline_file_path)
        self.min_rhyme = 2

    def throw(self, s1, s2):
        rhyme_count = self.count_rhyme(s1, s2)
        sim_s, sim_c = self.score_similarity(s1, s2)
        len_rate = self.len_rate(s1, s2)
        dist = self.calc_dist(rhyme_count, sim_s, sim_c, len_rate)
        return dist

    def most_rhyming(self, killer_phrase, candidates, topn=3):
        res = {}
        for c in candidates:
            res[c] = self.count_rhyme(killer_phrase, c)
        logger.debug(f'{res=}')
        sorted_res = sorted(res.items(), key=lambda item: item[1], reverse=True)

        return [w[0] for w in sorted_res[:topn]]

    def len_rate(self, s1, s2):
        return min(len(s1), len(s2)) / max(len(s1), len(s2))

    def count_rhyme(self, s1, s2):
        romaji1 = romanize_sentence(s1)
        romaji2 = romanize_sentence(s2)

        vowel1 = vowelize(romaji1)
        vowel2 = vowelize(romaji2)
        logger.debug(f'{vowel1=}')
        logger.debug(f'{vowel2=}')

        min_len = min(len(vowel1), len(vowel2))

        cnt = 0
        # 脚韻
        for i in range(1, min_len+1):
            if vowel1[-i] == vowel2[-i]:
                cnt += 1
            else:
                break
        if cnt > 0:
            return cnt

        # 頭韻
        for i in range(min_len):
            if vowel1[i] == vowel2[i]:
                cnt += 1
            else:
                break

        return cnt

    def score_similarity(self, s1, s2):
        refs = [s1]
        hyps = [s2]

        s1_nouns = [w.surface for w in tagger(s1) if (w.feature[0] == '名詞' and w.surface != self.c)]
        s2_nouns = [w.surface for w in tagger(s2) if (w.feature[0] == '名詞' and w.surface != self.c)]
        logger.debug(f'{s1_nouns=}')
        logger.debug(f'{s2_nouns=}')

        for s in s1_nouns:
            refs.append(self.c)
            hyps.append(s)

        for s in s2_nouns:
            refs.append(self.c)
            hyps.append(s)

        logger.debug(f'{refs=}')
        logger.debug(f'{hyps=}')
        P, R, F1 = self.scorer.score(refs, hyps)
        dist_s = F1[0]

        logger.debug(f'{F1[1:]=}')
        dist_c = max(F1[1:])

        return dist_s, dist_c

    def calc_dist(self, count, sim_s, sim_c, len_rate):
        logger.debug(f'{count=}')
        logger.debug(f'{sim_s=}')
        logger.debug(f'{sim_c=}')
        logger.debug(f'{len_rate=}')
        return int(count ** ((1 - sim_s) * (sim_c * 10) * (1 + len_rate)))


if __name__ == '__main__':
    meter = RhymeDistanceMeter('野球')
    if len(sys.argv) != 3:
        sys.stderr.write(f"ERROR: invalid args.\n  USAGE: {sys.argv[0]} s1 s2\n")
        sys.exit(1)
    s1, s2 = sys.argv[1], sys.argv[2]
    distance = meter.throw(s1, s2)
    logger.debug(f"rhyme distance is {distance} m.")

