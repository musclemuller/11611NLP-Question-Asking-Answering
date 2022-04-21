from tag import *
from Asking import apposition_util
from Asking import models
import logging

APPOSITION = (SENTENCE, ((NP, (NP, COMMA, NP, COMMA)), VP, PERIOD))

def parse_tree(sentences):
    # stanza.download(lang='en', processors='tokenize,pos,constituency')
    # logger = logging.getLogger('stanza')
    # logger.disabled = True
    # nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')
    nlp = models.stanza_nlp
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
        # print(tree)
        if apposition_util.matched(tree):
            sentences.remove(sentence)
            sentences += apposition_util.split_apposition(tree.children[0])
    # logger.disabled = False
    return sentences
    # trees = []
    # for doc in out_docs:
    #     #print(doc.sentences[0].constituency)
    #     trees.append(doc.sentences[0].constituency)
    # return trees


if __name__ == "__main__":
    sentences = ["Fulham became another American addition to a Cottagers' squad which included US internationals Brian McBride and Carlos Bocanegra"]
    #sentences = ["Dempsey played for one of the top youth soccer clubs in the state, the Dallas Texans, "
    #             "before playing for Furman University's men's soccer team."]
    trees = parse_tree(sentences)
    for sentence in sentences:
        print(sentence)
    #find_apposition(trees)
