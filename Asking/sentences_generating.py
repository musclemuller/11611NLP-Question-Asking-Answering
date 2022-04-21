import string
import re

import nltk
<<<<<<< Updated upstream
import spacy
import utils


def do_segementation(input_text):
=======
from Asking import utils
from Asking import models
import logging

def do_segementation(input_text):
    logger1 = logging.getLogger('nltk')
    logger1.disabled = True
>>>>>>> Stashed changes
    store = nltk.sent_tokenize(input_text, language='english')
    store = deal_whitespace(store)

    pronouns = {"He", "She", "It"}
    pos_pronouns = {"His", "Her", "Its"}
    subject = ""
    pronoun = ""
<<<<<<< Updated upstream
    nlp = spacy.load("en_core_web_trf")
=======
    nlp = models.spacy_nlp
>>>>>>> Stashed changes

    for i in range(len(store)):
        sentence = store[i]
        sentence = sentence.strip()
        doc = nlp(sentence)
        for word in doc:
            if word.dep_ == "nsubj":
                if (word.text in pronouns) and (subject != ""):
                    pronoun = word.text
                    subject = subject.replace("'s", "")
                    break
                else:
                    pronoun = ""
                    subject = word.text
                    break
            if word.dep_ == "poss":
                if (word.text in pos_pronouns) and (subject != ""):
                    pronoun = word.text
                    subject = subject + "'s"
                    break
        if pronoun != "" and subject != "":
            store[i] = sentence.replace(pronoun, subject)
    store.sort(key=lambda i: len(i))
    store = [s for s in store if s.count(' ') < 50]
    return store


def deal_whitespace(store):
    article = []
    for sentence in store:
        if "\r" in sentence or "\n" in sentence or "\t" in sentence:
            sentence = sentence.replace('\r', '.').replace('\n', '.').replace('\t', '.')
            sentence = re.sub("\.+", ".", sentence)
            for parts in sentence.split("."):
                parts = parts + "."
                if parts == ".":
                    continue
                article.append(parts)
        elif sentence[len(sentence)-1] != string.punctuation:
            sentence = sentence.replace('\r', '.').replace('\n', '.').replace('\t', '.')
            if sentence == ".":
                continue;
            article.append(sentence)
        else:
            article.append(sentence)
    return article

# Main program
if __name__ == "__main__":
<<<<<<< Updated upstream
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"
    input_text = utils.read_input_file(filename)
    store = do_segementation(input_text)
=======
    # filename = "../data/set1/a1.txt"
    # input_text = utils.read_input_file(filename)
    # store = do_segementation(input_text)
>>>>>>> Stashed changes

    sentences = "Before moving to Fulham, Dempsey went for a trial at ŁKS Łomża where the coach sent him to Fulham. In December 2006, English club Fulham offered MLS $4 million for the transfer of Dempsey, then the largest amount ever offered for an MLS player, and he became another American addition to a Cottagers' squad which included US internationals Brian McBride and Carlos Bocanegra. On January 11, 2007, he was granted a work permit from the Home Office as Fulham announced his signing on a long-term deal."
    store = do_segementation(sentences)
    print(store)

    # output_file = "../sentences/set1_a1.txt"
    # utils.write_output_file(output_file, store)
