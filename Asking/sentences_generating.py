import nltk
import spacy
import utils
import logging

def do_segementation(input_text):
    logger1 = logging.getLogger('nltk')
    logger2 = logging.getLogger('spacy')
    logger1.disabled = True
    logger2.disabled = True
    store = nltk.sent_tokenize(input_text, language='english')

    pronouns = {"He", "She", "It"}
    pos_pronouns = {"His", "Her", "Its"}
    subject = ""
    pronoun = ""
    nlp = spacy.load("en_core_web_lg")

    for i in range(len(store)):
        sentence = store[i]
        sentence = sentence.replace('\r', '').replace('\n', '').replace('\t', '')
        store[i] = sentence
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
    logger1.disabled = False
    logger2.disabled = False
    return store


# Main program
if __name__ == "__main__":
    filename = "../data/set1/a1.txt"
    input_text = utils.read_input_file(filename)
    store = do_segementation(input_text)

    # sentences = "Dempsey was born in Nacogdoches, Texas, and, for much of his childhood, his family lived in a trailer park, where he and his siblings grew up playing soccer with Hispanic immigrants. In his teens, Dempsey maintained these ties playing in a local Mexican-dominated adult league. Dempsey is of Irish descent on his father's side. His older brother Ryan was offered a tryout for the Dallas Texans, an elite youth soccer club, and brought Clint, who was noticed and recruited while passing time juggling a ball on the sidelines."
    # store = do_segementation(sentences)

    output_file = "../sentences/set1_a1.txt"
    utils.write_output_file(output_file, store)
