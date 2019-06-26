import json
from tqdm import tqdm
from cand2en import cand2en

if __name__ == "__main__":
    import sys
    filepath = sys.argv[1]

    trie = BytesTrie()
    trie.load("./id2title.marisa")

    with open(filepath) as f:
        data = json.load(f)
    recalls = []
    precisions = []

    for sent in tqdm(data):
        true_in_pred = 0
        pred_in_true = 0
        if len(sent["pred"]) == 0 or len(sent["true"]) == 0:
            continue
        sent["true"] = list({x["entity"].split("/")[-1] for x in sent["true"]})
        sent["pred"] = list({x["entity"] for x in sent["pred"]})
        
        sent["true"] = [
            cand2en(cand, trie) for cand in sent["true"]
            if cand2en(cand, trie) is not None
        ]

        sent["pred"] = [
            cand2en(cand, trie) for cand in sent["pred"]
            if cand2en(cand, trie) is not None
        ]

        if not sent["true"] or not sent["pred"]:
            continue
        
        for e in sent["true"]:
            if e in sent["pred"]:
                true_in_pred += 1
        precisions.append(float(true_in_pred) / float(len(sent["pred"])))
        for e in sent["pred"]:
            if e in sent["true"]:
                pred_in_true += 1
        recalls.append(float(pred_in_true) / float(len(sent["true"])))
    recall = sum(recalls) / len(recalls)
    precision = sum(precisions) / len(precisions)
    f1 = (2 * precision * recall) / (precision + recall)

    print("recall:", recall)
    print("precision:", precision)
    print("f1:", f1)
