import os
import stanza
from tag import *

APPOSITION = (SENTENCE, ((NP, (NP, COMMA, NP, COMMA)), VP, PERIOD))

def parse_tree(sentences):
    # stanza.download(lang='en', processors='tokenize,pos,constituency')
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')
    # doc = nlp("Bill Gates, a brilliant entrepreneur, owns Microsoft.")
    # tree = doc.sentences[0].constituency
    # print(tree)
    # constituents = []
    # tree.visit_preorder(internal=lambda x: constituents.append(x.label))
    # print(constituents)
    # return constituents
    # in_docs = [stanza.Document([], text=d) for d in sentences]
    # out_docs = nlp(in_docs)
    # print(out_docs)
    for i in range(len(sentences)):
        sentence = sentences[i]
        doc = nlp(sentence)
        tree = doc.sentences[0].constituency
        print(tree)
        if matched(tree):
            sentences.remove(sentence)
            #todo: generate two sentences
            sentences += split_apposition(tree.children[0])


    # trees = []
    # for doc in out_docs:
    #     #print(doc.sentences[0].constituency)
    #     trees.append(doc.sentences[0].constituency)
    # return trees


def split_apposition(tree):
    two_sentences = []
    np1 = []
    tree.children[0].children[0].visit_preorder(leaf=lambda x: np1.append(x.label))
    np2 = []
    tree.children[0].children[2].visit_preorder(leaf=lambda x: np2.append(x.label))
    vp = []
    tree.children[1].visit_preorder(leaf=lambda x: vp.append(x.label))
    two_sentences.append(combine_two_sentences(np1, vp))
    two_sentences.append(combine_two_sentences(np2, vp))
    return two_sentences

def combine_two_sentences(np, vp):
    str1 = ' '.join(np)
    str2 = ' '.join(vp)
    str = str1 + ' ' + str2
    #todo: cappital letter
    str = str.capitalize()
    return str



def matched(tree):
    tree = tree.children[0]
    if tree.label != SENTENCE:
        print("tree.label: " + tree.label)
        return False
    if len(tree.children) != 3:
        return False
    tree0 = tree.children[0]
    if tree0.label != NP:
        print("tree0.label: " + tree0.label)
        return False
    tree1 = tree.children[1]
    if tree1.label != VP:
        print("tree1.label: " + tree1.label)
        return False
    tree2 = tree.children[2]
    if tree2.label != PERIOD:
        print("tree2.label: " + tree2.label)
        return False
    if len(tree0.children) != 4:
        return False

    tree00 = tree0.children[0]
    if tree00.label != NP:
        print("tree00.label: " + tree00.label)
        return False
    tree01 = tree0.children[1]
    if tree01.label != COMMA:
        print("tree01.label: " + tree01.label)
        return False
    tree02 = tree0.children[2]
    if tree02.label != NP:
        print("tree02.label: " + tree02.label)
        return False
    tree03 = tree0.children[3]
    if tree03.label != COMMA:
        print("tree03.label: " + tree03.label)
        return False
    return True


if __name__ == "__main__":
    #sentences = ["Bill Gates, a brilliant entrepreneur, owns Microsoft."]
    sentences = ["Dempsey played for one of the top youth soccer clubs in the state, the Dallas Texans, "
                 "before playing for Furman University's men's soccer team."]
    trees = parse_tree(sentences)
    for sentence in sentences:
        print(sentence)
    #find_apposition(trees)
