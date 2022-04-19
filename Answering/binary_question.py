from Answering import sentence_processing

nlp = sentence_processing.nlp

import spacy

nlp = spacy.load('en_core_web_sm')


def load_NER(sentence):
    doc = nlp(sentence)
    my_tag = {'who': ['PERSON'], 'when': ['DATE', 'TIME'], 'money': ['MONEY'], 'where': ["LOC", "GPE"]}
    ner_dict = {}
    for ent in doc.ents:
        for tag in my_tag:
            found = False
            for t in my_tag[tag]:
                if t == ent.label_:
                    ner_dict[tag] = ner_dict.get(tag, []) + [ent.lemma_.lower()]
                    found = True
                    break
            if found:
                break
        else:
            ner_dict['other'] = ner_dict.get('other', []) + [ent.lemma_.lower()]

    return ner_dict


def compare_NER(sentence_ner, question_ner):
    # TODO: check is question has NER
    if not question_ner:
        return True

    cnt_positive = 0
    cnt_negative = 0
    for tag in question_ner:
        tagged_ner_sentence = sentence_ner[tag]
        tagged_ner_question = question_ner[tag]
        for q_ner in tagged_ner_question:
            for s_ner in tagged_ner_sentence:
                if q_ner == s_ner or q_ner in s_ner or s_ner in q_ner:
                    cnt_positive += 1
                    break
            else:
                cnt_negative += 1
    # print(cnt_positive, cnt_negative)
    return cnt_negative == 0


def answer_binary(sentence, question):
    question_ner = load_NER(sentence)
    sentence_ner = load_NER(question)
    return compare_NER(sentence_ner, question_ner)
