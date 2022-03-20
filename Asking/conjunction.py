import spacy, benepar


def parse_tree(sentence):
    nlp = spacy.load('en_core_web_trf')
    if spacy.__version__.startswith('2'):
        nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
    else:
        nlp.add_pipe("benepar", config={"model": "benepar_en3"})
    doc = nlp(sentence)
    sent = list(doc.sents)[0]
    sent = list(doc.sents)[0]
    print(sent._.parse_string)
    print(sent._.labels)
    print(list(sent._.children)[0])
    # doc = nlp(sentence)
    # for token in doc:
    #     print(token.tag_)


if __name__ == "__main__":
    input_sentence1 = "Andy has a bag of apples, which are sweet."
    input_sentence2 = "Bill Gates, a brilliant entrepreneur, owns Microsoft."
    parse_tree(input_sentence2)
    