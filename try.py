from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree

tree = []


def ip_del(item, not_list, pos_list):
    global tree
    for child in reversed(item):
        if child.label() == 'IP':
            print("IP ha ha")
            ip_del(child, not_list, pos_list)
        else:
            if child.label() != 'VP' and child.label() != 'VV' and child.label() != 'VCD' and child.label() != 'VCP' and child.label() != 'VNV' and child.label() != 'VPT' and child.label() != 'VRD' and child.label() != 'VSB':
                not_list.append(child)
                pos_list.append(child.treeposition())
                del tree[child.treeposition()]


def not_vp(temp, not_list, pos_list):
    global tree
    for item in reversed(temp):
        if item.label() == 'IP':
            print("IP ha")
            ip_del(item, not_list, pos_list)
        else:
            if item.label() != 'VP' and item.label() != 'VV' and item.label() != 'VCD' and item.label() != 'VCP' and item.label() != 'VNV' and item.label() != 'VPT' and item.label() != 'VRD' and item.label() != 'VSB':
                not_list.append(item)
                pos_list.append(item.treeposition())
                del tree[item.treeposition()]
    if temp.parent().label() != 'ROOT':
        temp = temp.parent()
        not_vp(temp, not_list, pos_list)


def traverse(t, not_list, pos_list):
    global tree
    for child in t:
        if type(child) == str:
            if str(child) == "请假":
                pos_list.append(t.treeposition())
                not_list.append(child)
                temp = t.parent()
                del tree[t.treeposition()]
                not_vp(temp, not_list, pos_list)
            return
        else:
            traverse(child, not_list, pos_list)


def main():
    global tree
    with StanfordCoreNLP(r'D:\corenlp\stanford-corenlp-full-2018-10-05', lang='zh', memory='4g', quiet=True,) as nlp:
        nlp.parse("test")
        while True:
            print("请输入")
            sentence = input()
            result = nlp.parse(sentence)
            tree = ParentedTree.fromstring(result)
            tree.pretty_print()
            not_list = []
            pos_list = []

            traverse(tree, not_list, pos_list)
            tree.pretty_print()
            print(tree.leaves())
            # print(not_list)
            # print(pos_list)


main()
