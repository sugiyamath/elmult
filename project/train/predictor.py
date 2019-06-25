from keras.models import load_model
import numpy as np
import nltk
from nltk.corpus import stopwords
import os

from keras.preprocessing.sequence import pad_sequences
import candidate_generator as cg
import entvec_encoder as eenc
import preprocessor as pre

os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def ngram(words, n):
    return list(zip(*(words[i:] for i in range(n))))


def feature(words, trie, kv, embedding_dict, n=6, k=30):
    X1 = []
    X2 = []
    X3 = []
    #X4 = []
    X5 = []
    X6 = []
    cands = []
    x1, x2 = pre.words_features(words, embedding_dict)
    for i in range(1, n):
        sent_mask = [0.0 for _ in range(len(words))]
        for gram, wind in zip(ngram(words, i), ngram(range(len(words)), i)):
            mention_words = list(gram)
            mention = ' '.join(mention_words)
            candidates = cg.generate_with_linkprob_and_windex(
                mention, wind[0], wind[-1], trie, k=k)
            encoded = eenc.encode_with_linkprob_and_windex(candidates, kv)
            for target in encoded:
                cands.append(target["candname"])
                x3 = sent_mask[:]
                x3[target["begin"]:target["end"]] = [
                    1.0 for _ in range(target["end"] - target["begin"])
                ]
                x3 = np.array(x3, dtype=np.int32)
                X1.append(x1)
                X2.append(x2)
                X3.append(x3)
                X5.append(target["entvec"])
                X6.append([target["linkprob"]])

    X1 = pad_sequences(X1, padding="post")
    X2 = pre.my_pad_sequences(X2)
    X3 = pad_sequences(X3, padding="post")
    X5 = np.array(X5)
    X6 = np.array(X6)
    return [X1, X2, X3, X5, X6], cands


def predict(model, X_list, cand_list, gram_list, threshold=0.005):
    out = []
    for X, cands, grams in zip(X_list, cand_list, gram_list):
        y_preds = [x[0] for x in model.predict(X)]
        if np.max(y_preds) < threshold:
            continue
        index = np.argmax(y_preds)
        out.append((cands[index], grams[index]))
    return out


if __name__ == "__main__":
    trie = cg.load("../data/mention_stat.marisa")
    kv = eenc.load("../entity_vector/enwiki_20180420_100d.bin")
    enc = lenc.Encoder()
    model = load_model("../models/model_wiki_tmp.h5")
    sent = None
    while sent != "-1":
        threshold = float(input("threshold>"))
        sent = input("sent>")
        words = nltk.word_tokenize(sent)
        X_list, cand_list, gram_list = feature(words, trie, kv, enc)
        result = predict(model, X_list, cand_list, gram_list, threshold)
        print(result)
