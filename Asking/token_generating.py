import spacy
import nltk

def write_sentences(filename, list):
    fp = open(filename, 'w+')
    for i in range(len(list)):
        if(len(list[i]) > 1):
            for token in list[i]:
                fp.write(token + ' | ')
            fp.write('\n')


# Main program
if __name__ == "__main__":
    filename = "../sentences/set1_a1.txt"
    nlp = spacy.load('en_core_web_lg')
    tokens = []
    with open(filename, "r") as f:
        for line in f:
            doc = nlp(line.replace('\n', '').replace('\r', ''))
            one_sentence_token = []
            for token in doc:
                one_sentence_token.append(token.text)
            tokens.append(one_sentence_token)

    output_file = "../tokens/set1_a1.txt"
    write_sentences(output_file, tokens)