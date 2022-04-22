from Answering import sentence_processing
from Answering import binary_question
from Answering import answer_different_types

nlp = sentence_processing.nlp


def printAnswer(question, original):
    try:
        # Question Classification
        question = nlp(question)
        answer = original
        if question[0].pos_ == 'AUX':
            answer = binary_question.answer_binary(question, original)
        elif question[0].lemma_.lower() == 'who':
            answer = answer_different_types.answer_who(question, original)
        elif question[0].lemma_.lower() == 'why':
            answer = answer_different_types.answer_why(question, original)
        elif question[0].lemma_.lower() == 'where':
            answer = answer_different_types.answer_where(question, original)
        elif question[0].lemma_.lower() == 'when':
            answer = answer_different_types.answer_when(question, original)
        elif question[0].lemma_.lower() == 'how':
            if question[1].lemma_.lower() == 'many':
                answer = answer_different_types.answer_how_many(question, original)
            else:
                answer = answer_different_types.answer_how(question, original)
    except:
        answer = original
    finally:
        print(answer.replace('\n', '').replace('\t', '').replace('\r', ''))


if __name__ == '__main__':
    printAnswer('How many did you go?', 'I go 300 times.')
