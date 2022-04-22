import math
import spacy
import logging

sentences = []
sentences_lemma = []
word_freq_sentence = {}
sentences_vectors = []
logger = logging.getLogger('spacy')
logger.disabled = True
nlp = spacy.load('en_core_web_lg')

# TODO: remove stop words?
all_stopwords = nlp.Defaults.stop_words


# all_stopwords.add("?")


def vectorize_sentence(sentence_lemma):
    """
    input sentence lemma and calculate the feature vector
    :param sentence_lemma: List[lemma]
    :return: feature vector of sentence
    """
    term_freq_sentence = term_fre(sentence_lemma)
    vector_sentence = {}
    for w in term_freq_sentence:
        vector_sentence[w] = term_freq_sentence[w] * word_freq_sentence.get(w, 0)
    return vector_sentence


def load_file(file_input):
    """
    :param file_input:
    :param article_name: string
    :return: list of sentence

    """
    sentences.clear()
    sentences_lemma.clear()
    word_freq_sentence.clear()
    sentences_vectors.clear()

    doc = nlp(file_input)

    previous_nsubj = None

    for sen in doc.sents:
        # TODO: how solve the '\n'
        sen_spit = sen.text.split('\n')

        # handel '\n'
        if len(sen_spit) > 1:
            max_sen = max(sen_spit, key=lambda x: len(x))
            sen = nlp(max_sen)

        sen_lemma = []
        word_lst = []
        for token in sen:
            current_word = token.text_with_ws
            if not token.is_punct:
                sen_lemma.append(token.lemma_.lower())
            if token.dep_ == 'nsubj':
                if token.tag_ != 'PRP':
                    previous_nsubj = token.text_with_ws
                    sen_lemma.append(token.lemma_.lower())
                else:
                    if previous_nsubj:
                        sen_lemma.append(previous_nsubj.lower())
                        current_word = previous_nsubj
                    else:
                        sen_lemma.append(token.lemma_.lower())
            if not current_word.isspace():
                word_lst.append(current_word)

        sentences_lemma.append(sen_lemma)

        sentences.append(''.join(word_lst))


def my_tokenize(sentence):
    """
    :param sentence: string
    :return: list of tokenize words (lemma or not?) => can be set()
    """
    # TODO
    nlp_result = nlp(sentence)

    return [word.lemma_.lower() for word in nlp_result if not word.is_punct]


def term_fre(words):
    term_f = {}
    for w in words:
        # TODO: term frequency
        term_f[w] = 1
        # term_f[w] = term_f.get(w, 0) + 1
    return term_f


def vectorize_question(question):
    tokenized_question = my_tokenize(question)
    term_freq_question = term_fre(tokenized_question)
    vector_question = {}
    for w in term_freq_question:
        vector_question[w] = term_freq_question[w] * word_freq_sentence.get(w, 0)
    return vector_question


def cal_similarity(q_vector, s_vector):
    similarity = 0
    s_lst = 0
    for q in q_vector:
        if q in s_vector:
            similarity += q_vector[q] * s_vector[q]

    for s in s_vector:
        s_lst += s_vector[s] ** 2
    # similarity /  math.sqrt(s_lst) if math.sqrt(s_lst) != 0 else 0
    return (similarity / math.sqrt(s_lst)) if math.sqrt(s_lst) != 0 else 0


def cal_log_inverse_sentence_fre(file_input):
    """
    :param article_name: string
    :return: dict of log inverse of sentence frequency
    """
    load_file(file_input)
    # print('Log inverse: tokenize')
    for sentences_idx in range(len(sentences)):
        word_set = set()
        for word in sentences_lemma[sentences_idx]:
            if word not in word_set:
                word_freq_sentence[word] = word_freq_sentence.get(word, 0) + 1
                word_set.add(word)

    for k in word_freq_sentence:
        word_freq_sentence[k] = math.log(float(len(sentences)) / word_freq_sentence[k])

    for sentences_idx in range(len(sentences)):
        sentences_vectors.append(vectorize_sentence(sentences_lemma[sentences_idx]))


def find_best_candidate(question):
    best_idx = 0
    best_similarity = -1
    question_vector = vectorize_question(question)

    for sentence_idx in range(len(sentences)):
        # print(sentence_idx)
        similarity = cal_similarity(question_vector, sentences_vectors[sentence_idx])
        if similarity > best_similarity:
            best_idx = sentence_idx
            best_similarity = similarity

    return sentences[best_idx]
