import sentences_generating
import apposition_util

if __name__ == "__main__":
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"
    input_text = sentences_generating.read_input_file(filename)
    store = sentences_generating.do_segementation(input_text)
    trees = apposition_util.parse_tree(store)
    appositions = apposition_util.find_apposition(trees)

    # NER tag

    output_file = "../sentences/set1_a1.txt"
    sentences_generating.write_sentences(output_file, store)
