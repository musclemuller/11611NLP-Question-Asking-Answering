import string
import logging

from tag import *
from Asking import models
from Asking import conjunction_util


def match_npvp(tree):
    tree = tree.children[0]
    if tree.label != SENTENCE:
        return False
    if len(tree.children) != 3:
        return False
    # look for np and vp structure
    if tree.children[0].label != NP:
        return False
    if tree.children[1].label != VP:
        return False
    return True

def match_ppnpvp(tree):
    tree = tree.children[0]
    if tree.label != SENTENCE:
        return False
    # tree with structure pp , np vp .
    if len(tree.children) != 5:
        return False
    # see if the tree matches the structure
    if tree.children[0].label != PP:
        return False
    if tree.children[1].label != ",":
        return False
    if tree.children[2].label != NP:
        return False
    if tree.children[3].label != VP:
        return False
    return True


def binary_questions(doc, line):
    question = ""
    words = doc.sentences[0].words
    spacy_nlp = models.spacy_nlp
    spacy_doc = spacy_nlp(line)
    root = return_root(spacy_doc).text
    for i, word in enumerate(words):
        if word.deprel == "aux" and words[i+1].text == root: # if sentence contains aux verbs, use different method
            return front_binary_quesitons(doc)
        elif word.text == "are":
            return front_binary_quesitons(doc)
        elif word.xpos == "VBP" and word.text == root:
            question = "do " + question
            question = question + word.lemma + " "
        elif word.xpos == "VBZ" and word.text == "is":
            return front_binary_quesitons(doc)
        elif word.xpos == "VBZ" and word.text == root:
            question = "does " + question
            question = question + word.lemma + " "
        elif word.text == "were" or word.text == "was":
            return front_binary_quesitons(doc)
        elif word.xpos == "VBD" and word.text == root:
            question = "did " + question
            question = question + word.lemma + " "
        elif word.xpos == ".":
            break;
        elif i < len(words)-1 and words[i+1].text in string.punctuation:
            question = question + word.text
        elif i < len(words)-1 and words[i+1].text == "'s":
            question = question + word.text
        else:
            question = question + word.text + " "

    return question



def return_root(doc):
    for token in doc:
        if token.dep_ == "ROOT":
            return token

def front_binary_quesitons(doc):
    question = ""
    for word in doc.sentences[0].words:
        if word.deprel == "aux" or word.text == "is" or word.text == "was" or word.text == "were"\
                or word.text == "are":
            question = word.text + " " + question
        elif word.xpos == ".":
            break;
        elif word.lemma == "not": # skip the not
            continue;
        else:
            question = question + word.text + " "

    return question

def ner_questions(doc, sentence):
    # spacy_doc = models.spacy_nlp(sentence)
    questions = []
    try:
        ents = {}
        for ent in doc.sentences[0].ents:
            ents[ent.text] = ent.type

        base = binary_questions(doc, sentence)
        words = []
        for word in doc.sentences[0].words:
            words.append(word.text)
        # loop through ents
        for ent in ents.keys():
            # get the corresponding what, why, who from ent
            wh = get_wh(ents[ent])
            if wh is None:
                continue
            # if the sentence starts with an ent, simply delete the ent and replace it with wh
            if sentence.startswith(ent):
                temp = sentence.replace(ent, "")  # remove the first ent
                question = wh + temp
                questions.append(format_question(question))
            else:
                # format the sentence in the structure of wh + base formate from binary question
                question = wh + " " + base
                # question = find_clause(ent, spacy_doc, question)
                before = sentence.partition(ent)[0]
                prev_words = before.split()
                prev_word = prev_words[len(prev_words)-1]
                # prev_index = words.index(ent.split()[0]) - 1
                # prev_word = words[prev_index]
                prev_index = -1;
                for i, w in enumerate(words):
                    if w == prev_word:
                        if i < len(words) -1 and words[i+1] == ent.split()[0]:
                            prev_index = i
                if prev_index != -1 and doc.sentences[0].words[prev_index].deprel == "case" and prev_word != "with":
                    question = question.replace(prev_word + " " + ent, "")
                else:
                    question = question.replace(ent, "", 1)
                questions.append(format_question(question))
    except:
        return []
    return questions
#
# def find_clause(ent, doc, question):
#     try:
#         head = None
#         target = None
#         for token in doc:
#             if token.text == ent:
#                 head = token.head
#                 target = token
#                 break;
#     except:
#         return question.replace(ent, "", 1)
#
#     if head is not None and target is not None:
#         print(head.text)
#         clause = doc[head.i:target.i]
#         print("clause: " + clause.text)
#         question = question.replace(clause.text, "")
#         return question
#     else:
#         return question.replace(ent, "", 1)



def get_wh(ent):
    if ent == "PERSON":
        return "who"
    if ent == "GPE":
        return "where"
    if ent == "LOCATION":
        return "where"
    if ent == "DATE":
        return "when"
    if ent == "TIME":
        return "when"

def why_questions(doc, line):
    question = binary_questions(doc, line)
    question = "Why " + question
    return format_question(question)


def format_question(question):
    str = question.rstrip(".")
    str = str.strip()
    str = str.replace("  ", " ")
    str = str[0].upper() + str[1:len(str)]
    # remove white spaces before punctuation
    words = str.split()
    q = ""
    for i, word in enumerate(words):

        if i < len(words) - 1 and ((words[i + 1] in string.punctuation or word == "-" or word == "–" or words[i+1] == "'s") and
                                   (words[i + 1] != "(")):
            if word != " ":
                q += word
        elif word == '(' or word == "-" or word == "–":
            q += word
        else:
            q += word + " "
    q = q.strip()
    q = q + "?"
    return q

def simplify_sentence(tree):
    tree = tree.children[0]
    words = []
    sentence = ""
    for child in tree.children[2:]:
        leaf = []
        conjunction_util.find_leaves(child, leaf)
        words.extend(leaf)
    for i, word in enumerate(words):
        if i < len(words) - 1 and words[i + 1] in string.punctuation:
            sentence = sentence + word
        elif i < len(words) - 1 and words[i + 1] == "'s":
            sentence = sentence + word
        else:
            sentence = sentence + word + " "
    return sentence


def generating(sentences):
    logger = logging.getLogger()
    logger.disabled = True
    nlp = models.stanza_nlp
    binary = []
    wh = []

    for line in sentences:
        doc = nlp(line)
        tree = doc.sentences[0].constituency
        ents = []
        for ent in doc.sentences[0].ents:
            ents.append(ent.text)

        # lower case first word
        words = line.split()
        if words[0] not in ents or doc.sentences[0].words[0].upos == "NUM":
            line = line[0].lower() + line[1:len(line)]
            doc = nlp(line)
            tree = doc.sentences[0].constituency
        if match_ppnpvp(tree):
            # check if sentences start with an On time, sentence
            if line.split()[0] == "On" and len(ents) != 0:
                # strip the sentence
                line = simplify_sentence(tree)
                doc = nlp(line)
                tree = doc.sentences[0].constituency
                base = binary_questions(doc, line)
                q = "when " + base # make a when sentence
                q = format_question(q)
                wh.append(q)
        if match_npvp(tree):
            # check for why questions
            if "because" in line.split():
                line = line.split("because")[0]
                line = line.rstrip(",")
                doc = nlp(line)
                question = why_questions(doc, line)
                wh.append(question)
            # check if the question contains NERs
            if len(ents) != 0:
                question = ner_questions(doc, line)
                wh.extend(question)
            question = binary_questions(doc, line)
            question = format_question(question)
            binary.append(question)
    logger.disabled = False
    return binary, wh


# Main program
if __name__ == "__main__":
    # sentences = ["John made a cake.", "Mary makes a cake.", "I make a cake.", "John has made a cake.",
    #              "I have made a cake.", "She had made a cake.",
    #              "David had lunch in New York with Mary last Sunday because they did not meet in 10 years.",
    #              "John did not go to the gym yesterday.", "John will have a meeting on Monday."]
    sentences = ["Dempsey has also played for New England Revolution, Fulham and Tottenham Hotspur.", "Donovan was a member of the U.S. squad at the 2006 World Cup, in which the Americans eliminated in the group stage.",
                  "He was named to the MLS All-Time Best XI after the season.", "3 airplanes fly across the sky.","One of Dempsey's passion outside of soccer is hip hop music."]
    # sentences = ["He was named to the MLS All-Time Best XI after the season."]
    questions = generating(sentences) # generating binary and wh questions for NP, VP sentences
    for l in questions:
        for q in l:
            print(q)

