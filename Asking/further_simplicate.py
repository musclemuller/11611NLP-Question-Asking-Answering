from Asking import sentences_generating
from Asking import models


def further_simplification(sentences):
    nlp = models.spacy_nlp

    simplified_sentences = []
    for line in sentences:
        for_this_line = []
        doc = nlp(line)

        root = return_root(doc)
        if root is None:
            simplified_sentences.append(line)
            continue;
        list_of_verbs = verbs(doc, root)
        first_noun = noun(root)

        ranges = []
        for verb in list_of_verbs:
            start = len(doc)
            end = -1
            for child in verb.children:
                if child not in list_of_verbs:
                    if child.dep_ == 'punct':
                        end = child.i
                        break;
                    if child.i < start:
                        start = child.i
                    if child.i > end:
                        end = child.i
            ranges.append((start, end))

        for range in ranges:
            start = range[0]
            end = range[1]
            if start < end:
                clause = doc[start:end]
                if first_noun != None:
                    temp = change_noun(clause, first_noun)
                else:
                    temp = clause.text
                # format each sentence
                temp = temp + "."
                temp = temp[0].upper() + temp[1:len(temp)]
                for_this_line.append(temp)

        if len(for_this_line) == 0:
            simplified_sentences.append(line)
        else:
            simplified_sentences.extend(for_this_line)
    return simplified_sentences

def return_root(doc):
    for token in doc:
        if token.dep_ == "ROOT":
            return token

def verbs(doc, root):
    list = []
    list.append(root)
    for token in doc:
        # if is not root
        if token != root:
            if token.pos_ == "VERB" and token.dep_ == "conj":
                list.append(token)
    return list

def noun(root):
    for child in root.children:
        if child.dep_ == "nsubj":
            return child

def change_noun(doc, noun):
    sentence = ""
    for token in doc:
        if token.dep_ == "nsubj":
            sentence += noun.text
            sentence += token.whitespace_
        else:
            sentence += token.text_with_ws
    return sentence

if __name__ == "__main__":
    # text =""
    # sentences = sentences_generating.do_segementation(text)
    sentences = ['Before moving to Fulham, Dempsey went for a trial at ŁKS Łomża where the coach sent him to Fulham.', 'On January 11, 2007, he was granted a work permit from the Home Office as Fulham announced his signing on a long-term deal.', "In December 2006, English club Fulham offered MLS $4 million for the transfer of Dempsey, then the largest amount ever offered for an MLS player, and he became another American addition to a Cottagers' squad which included US internationals Brian McBride and Carlos Bocanegra."]
    further_simplification(sentences)
    for sentence in sentences:
        print(sentence)
    # find_apposition(trees)
