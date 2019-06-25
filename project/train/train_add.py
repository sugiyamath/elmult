from data_generator import load_data3, generate_aida
from keras.callbacks import ModelCheckpoint
from keras.models import load_model


def run():
    trie, kv, embedding_dict, _ = load_data3(3000000)
    pdata = (trie, kv, embedding_dict)
    callbacks = [
        ModelCheckpoint("./model_aida_wiki_best.h5")
    ]
    model = load_model("./model_wiki.h5")
    model.fit_generator(generate_aida("./data.json", *pdata),
                        steps_per_epoch=300,
                        epochs=50,
                        callbacks=callbacks)


if __name__ == "__main__":
    run()
