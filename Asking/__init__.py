import sentences_generating
import apposition
import conjunction

if __name__ == "__main__":
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"

    # preprocessing
    input_text = sentences_generating.read_input_file(filename)
    store = sentences_generating.do_segementation(input_text)
    store = apposition.parse_tree(store)
    store = conjunction.parse_tree(store)
    store = [s for s in store if s.count(' ') < 50]

    # question generating


    output_file = "../sentences/set1_a1.txt"
    sentences_generating.write_sentences(output_file, store)
