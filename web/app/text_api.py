import numpy as np
import nltk
import MeCab
import warnings
from gensim.models import word2vec
from django.conf import settings


class TextAPI:
    def __init__(self, text):
        self._model = word2vec.Word2Vec.load(settings.BASE_DIR + "/app/wiki.model")
        self.shape = self._model.wv["私"].shape[0]

        self.text = text

    def extract_noun(self, text):
        """
        text から名詞を抽出し、そのリストを返す。
        """
        tagger = MeCab.Tagger("-Ochasen")
        tagger.parse("")
        node = tagger.parseToNode(text)
        keywords = []

        while node:
            if (node.feature.split(',')[0] == '名詞'):
                keywords.append(node.surface)
            node = node.next

        return keywords

    def get_text_vector(self, text):
        sum_vec = np.zeros(self.shape)
        word_count = 0
        noun = self.extract_noun(text)

        for t in noun:
            try:
                vec = self._model.wv[t]
                sum_vec += vec
                word_count += 1
            except KeyError:
                continue

        return sum_vec / word_count

    def vector_distance(self, text1, text2):
        v1 = self.get_text_vector(text1)
        v2 = self.get_text_vector(text2)

        return np.linalg.norm(v1 - v2)

    def calc_similarlities(self, cards):
        similarlities = {}

        for card in cards:
            # 厳密でない．本来ならばIDを比較すべき．
            if self.text == card.bio:
                continue
            sim = self.vector_distance(self.text, card.bio)
            similarlities[card.id] = sim if sim is not np.nan else -1

        return similarlities

    def suggest_words(self, keywords1, keywords2):
        """
        keywords1, keywords2 に関連する単語のリストを返す
        """

        result = []
        warnings.filterwarnings('ignore')
        # 2つのリストを連結する
        keywords = keywords1 + keywords2
        tmp = []
        for word in keywords:
            try:
                tmp.append(self._model.wv.most_similar(positive=word)[0])
            except:
                continue

        return list(set([ words[0] for words in tmp ]))

    def get_suggest_words(self, others_text):
        keywords1 = self.extract_noun(self.text)
        keywords2 = self.extract_noun(others_text)
        return ', '.join(self.suggest_words(keywords1, keywords2))
