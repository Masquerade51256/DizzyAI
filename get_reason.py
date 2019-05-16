from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree

def traverse(t, np_trees):
    find_vp = []
    try:
        t.label()
    except AttributeError:
        return

    if t.label() == "VP":
        current = t
        for i in range(len(t.leaves())):
            find_vp.append(t.leaves()[i])
        while current.parent() is not None:

            while current.left_sibling() is not None:

                if current.left_sibling().label() == "NP":
                    for i in range(len(current.left_sibling().leaves())):
                        np_trees.append(current.left_sibling().leaves()[i])
                    for i in range(len(find_vp)):
                        np_trees.append(find_vp[i])
                    break
            current = current.left_sibling()

            current = current.parent()
        # 没有np时
        if len(np_trees) == 0:
            for i in range(len(find_vp)):
                np_trees.append(find_vp[i])
        return
    for child in t:
        traverse(child, np_trees)

def contain_approver(tree):
    return True if "批" in tree.leaves() else False

def contain_type(sentence):
    return True if re.match(r'(.*)[事病](.*?)假(.*).*', sentence) is not None else False

def find_reason(trees):
    reason = []
    tn = TimeNormalizer()
    for tree in trees:
        sentence = "".join(tree.leaves())
        if contain_approver(tree):
            trees.remove(tree)
            continue
        if contain_type(sentence):
            trees.remove(tree)
            continue
        pos, _ = tn.parse(sentence)
        print(pos)
        if re.match(r'(.*)请(.*?)假(.*).*', sentence) is not None:
            # 判断是否有其他动词
            print(sentence)
    reason.extend(trees)
    return reason

def preprocess(sentence):
    sentence = sentence.replace("请个假", "请假")
    return sentence

def main():
    with StanfordCoreNLP(r'E:\stanford-corenlp-full-2018-10-05', lang='zh', memory='4g', quiet=True,) as nlp:
        nlp.parse("test")
        while True:
            print("请输入")
            sentence = input()
            sentence = preprocess(sentence)
            splits = re.compile("[,，。,]").split(sentence)
            results = [nlp.parse(s) for s in splits]

            trees = [ParentedTree.fromstring(result) for result in results]
            for tree in trees:
                tree.pretty_print()

            reason = find_reason(trees)
            print(reason)

import re
from TimeNLP import TimeNormalizer
main()
