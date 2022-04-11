from collections import defaultdict
import ranking_utils


def length_limit(questions):
    return [question for question in questions if 5 < question.count(' ') < 30]


def grade_for_pronoun(question_dict):
    for key in question_dict.keys():
        question_dict[key] = question_dict[key] - ranking_utils.count_pronoun(key)
    return question_dict


def grade_for_definite_article(question_dict):
    for key in question_dict.keys():
        question_dict[key] = question_dict[key] - ranking_utils.count_definite_article(key)
    return question_dict

def ranking(questions):
    questions = length_limit(questions)
    questions_dict = defaultdict(lambda: 0)
    for question in questions:
        questions_dict[question] = 0
    questions_dict = grade_for_pronoun(questions_dict)
    questions_dict = grade_for_definite_article(questions_dict)
    ranked_questions = sorted(questions_dict.items(), key=lambda item: item[1], reverse=True)
    return  ranked_questions

def process_binary_wh_nums(ranked_binary, ranked_wh):
    standard_length = 0
    binary_len = len(ranked_binary)
    wh_len = len(ranked_wh)
    if binary_len > wh_len:
        standard_length = wh_len
    else:
        standard_length = binary_len
    binary = []
    wh = []
    for rb in ranked_binary:
        binary.append(rb[0])
    for rw in ranked_wh:
        wh.append(rw[0])
    binary = binary[:standard_length]
    wh = wh[:standard_length]
    return binary, wh

if __name__ == "__main__":
    binary = ["Has DempseyClinton also played for New England Revolution , Fulham and Tottenham Hotspur?",
              "Did Dempsey score the game-winning goal in the Eastern Conference Final on his way to an appearance "
              "in the MLS Cup Final?"]

    wh = ["Who did break Fulham 's Premier League goalscoring record by netting twice in a 3–0 victory over Bolton on "
          "April 27 , 2011?",
          "Where did did Fulham come from a goal down to beat 3–1 away from home as Dempsey score two goals on April "
          "12?"]

    binary = length_limit(binary)
    wh = length_limit(wh)

    binary_dict = defaultdict(lambda: 0)
    wh_dict = defaultdict(lambda: 0)
    for bi in binary:
        binary_dict[bi] = 0
    for w in wh:
        wh_dict[w] = 0

    binary_dict = grade_for_pronoun(binary_dict)
    binary_dict = grade_for_definite_article(binary_dict)

    wh_dict = grade_for_definite_article(wh_dict)
    wh_dict = grade_for_definite_article(wh_dict)

    ranked_binary = sorted(binary_dict.items(), key=lambda item: item[1], reverse=True)
    ranked_wh = sorted(wh_dict.items(), key=lambda item: item[1], reverse=True)
    print(ranked_binary)
    print(ranked_wh)
    binary, wh = process_binary_wh_nums(ranked_binary, ranked_wh)
    print(binary)
    print(wh)
