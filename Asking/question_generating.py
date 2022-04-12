from tag import *
import stanza
import logging


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


def binary_questions(doc):
    question = ""
    for word in doc.sentences[0].words:
        if word.deprel == "aux":
            return aux_binary_quesitons(doc)
        elif word.xpos == "VBP":
            question = "do " + question
            question = question + word.lemma + " "
        elif word.xpos == "VBZ":
            question = "does " + question
            question = question + word.lemma + " "
        elif word.xpos == "VBD":
            question = "did " + question
            question = question + word.lemma + " "
        elif word.xpos == ".":
            break;
        else:
            question = question + word.text + " "

    return question


def aux_binary_quesitons(doc):
    question = ""
    for word in doc.sentences[0].words:
        if word.deprel == "aux":
            question = word.text + " " + question
        elif word.xpos == ".":
            break;
        else:
            question = question + word.text + " "

    return question


def ner_questions(doc, sentence):
    questions = []
    try:
        ents = {}
        for ent in doc.sentences[0].ents:
            ents[ent.text] = ent.type
        words = sentence.split()
        first_word = words[0]
        if first_word in ents.keys():
            words[0] = get_wh(ents[first_word])
            if words[0] is not None:
                question = " ".join(words)
                questions.append(format_question(question))
                del ents[first_word]
                return questions

        base = binary_questions(doc)
        # print("base:", base)
        for ent in ents.keys():
            wh = get_wh(ents[ent])
            if wh is None:
                continue
            # print("wh:", wh)
            question = wh + " " + base
            question = question.replace(ent, "", 1)
            questions.append(format_question(question))
    except:
        return []
    return questions


def get_wh(ent):
    if ent == "PERSON":
        return "who"
    if ent == "GPE":
        return "where"
    if ent == "DATE":
        return "when"


def why_questions(doc):
    question = binary_questions(doc)
    question = "Why " + question
    return format_question(question)


def format_question(question):
    str = question.strip()
    str = str.rstrip(".")
    str = str.replace("  ", " ")
    str = str[0].upper() + str[1:len(str)]
    str = str + "?"
    return str


def generating(sentences):
    logger = logging.getLogger('stanza')
    logger.disabled = True
    nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,constituency,lemma,depparse, ner')
    binary = []
    wh = []
    for line in sentences:
        doc = nlp(line)
        tree = doc.sentences[0].constituency
        if match_npvp(tree):
            # check for why questions
            if "because" in line.split():
                line = line.split("because")[0]
                line = line.rstrip(",")
                doc = nlp(line)
                question = why_questions(doc)
                wh.append(question)
            # check if the question contains NERs
            if len(doc.sentences[0].ents) != 0:
                question = ner_questions(doc, line)
                wh.extend(question)
            question = binary_questions(doc)
            question = format_question(question)
            binary.append(question)
    logger.disabled = False
    return binary, wh


# Main program
if __name__ == "__main__":
    sentences = ["John made a cake.", "Mary makes a cake.", "I make a cake.", "John has made a cake.",
                 "I have made a cake.", "She had made a cake.",
                 "David had lunch in New York with Mary last Sunday because they did not meet in 10 years."]
    # stanza.download(lang='en', processors='tokenize,mwt,pos,constituency,lemma,depparse, ner')
    # nlp = stanza.Pipeline(lang='en', processors='tokenize,mwt,pos,constituency,lemma,depparse, ner')
    # questions = []
    # for line in sentences:
    #     doc = nlp(line)
    #     tree = doc.sentences[0].constituency
    #     if match_npvp(tree):
    #         # check for why questions
    #         if "because" in line.split():
    #             line = line.split("because")[0]
    #             line = line.rstrip(",")
    #             doc = nlp(line)
    #             question = why_questions(doc)
    #             questions.append(question)
    #         # check if the question contains NERs
    #         if len(doc.sentences[0].ents) != 0:
    #             question = ner_questions(doc, line)
    #             questions.extend(question)
    # 
    #         question = binary_questions(doc)
    #         question = format_question(question)
    #         questions.append(question)
    questions = generating(sentences)

    print(questions)
