import os
import nltk
import spacy
import countChar
import benepar

def read_input_file(filename):
    """
    Read input from input file into string
    :param filename: filename of input file
    :return: string containing all contents of input file
    """

    with open(filename, "r") as f:
        return f.read()


def write_sentences(filename, list):
    fp = open(filename, 'w+')
    for i in range(len(list)):
        # fp.write(str(i) + " " + str(len(list[i])) + " " + list[i] + '\n')
        fp.write(list[i] + '\n')

def do_segementation(input_text):
    store = nltk.sent_tokenize(input_text)
    for i in range(len(store)):
        sentence = store[i]
        sentence = sentence.replace('\r', '').replace('\n', '').replace('\t', '')
        store[i] = sentence
    store.sort(key=lambda i: len(i))
    store = [s for s in store if s.count(' ') < 50]
    return store


# Main program
if __name__ == "__main__":
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"
    input_text = read_input_file(filename)
    store = do_segementation(input_text)
    output_file = "../sentences/set1_a1.txt"
    write_sentences(output_file, store)
