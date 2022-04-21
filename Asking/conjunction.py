#pytimport os
import stanza
<<<<<<< Updated upstream
import sentences_generating
import conjunction_util
from tag import *

def parse_tree(sentences):
    #stanza.download(lang='en', processors='mwt,lemma,depparse')
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency,mwt,lemma,depparse')
=======
from Asking import sentences_generating
from Asking import conjunction_util
from Asking import models

def parse_tree(sentences):
    #stanza.download(lang='en', processors='mwt,lemma,depparse')
    nlp = models.stanza_nlp
>>>>>>> Stashed changes

    for i in range(len(sentences)):
        sentence = sentences[i]
        doc = nlp(sentence)
        tree = doc.sentences[0].constituency
        #print(tree)
        simplified = conjunction_util.simplify_conjunction(tree)
        if len(simplified) != 0:
            sentences.remove(sentence)
            for line in simplified:
                sentences.append(line);

<<<<<<< Updated upstream
    #     if apposition.matched(tree):
    #         sentences.remove(sentence)
    #         #todo: generate two sentences
    #         sentences += apposition.split_apposition(tree.children[0])


    # trees = []
    # for doc in out_docs:
    #     #print(doc.sentences[0].constituency)
    #     trees.append(doc.sentences[0].constituency)
    # return trees
=======
>>>>>>> Stashed changes
    return sentences


if __name__ == "__main__":
    text = "Fulham became another American addition to a Cottagers' squad which included US internationals Brian McBride and Carlos Bocanegra."
    sentences = sentences_generating.do_segementation(text)
    trees = parse_tree(sentences)
    for sentence in sentences:
       print(sentence)
    #find_apposition(trees)
