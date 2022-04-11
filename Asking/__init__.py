import sentences_generating
import apposition
import conjunction
import question_generating

if __name__ == "__main__":
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"

    # preprocessing
    input_text = sentences_generating.read_input_file(filename)
    sentences = sentences_generating.do_segementation(input_text)
    sentences = apposition.parse_tree(sentences)
    sentences = conjunction.parse_tree(sentences)
    sentences = [s for s in sentences if s.count(' ') < 50]

    # question generating
    questions = question_generating.generating(sentences)

    # ranking

    output_file = "../sentences/set1_a1.txt"
    sentences_generating.write_sentences(output_file, questions)
