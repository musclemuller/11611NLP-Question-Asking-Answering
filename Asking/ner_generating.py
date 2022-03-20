import spacy

def write_sentences(filename, list):
    fp = open(filename, 'w+')
    for i in range(len(list)):
        ner = list[i]
        if len(ner) == 4:
            fp.write("TEXT: " + ner[0] + " ")
            fp.write("START: " + ner[1] + " ")
            fp.write("END: " + ner[2] + " ")
            fp.write("LABEL: " + ner[3] + " ")
            fp.write('\n')


# Main program
if __name__ == "__main__":
    filename = "../sentences/set1_a1.txt"
    nlp = spacy.load('en_core_web_sm')
    ners = []
    with open(filename, "r") as f:
        for line in f:
            doc = nlp(line.replace('\n', '').replace('\r', ''))
            one_ner = []
            for ent in doc.ents:
                one_ner.append(ent.text)
                one_ner.append(str(ent.start_char))
                one_ner.append(str(ent.end_char))
                one_ner.append(ent.label_)
            ners.append(one_ner)

    output_file = "../NERs/set1_a1.txt"
    write_sentences(output_file, ners)