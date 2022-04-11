def read_input_file(filename):
    """
    Read input from input file into string
    :param filename: filename of input file
    :return: string containing all contents of input file
    """

    with open(filename, "r", encoding='utf-8') as f:
        return f.read()


def write_output_file(filename, list):
    fp = open(filename, 'w+', encoding='utf-8')
    for i in range(len(list)):
        # fp.write(str(i) + " " + str(len(list[i])) + " " + list[i] + '\n')
        fp.write(list[i] + '\n')