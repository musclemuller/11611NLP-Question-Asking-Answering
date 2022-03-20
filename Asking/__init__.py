import sentences_generating
import stanford_parse

if __name__ == "__main__":
    filename = "../nlp-project-dev-data-articles/set1/a1.txt"
    input_text = sentences_generating.read_input_file(filename)
    store = sentences_generating.do_segementation(input_text)
    trees = stanford_parse.parse_tree(store)
    # for tree in trees:
    #     print(tree)
    # apposition
    appositions = stanford_parse.find_apposition(trees)
    # for apposition in appositions:
    #     print(apposition)
    # conjunction

    # NER tag

    output_file = "../sentences/set1_a1.txt"
    sentences_generating.write_sentences(output_file, store)
