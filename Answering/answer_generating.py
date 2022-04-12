from Answering import sentence_processing

nlp = sentence_processing.nlp


def printAnswer(ask, original):
    # Question Classification
    question = nlp(ask)
    if question[0].pos_ == 'AUX':
        question_type = 'is'
    elif question[0].pos_ == 'PRON':
        question_type = 'wh'
    else:
        question_type = 'uk'

        # Is-A Question
    if question_type == 'is':
        # find closest subpart in original one
        # namely: with same beginning & ending
        answer = "Yes"

        # Rule 1: Unmatching NERs
        for ent in question.ents:
            if ent.text not in original:
                answer = "No"

        # Rule 2: Parts match with NOT
        T = nlp(original)
        for token in T:
            if token.text not in str(question.text):
                if token.text.endswith("n't") or token.text.endswith('not') or token.text.endswith('no'):
                    answer = "No"

        print(answer)

    if question_type == 'wh':
        # for token in question:
        #     print(token.pos_)
        # for ent in question.ents:
        #     print(ent.text, ent.label_)

        Q = question
        T = nlp(original)
        answer = original

        # if NER doesn't match, return corresponding NER
        for ent in T.ents:
            if ent.text not in Q.text:
                answer = ent.text

        print(answer)

    if question_type == 'uk':
        print(original)
