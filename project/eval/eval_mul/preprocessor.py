import nltk
from keras.preprocessing.sequence import pad_sequences
from tqdm import tqdm
import numpy as np


def words_features(words, embedding_dict):
    X1 = tokenize(words, embedding_dict, sequence=True)
    #X1 = pad_sequences(X1, padding="post")
    X2 = char_tokenize(words, sequence=True)
    #X2 = my_pad_sequences(X2)
    return X1, X2


def char_tokenize(text, n_char=256, sequence=False):
    out = []
    if sequence:
        words = text
    else:
        words = nltk.word_tokenize(text)
    for word in words:
        tmp = []
        for c in list(word):
            cnum = ord(c)
            if cnum > n_char:
                tmp.append(1)
            else:
                tmp.append(cnum)
        out.append(tmp)
    return out


def create_embedding_weights(kv, nb_words=500000, emb_dim=300):
    embedding_matrix = np.zeros((nb_words, emb_dim))
    embedding_dict = {}
    embedding_dict["<PAD>"] = 0
    embedding_dict["<UNK>"] = 1
    embedding_matrix[1].fill(1.0)
    for i, (word, _) in tqdm(enumerate(kv.wv.vocab.items())):
        if i >= nb_words - 2:
            break
        embedding_dict[word] = i + 2
        embedding_matrix[i + 2] = kv.wv[word]
    return embedding_dict, embedding_matrix


def tokenize(text, embedding_dict, sequence=False):
    out = []
    if sequence:
        words = text
    else:
        words = nltk.word_tokenize(text)

    for word in words:
        word = word.lower()
        try:
            out.append(embedding_dict[word])
        except KeyError:
            out.append(embedding_dict["<UNK>"])
    return np.array(out, dtype=np.int32)


def my_pad_sequences(sequences):
    max_sent_len = 0
    max_word_len = 0
    for sent in sequences:
        max_sent_len = max(len(sent), max_sent_len)
        for word in sent:
            max_word_len = max(len(word), max_word_len)
    x = np.zeros((len(sequences), max_sent_len, max_word_len)).astype('int32')
    for i, sent in enumerate(sequences):
        for j, word in enumerate(sent):
            x[i, j, :len(word)] = word
    return x
