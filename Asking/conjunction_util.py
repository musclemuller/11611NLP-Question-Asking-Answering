from tag import *
import re

np_tree = None
vp_tree = None

def simplify_conjunction(tree):
    tree = tree.children[0]
    if tree.label != SENTENCE:
        return []
    if len(tree.children) < 3:
        return []
    np_true = False
    vp_true = False
    #look for np and vp structure
    for child in tree.children:
        if child.label == NP:
            np_true = True
            np_tree = child
        if child.label == VP:
            vp_children = child.children
            vp_tree = child
            vp_true = True
    if not np_true or not vp_true:
        return []
    #look for #VP,VP,CC,VP
              #VP,CC,VP
    check_str = "" #a string for checking
    for child in vp_children:
        check_str = check_str + child.label
    result = re.search("VP(,VP)?CCVP", check_str)
    if result is None:
        return []

    sentences = []
    sen = []
    if np_tree and vp_tree:
        np_tree.children[0].visit_preorder(leaf=lambda x: sen.append(x.label))
        for child in vp_tree.children:
            leaf = []
            if child.label == VP:
                find_leaves(child, leaf)
                sentences.append(sen + leaf)
    return form_strings(sentences)

def find_leaves(tree, leaf):
    if tree is not None:
        if len(tree.children) == 0:
            leaf.append(tree.label)
        for child in tree.children:
            find_leaves(child, leaf)

def form_strings(sentences):
    strings = []
    for line in sentences:
        str = ""
        for i,word in enumerate(line):
            if i < len(line) - 1 and line[i+1] == ")":
                str += word
            elif i < len(line) - 1 and line[i+1] == ",":
                str += word
            elif word == '(' or word == ')':
                str += word
            else:
                str = str + word + " "
        s = str.strip()
        s = s + "."
        s.capitalize()
        strings.append(s)
    #print(strings)
    return strings