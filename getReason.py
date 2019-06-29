from nltk.tree import ParentedTree
import re
from TimeNLP import TimeNormalizer


def traverse_remains(t):
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
    final_result = []
    for tree in trees:
        # tree.pretty_print()
        sentence = "".join(tree.leaves())
        if '@' in sentence:
            continue
        if contain_approver(tree):
            # trees.remove(tree)
            continue
        if contain_type(sentence):
            # trees.remove(tree)
            continue
        # pos, _ = tn.parse(sentence)
        matchObj = re.match(r'(.*)请(.*)假(.*)', sentence)
        if matchObj is not None:
            sentence = sentence[: matchObj.pos] + sentence[matchObj.endpos:]
            if sentence == "":
                continue
            else:
                tree = ParentedTree.fromstring(sentence)
            # 判断是否有其他动词
            current_tree = tree
            traverse(current_tree, current_tree)
            # vp = "".join(current_tree.leaves())
            # trees.remove(tree)
            if len(current_tree.leaves()) > 0:
                cnt = 0
                for i in range(len(current_tree.leaves())):
                    if current_tree.leaves()[i] != "要" and current_tree.leaves()[i] != "想" and current_tree.leaves()[i] != "准备" and current_tree.leaves()[i] != "打算":
                        final_result.append(current_tree.leaves()[i])
                        cnt = cnt + 1
                if cnt > 0:
                    final_result.append(" ")
            continue
        else:
            temp = traverse_remains(tree)
            if len(temp) > 0:
                cnt = 0
                for i in range(len(temp)):
                    if temp[i] != "要" and temp[i] != "想" and temp[i] != "准备" and temp[i] != "打算":
                        final_result.append(temp[i])
                        cnt = cnt + 1
                if cnt > 0:
                    final_result.append(" ")
    reason.extend(trees)
    return final_result


def preprocess(sentence):
    try:
        sentence = sentence.replace("请个假", "请假")
        tn = TimeNormalizer()
        pos, _ = tn.parse(sentence)
        if len(pos) > 0:
            l = [x for y in pos for x in y]
            a, b = min(l), max(l)
            if a > 0 and sentence[a - 1] == "从":
                a = a - 1
            sentence = sentence[: a] + sentence[b:]

            # for i in range(len(pos) - 1, -1, -1):
            #     for j in range(pos[i][1] - 1, pos[i][0] - 1, -1):
            #         sentence = sentence[:j] + sentence[j + 1:]
        cutspan = re.match(r'(.*?)请(.*?)假(.*?)(日?|天?|月?|年?|周?|小时?)', sentence).span()
        sentence = sentence[0:cutspan[0]] + "请假" + sentence[cutspan[1]:len(sentence)]
        return sentence
    except:
        return sentence


def get_reason(sentence, nlp):
    processed = preprocess(sentence)
    if len(processed) != 0:
        splits = re.compile("[,，。,]").split(processed)
        results = [nlp.parse(s) for s in splits if s != ""]
        trees = [ParentedTree.fromstring(result) for result in results]
        final_result = find_reason(trees)
        # print(final_result)
        if len(final_result) != 0:
            return "".join(final_result)
    return None


