import sentences_generating
import apposition
import conjunction
import question_generating
import utils

if __name__ == "__main__":
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"

    # preprocessing
    input_text = utils.read_input_file(filename)
    sentences = sentences_generating.do_segementation(input_text)
    sentences = apposition.parse_tree(sentences)
    sentences = conjunction.parse_tree(sentences)
    sentences = [s for s in sentences if s.count(' ') < 50]
    # for i in range(len(sentences)):
    #     print(str(i), repr(sentences[i]))
    # question generating
    questions = question_generating.generating(sentences)

    # ranking

    output_file = "./questions/set1_a1_question.txt"
    utils.write_output_file(output_file, questions)
