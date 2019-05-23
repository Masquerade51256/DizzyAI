from stanfordcorenlp import StanfordCoreNLP
from nltk.tree import ParentedTree
import re
from TimeNLP import TimeNormalizer

# current_tree = []


def traverse_remains(t):
    # t.pretty_print()
    np_trees = []
    find_remains_vp(t, np_trees)
    return np_trees


def find_remains_vp(t, np_trees):
    find_vp = []
    try:
        t.label()
    except AttributeError:
        return

    if t.label() == "VV" or t.label() == 'VP' or t.label() == 'VCD' or t.label() == 'VCP' or t.label() == 'VNV' or t.label() == 'VPT' or t.label() == 'VRD' or t.label() == 'VSB':
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
        find_remains_vp(child, np_trees)


def ip_del(item, current_tree):
    for child in reversed(item):
        if child.label() == 'IP':
            ip_del(child, current_tree)
        else:
            if child.label() != 'VP' and child.label() != 'VV' and child.label() != 'VCD' and child.label() != 'VCP' and child.label() != 'VNV' and child.label() != 'VPT' and child.label() != 'VRD' and child.label() != 'VSB':
                del current_tree[child.treeposition()]


def not_vp(temp, current_tree):
    for item in reversed(temp):
        if item.label() == 'IP':
            ip_del(item, current_tree)
        else:
            if item.label() != 'VP' and item.label() != 'VV' and item.label() != 'VCD' and item.label() != 'VCP' and item.label() != 'VNV' and item.label() != 'VPT' and item.label() != 'VRD' and item.label() != 'VSB':
                del current_tree[item.treeposition()]
    if temp.parent().label() != 'ROOT':
        temp = temp.parent()
        not_vp(temp, current_tree)


def traverse(t, current_tree):
    for child in t:
        if type(child) == str:
            if str(child) == "请假":
                temp = t.parent()
                del current_tree[t.treeposition()]
                not_vp(temp, current_tree)
            return
        else:
            traverse(child, current_tree)


def contain_approver(tree):
    return True if "批" in tree.leaves() else False


def contain_type(sentence):
    return True if re.match(r'(.*)[事病](.*?)假(.*).*', sentence) is not None else False


def find_reason(trees):
    reason = []
    tn = TimeNormalizer()
    vp = ""
    final_result = []
    for tree in trees:
        sentence = "".join(tree.leaves())
        if contain_approver(tree):
            # trees.remove(tree)
            continue
        if contain_type(sentence):
            # trees.remove(tree)
            continue
        # pos, _ = tn.parse(sentence)
        # if len(pos) > 0:
        #     print(pos)
        if re.match(r'(.*)请(.*?)假(.*).*', sentence) is not None:
            # 判断是否有其他动词
            current_tree = tree
            # current_tree.pretty_print()
            not_list = []
            pos_list = []
            traverse(current_tree, current_tree)
            # current_tree.pretty_print()
            # vp = "".join(current_tree.leaves())
            # trees.remove(tree)
            for i in range(len(current_tree.leaves())):
                final_result.append(current_tree.leaves()[i])
            final_result.append(" ")
            continue
        else:
            temp = traverse_remains(tree)
            if len(temp) > 0:
                for i in range(len(temp)):
                    final_result.append(temp[i])
                final_result.append(" ")
    reason.extend(trees)
    return final_result


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
            final_result = find_reason(trees)
            output = "".join(final_result)
            print(output)


main()

