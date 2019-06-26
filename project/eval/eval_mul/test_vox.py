import json
import os
import sys

import gensim
import nltk
from keras.models import load_model
from tqdm import tqdm

import candidate_generator as cg
import entvec_encoder as eenc
import predictor as pr
import preprocessor as pre


os.environ["CUDA_VISIBLE_DEVICES"] = "-1"


def is_exist_models(langs):
    flag = True
    path = "../../train/model_wiki_{}.h5"
    for lang in langs:
        flag = flag and os.path.isfile(path.format(lang))
    return flag


def run(lang="en"):
    out = []
    with open("../../../eval_data/data/s_{}.json".format(lang)) as f:
        data = json.load(f)

    n_words = 3000000
    trie = cg.load(
        "../../wiki_processor/data/marisa_data/mention_stat_{}.marisa".format(
            lang))
    kv = eenc.load(
        "../../wiki_processor/entity_vectors/{}wiki_20180420_100d.bin".format(
            lang))
    model = load_model("../../train/model_wiki_{}.h5".format(lang))
    word2vec = gensim.models.KeyedVectors.load(
        "../../wiki_processor/data/w2v_models/word2vec_{}.model".format(lang),
        mmap="r")
    embedding_dict, embedding_matrix = pre.create_embedding_weights(
        word2vec, n_words)
    del (word2vec)
    del (embedding_matrix)
    for d in tqdm(data):
        words = nltk.word_tokenize(d["sentence"])
        X_list, cand_list, gram_list, ind_list = pr.feature(words,
                                                            trie,
                                                            kv,
                                                            embedding_dict,
                                                            n=10,
                                                            k=50)
        result = pr.predict(model,
                            X_list,
                            cand_list,
                            gram_list,
                            ind_list,
                            threshold=0.3)
        out.append({"true": d["entities"], "pred": result})

    with open("result_vox_{}.json".format(lang), "w") as f:
        json.dump(out, f, indent=4)


if __name__ == "__main__":
    import time
    import sys
    langs = ["de", "it", "es", "fr", "en"]
    counter = 0
    while not is_exist_models(langs):
        sys.stdout.write("waiting eval...[{}]\r".format(counter))
        sys.stdout.flush()
        time.sleep(1)
        counter += 1

    for lang in langs:
        run(lang)
