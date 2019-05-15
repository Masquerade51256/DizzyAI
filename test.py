from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import Tree, ParentedTree
import time
import logging


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


def find_reason(t):
    np_trees = []
    traverse(t, np_trees)
    print(np_trees)


print("请输入")
print(time.asctime(time.localtime(time.time())))
with StanfordCoreNLP(r'D:\corenlp\stanford-corenlp-full-2018-10-05', lang='zh', memory='4g', timeout=1500, quiet=True, logging_level=logging.INFO) as nlp:
    print(time.asctime(time.localtime(time.time())))
    while True:
        sentence = input()
        result = nlp.parse(sentence)
        print(result)
        parsetree = Tree.fromstring(result)
        parsetree.pretty_print()
        print(parsetree.leaves())

        tree = ParentedTree.fromstring(result)
        find_reason(tree)
        # print(find_vp)

