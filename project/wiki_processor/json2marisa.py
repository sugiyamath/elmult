import json
import sys
from marisa_trie import BytesTrie

if __name__ == "__main__":
    lang = sys.argv[1]
    print("load mention_stat")
    with open("./mention_stat_{}.json".format(lang)) as f:
        data = json.load(f)

    print("mention_stat to trie")
    trie = BytesTrie([(k, bytes(json.dumps(v), "utf-8"))
                      for k, v in data.items()])

    print("saving...")
    trie.save("mention_stat_{}.marisa".format(lang))

    print("Done!")
