# coding: utf-8
from pynif import NIFCollection
import json


def nif2dict(nif):
    out = []
    for context in nif.contexts:
        if context.mention is None:
            continue
        tmp = {"sentence": context.mention, "entities": []}
        for phrase in context.phrases:
            try:
                tmp["entities"].append(
                    {
                        "entity": phrase.taIdentRef,
                        "begin": phrase.beginIndex,
                        "end": phrase.endIndex
                    }
                )
            except:
                continue

        if tmp["entities"]:
            out.append(tmp)
    return out


def nif2json(lang="en"):
    paths = ["./VoxEL/rVoxEL-{}.ttl", "./VoxEL/sVoxEL-{}.ttl"]
    prefix = ["r", "s"]

    for path, p in zip(paths, prefix):
        with open(path.format(lang)) as f:
            data = NIFCollection.loads(f.read(), format='turtle')
        out = nif2dict(data)
        with open("./{}_{}.json".format(p, lang), "w") as f:
            json.dump(out, f, indent=4)


def run(langs=["en", "de", "es", "fr", "it"]):
    for lang in langs:
        nif2json(lang)


if __name__ == "__main__":
    run()
