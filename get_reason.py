from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree

current_tree = []


def ip_del(item, not_list, pos_list):
    global current_tree
    for child in reversed(item):
        if child.label() == 'IP':
            print("IP ha ha")
            ip_del(child, not_list, pos_list)
        else:
            if child.label() != 'VP' and child.label() != 'VV' and child.label() != 'VCD' and child.label() != 'VCP' and child.label() != 'VNV' and child.label() != 'VPT' and child.label() != 'VRD' and child.label() != 'VSB':
                not_list.append(child)
                pos_list.append(child.treeposition())
                del current_tree[child.treeposition()]


def not_vp(temp, not_list, pos_list):
    global current_tree
    for item in reversed(temp):
        if item.label() == 'IP':
            print("IP ha")
            ip_del(item, not_list, pos_list)
        else:
            if item.label() != 'VP' and item.label() != 'VV' and item.label() != 'VCD' and item.label() != 'VCP' and item.label() != 'VNV' and item.label() != 'VPT' and item.label() != 'VRD' and item.label() != 'VSB':
                not_list.append(item)
                pos_list.append(item.treeposition())
                del current_tree[item.treeposition()]
    if temp.parent().label() != 'ROOT':
        temp = temp.parent()
        not_vp(temp, not_list, pos_list)


def traverse(t, not_list, pos_list):
    global current_tree
    for child in t:
        if type(child) == str:
            if str(child) == "请假":
                pos_list.append(t.treeposition())
                not_list.append(child)
                temp = t.parent()
                del current_tree[t.treeposition()]
                not_vp(temp, not_list, pos_list)
            return
        else:
            traverse(child, not_list, pos_list)


def contain_approver(tree):
    return True if "批" in tree.leaves() else False


def contain_type(sentence):
    return True if re.match(r'(.*)[事病](.*?)假(.*).*', sentence) is not None else False


def find_reason(trees):
    global current_tree
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
        if len(pos) > 0:
            print(pos)
            if re.match(r'(.*)请(.*?)假(.*).*', sentence) is not None:
                # 判断是否有其他动词
                current_tree = tree
                current_tree.pretty_print()
                print(sentence)
                not_list = []
                pos_list = []
                traverse(current_tree, not_list, pos_list)
                current_tree.pretty_print()
                # print(current_tree.leaves())
                vp = "".join(current_tree.leaves())
                print(vp)
                if len(vp) == 0:
                    print("您的请假理由是？")
    reason.extend(trees)
    return reason


def preprocess(sentence):
    sentence = sentence.replace("请个假", "请假")
    return sentence


def main():
    with StanfordCoreNLP(r'D:\corenlp\stanford-corenlp-full-2018-10-05', lang='zh', memory='4g', quiet=True,) as nlp:
        nlp.parse("test")
        while True:
            print("请输入")
            sentence = input()
            sentence = preprocess(sentence)
            splits = re.compile("[,，。,]").split(sentence)
            results = [nlp.parse(s) for s in splits]

            trees = [ParentedTree.fromstring(result) for result in results]
            # for tree in trees:
            #     tree.pretty_print()
            find_reason(trees)
            # reason = find_reason(trees)
            # print(reason)


import re
from TimeNLP import TimeNormalizer
main()
