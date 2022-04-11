#pytimport os
import stanza
import sentences_generating
import conjunction_util
from tag import *

def parse_tree(sentences):
    #stanza.download(lang='en', processors='mwt,lemma,depparse')
    nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency,mwt,lemma,depparse')

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

    #     if apposition.matched(tree):
    #         sentences.remove(sentence)
    #         #todo: generate two sentences
    #         sentences += apposition.split_apposition(tree.children[0])


    # trees = []
    # for doc in out_docs:
    #     #print(doc.sentences[0].constituency)
    #     trees.append(doc.sentences[0].constituency)
    # return trees
    return sentences


if __name__ == "__main__":
    text = "Dempsey first represented the United States at the 2003 FIFA World Youth Championship and made his first appearance with the senior team on November 17, 2004, against Jamaica. " \
           "He has earned over 100 caps and scored 48 international goals, making him the nation's sixth-most capped player and second top scorer of all time. " \
           "He has represented the nation at four CONCACAF Gold Cups (winning two), helped them to the final of the 2009 FIFA Confederations Cup and played at three FIFA World Cups, becoming the first American male to score in three World Cups."
    sentences = sentences_generating.do_segementation(text)
    trees = parse_tree(sentences)
    for sentence in sentences:
       print(sentence)
    #find_apposition(trees)
