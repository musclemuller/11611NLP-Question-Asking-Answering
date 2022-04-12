from answer_utils import sentence_processing
from answer_utils import answer_generating

import sys

# Import our modules from /modules
sys.path.append("modules")


def answer(question):
    """
    :param question:
    :param word_log_inverse_freq:
    :return:
    """
    # TODO: reformat the question into a sentence
    question_reformat = question
    best_sentence = sentence_processing.find_best_candidate(question_reformat)
    answer_generating.printAnswer(question, best_sentence)


if __name__ == '__main__':
    #article_file_name = sys.argv[1]
    #question_file_name = sys.argv[2]
    article_file_name = 'nlp-project-dev-data-articles/set1/a1.txt'
    question_file_name = 'question_set1_a1.txt'

    question_list = open(question_file_name, encoding='utf8').read().split("\n")
    sentence_processing.load_file(article_file_name)
    sentence_processing.cal_log_inverse_sentence_fre(article_file_name)
    for q in question_list:
        answer(q)
