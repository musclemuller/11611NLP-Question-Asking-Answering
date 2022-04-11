PRONOUN = {"i", "me", "we", "us", "you", "he", "she", "it", "they", "them", "my", "mine", "our", "ours", "your",
           "yours", "his", "her", "its", "their", "theirs", "myself", "yourself", "himself", "herself", "itself",
           "ourselves", "yourselves", "themselves"}

DEFINITE_ARTICLE = {"the", "this", "that", "these", "those"}

def count_pronoun(question):
    words = question.split()
    count = 0
    for word in words:
        if word.lower() in PRONOUN:
            count = count + 1
    return count


def count_definite_article(question):
    words = question.split()
    count = 0
    for word in words:
        if word.lower() in DEFINITE_ARTICLE:
            count = count + 1
    return count
