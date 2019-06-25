from data_generator import load_data_general, generate_wiki
from keras.layers import Input, Dense, Dropout, \
    Embedding, Bidirectional, TimeDistributed, LSTM, Concatenate, \
    SeparableConv1D, GlobalAvgPool1D, GlobalMaxPool1D
from keras.models import Model
from keras.callbacks import ModelCheckpoint


def build_model(
        embedding_matrix,
        n_words,
        n_char,
        wdim=200,
        cdim=25,
        rdim=1,
        entdim=100,
):
    in1 = Input(batch_shape=(None, None), dtype='int32')
    in2 = Input(batch_shape=(None, None, None), dtype='int32')
    in3 = Input(batch_shape=(None, None), dtype='int32')
    in5 = Input(shape=(entdim, ))
    in6 = Input(shape=(1, ))
    wemb1 = Embedding(n_words,
                      wdim,
                      weights=[embedding_matrix],
                      trainable=False,
                      mask_zero=False)(in1)
    cemb1 = Embedding(n_char, cdim, mask_zero=False)(in2)
    cemb1 = TimeDistributed(Bidirectional(LSTM(cdim)))(cemb1)
    remb1 = Embedding(2, rdim, mask_zero=False)(in3)
    out = Concatenate()([wemb1, cemb1, remb1])
    out = Dropout(0.5)(out)
    out = SeparableConv1D(32, kernel_size=3, padding="same",
                          activation="relu")(out)
    out1 = GlobalAvgPool1D()(out)
    out2 = GlobalMaxPool1D()(out)
    out = Concatenate()([out1, out2])

    x3 = Dense(512, activation="relu")(in5)
    x4 = Dense(1, activation="relu")(in6)

    out = Dense(512, activation="relu")(out)
    out = Concatenate()([out, x3])
    out = Dense(512, activation="relu")(out)
    out = Concatenate()([out, x4])
    out = Dense(512, activation="relu")(out)
    out = Dropout(0.5)(out)
    out = Dense(1, activation="sigmoid")(out)
    model = Model([in1, in2, in3, in5, in6], out)
    model.compile(optimizer="nadam",
                  loss="binary_crossentropy",
                  metrics=["acc"])
    return model


def run(lang):
    n_words = 3000000
    n_chars = 256
    trie, kv, embedding_dict, embedding_matrix = load_data_general(n_words,
                                                                   lang=lang)
    pdata = (trie, kv, embedding_dict)
    callbacks = [ModelCheckpoint("./model_wiki_{}.h5".format(lang))]
    model = build_model(embedding_matrix, n_words, n_chars)
    model.fit_generator(generate_wiki(
        "../wiki_processor/data/training_data/ELdata_wiki_{}.txt".format(lang),
        *pdata),
                        steps_per_epoch=10,
                        epochs=1000,
                        callbacks=callbacks)


def is_exist_nessesary_files(langs):
    import os
    flag = True
    paths = [
        "../wiki_processor/data/training_data/ELdata_wiki_{}.txt",
        "../wiki_processor/entity_vectors/{}wiki_20180420_100d.bin",
        "../wiki_processor/data/w2v_models/word2vec_{}.model",
        "../wiki_processor/data/marisa_data/mention_stat_{}.marisa"
    ]
    for lang in langs:
        for path in paths:
            flag = flag and os.path.isfile(path.format(lang))
    return flag


if __name__ == "__main__":
    import sys
    import time
    langs = ["de", "it", "es", "fr", "en"]

    counter = 0
    while not is_exist_nessesary_files(langs):
        sys.stdout.write("waiting...[{}]\r".format(counter))
        sys.stdout.flush()
        counter += 1
        time.sleep(1)
    for lang in langs:
        run(lang)
