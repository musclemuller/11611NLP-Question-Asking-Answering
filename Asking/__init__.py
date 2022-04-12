import sentences_generating
import apposition
import conjunction
import question_generating
import utils
import ranking
import sys

if __name__ == "__main__":
    # filename = "../nlp-project-dev-data-articles/set1/a1.txt"
    filename = sys.argv[1]
    num_questions = sys.argv[2]

    # preprocessing
    input_text = utils.read_input_file(filename)
    sentences = sentences_generating.do_segementation(input_text)
    sentences = apposition.parse_tree(sentences)
    sentences = conjunction.parse_tree(sentences)
    sentences = [s for s in sentences if s.count(' ') < 50]

    # question generating
    binary, wh = question_generating.generating(sentences)

    # ranking
    ranked_binary = ranking.ranking(binary)
    ranked_wh = ranking.ranking(wh)
    binary, wh = ranking.process_binary_wh_nums(ranked_binary, ranked_wh)

    questions = []
    questions.extend(binary)
    questions.extend(wh)
    sorted_questions = sorted(questions, key=len)

    for question in range(min(num_questions, len(sorted_questions))):
        print(question)

    # # write to question file
    # output_file = "./questions/set1_a1_question.txt"
    # utils.write_output_file(output_file, binary)
    # utils.write_output_file_append(output_file, wh)
