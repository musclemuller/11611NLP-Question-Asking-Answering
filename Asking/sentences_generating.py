import os
import nltk
import spacy
import count_char
import benepar

def read_input_file(filename):
    """
    Read input from input file into string
    :param filename: filename of input file
    :return: string containing all contents of input file
    """

    with open(filename, "r", encoding='utf-8') as f:
        return f.read()


def write_sentences(filename, list):
    fp = open(filename, 'w+', encoding='utf-8')
    for i in range(len(list)):
        # fp.write(str(i) + " " + str(len(list[i])) + " " + list[i] + '\n')
        fp.write(list[i] + '\n')

def do_segementation(input_text):
    store = nltk.sent_tokenize(input_text, language='english')

    pronouns = {"He", "She", "It"}
    pos_pronouns = {"His", "Her", "Its"}
    subject = ""
    pronoun = ""
    nlp = spacy.load("en_core_web_trf")

    for i in range(len(store)):
        sentence = store[i]
        sentence = sentence.replace('\r', '').replace('\n', '').replace('\t', '')
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
    # store.sort(key=lambda i: len(i))
    store = [s for s in store if s.count(' ') < 50]
    return store


# Main program
if __name__ == "__main__":
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"
    input_text = read_input_file(filename)
    store = do_segementation(input_text)

    # sentences = "Dempsey was born in Nacogdoches, Texas, and, for much of his childhood, his family lived in a trailer park, where he and his siblings grew up playing soccer with Hispanic immigrants. In his teens, Dempsey maintained these ties playing in a local Mexican-dominated adult league. Dempsey is of Irish descent on his father's side. His older brother Ryan was offered a tryout for the Dallas Texans, an elite youth soccer club, and brought Clint, who was noticed and recruited while passing time juggling a ball on the sidelines."
    # store = do_segementation(sentences)

    output_file = "../sentences/set1_a1.txt"
    write_sentences(output_file, store)
