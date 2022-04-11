import math
import spacy

sentences = []
sentences_lemma = []
word_freq_sentence = {}
sentences_vectors = []
nlp = spacy.load('en_core_web_sm')


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


def load_file(article_name):
    """
    :param article_name: string
    :return: list of sentence
    """
    doc = nlp(open(article_name, encoding='utf8').read())
    for sen in doc.sents:
        # TODO: how solve the '\n'
        sentences.append(sen.text.split('\n')[-1])
        sen_lemma = []
        for word in sen:
            sen_lemma.append(word.lemma_)
        sentences_lemma.append(sen_lemma)


def my_tokenize(sentence):
    """
    :param sentence: string
    :return: list of tokenize words (lemma or not?) => can be set()
    """
    # TODO
    nlp_result = nlp(sentence)
    lemmas = []

    for token in nlp_result:
        lemmas.append(token.lemma_)
    return lemmas


def term_fre(words):
    term_f = {}
    for w in words:
        term_f[w] = term_f.get(w, 0) + 1
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
    q_lst = 0
    s_lst = 0
    for q in q_vector:
        if q in s_vector:
            similarity += q_vector[q] * s_vector[q]
            q_lst += q_vector[q] ** 2
            s_lst += s_vector[q] ** 2
    # similarity / (math.sqrt(q_lst) * math.sqrt(s_lst)) if math.sqrt(q_lst) * math.sqrt(s_lst) != 0 else 0
    return similarity


def cal_log_inverse_sentence_fre(article_name):
    """
    :param article_name: string
    :return: dict of log inverse of sentence frequency
    """
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