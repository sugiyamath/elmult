from gensim.models import KeyedVectors

if __name__ == "__main__":
    import sys
    import os
    lang = sys.argv[1]
    rootpath = "./entity_vectors"
    filepath = "{}wiki_20180420_100d.txt".format(lang)
    targetpath = os.path.join(rootpath, filepath) 
    print("loading...")
    model = KeyedVectors.load_word2vec_format(
        targetpath, binary=False)
    print("saving...")
    model.save("{}wiki_20180420_100d.bin".format(lang))
    print("Done!")
