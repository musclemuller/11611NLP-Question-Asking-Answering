from Answering import sentence_processing

nlp = sentence_processing.nlp


def answer_who(q, a):
    query = nlp(q)
    origin = nlp(a)

    candidate_ents = [ent for ent in origin.ents if
                      ent.label_ == 'PERSON' or ent.label_ == 'ORG' and ent.text not in str(query.text)]
    asking_token = [token for token in query if token.text.upper() in ('WHO', 'WHOM')][0]

    def token_similarity(who, candidate):
        score = 0
        if who.dep_ == candidate.dep_:
            score = score + 3
        who_parent = [token for token in who.head.subtree if token.dep_ == 'conj']
        who_parent.append(who.head)

        candidate_parent = [token for token in candidate.head.subtree if token.dep_ == 'conj']
        candidate_parent.append(candidate.head)

        matching_parents_who = []
        matching_parents_can = []
        for verb in who_parent:
            for token in candidate_parent:
                if verb.lemma_ == token.lemma_:
                    matching_parents_who.append(verb)
                    matching_parents_can.append(token)
        matches = len(matching_parents_who)
        if matches > 0:
            for i in range(0, matches):
                query_verb = matching_parents_who[i]
                origin_verb = matching_parents_can[i]

                # descendents lemma match
                query_lemmas = [t.lemma_ for t in query_verb.subtree if not t.is_stop]
                origin_lemmas = [t.lemma_ for t in origin_verb.subtree if not t.is_stop]
                score += len(set(query_lemmas).intersection(origin_lemmas))
        return score

    answer, kept_score = a, 0

    for ent in candidate_ents:
        curr_score = token_similarity(asking_token, ent[-1])
        if curr_score > kept_score:
            answer = ent.text
            kept_score = curr_score

    return answer + '.' if answer[-1] != '.' else answer


def answer_when(question, a):
    query = nlp(question)
    reply = nlp(a)
    query_token = [t for t in query if t.text.upper() == 'WHEN'][0]

    answer = reply.text

    query_verb = query_token.head

    # find same token in reply
    reply_verb = [t for t in reply if t.lemma_ == query_verb.lemma_]

    when_lst = [ent.text for ent in reply.ents if ent.label_ == 'DATE' or ent.label_ == 'TIME']

    if len(reply_verb) > 0:
        reply_root = reply_verb[0]

        for token in reply_root.children:
            if token.dep_ == 'npadvmod':
                l = token.left_edge.idx
                r = token.right_edge.idx + len(token.right_edge.text)
                s = reply.text[l: r]

                # format
                answer = s.capitalize() + '.'
                break
        else:
            if when_lst:
                answer = when_lst[0].capitalize() + '.'
    else:
        if when_lst:
            if when_lst[0][0].isalpha():
                answer = when_lst[0].capitalize() + '.'
            else:
                answer = 'It was ' + when_lst[0].capitalize() + '.'
    return answer


def answer_where(question, answer):
    answer = answer
    reply = nlp(answer)

    for token in reply:
        if token.dep_ == 'pobj':
            l = token.left_edge.idx
            r = token.right_edge.idx + len(token.right_edge.text)
            s = reply.text[l: r]

            # format
            answer = s.capitalize() + '.'
            break

    return answer


def answer_why(question, a):
    answer = a
    reply = nlp(a)

    # empirical division
    case = ''
    for token in reply:
        if token.text.lower() == 'because':
            if token.nbor().text == 'of':
                case = 'becauseof'
            else:
                case = 'because'
        if token.text.lower() == 'since' and token.pos_ == 'SCONJ':
            case = 'since'
        if token.text.lower() == 'due' and token.nbor().text == 'to':
            case = 'dueto'
        if token.text.lower() == 'reason':
            case = 'clause'

    # because / because of

    if case == 'becauseof':
        for token in reply:
            if token.text.lower() == 'because' and token.nbor().text == 'of':
                for t in token.children:
                    if t.dep_ == 'pobj':
                        l = t.left_edge.idx
                        r = t.right_edge.idx + len(t.right_edge.text)
                        s = reply.text[l: r]
                        answer = s.capitalize() + '.'

    if case == 'dueto':
        for token in reply:
            if token.text.lower() == 'due' and token.nbor().text == 'to':
                for t in token.children:
                    if t.dep_ == 'pobj':
                        l = t.left_edge.idx
                        r = t.right_edge.idx + len(t.right_edge.text)
                        s = reply.text[l: r]
                        answer = s.capitalize() + '.'

    if case == 'because' or case == 'since':
        for token in reply:
            if token.pos_ == 'SCONJ':
                t = token.head
                l = t.left_edge.idx
                r = t.right_edge.idx + len(t.right_edge.text)
                s = reply.text[l: r]
                answer = s.capitalize() + '.'

    return answer


def answer_how(q, a):
    answer = a
    reply = nlp(a)

    for token in reply:
        if token.dep_ == 'prep':
            l = token.left_edge.idx
            r = token.right_edge.idx + len(token.right_edge.text)
            s = reply.text[l: r]

            # format
            answer = s.capitalize() + '.'
            break

    return answer


def answer_how_many(q, a):
    answer = a

    reply = nlp(a)

    for ent in reply.ents:
        if ent.label_ in ('CARDINAL', 'MONEY'):
            answer = ent.text

            answer = answer.capitalize() + '.'

    return answer


if __name__ == '__main__':
    print(answer_who('When did Harry die?', 'get send by'))