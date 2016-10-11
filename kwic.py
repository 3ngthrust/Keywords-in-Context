# -*- coding: utf-8 -*-
# Author: @3ngthrust
# Licensed under the terms of the MIT License see LICENSE.txt for Details.

def cut_to_sentence(text, keyword, keywordindex):
    """ Cuts the sentence around a keyword out of the text

    Arguments
    ----------
    text : str
        Text out of which the sentence should be extracted
    keyword : str
        Keyword in the sentence of the text
    keywordindex: int
        Index of the keyword in the text

    Returns
    -------
    Indices of of the sentence in the text and a string of the sentence
    """
    # Strings after wich a point does not end a sentence
    safe = ["Ms", "Mr", "Fr", "Hr", "Dipl", "B", "M", "Sc", "Dr", "Prof",
            "Mo", "Mon", "Di", "Tu", "Tue", "Tues", "Mi", "Wed", "Do", "Th",
            "Thu", "Thur", "Thurs", "Fr", "Fri", "Sa", "Sat", "So", "Sun",
            "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
            "str"]

    # Find beginning
    rfind_results = []
    end_ = keywordindex
    # Special Case "."
    while True:
        rfind_ = text.rfind(". ", 0, end_)
        if not rfind_ == -1:
            no_safe = False
            for i, s in enumerate(safe):
                if text[0:rfind_][::-1].find(s[::-1]) == 0:
                    end_ = rfind_ - len(s)
                    break
                if i == len(safe)-1:
                    no_safe = True
            if no_safe is True:
                break
        else:
            break
    rfind_results.append(rfind_)

    rfind_results.append(max([text.rfind(sentence_ending, 0, keywordindex)
                              for sentence_ending in ["! ", "? "]]))

    rfind_result = max(rfind_results)
    if rfind_result == -1:
        start = 0
    else:
        start = rfind_result + 2

    # Find ending
    find_results = []
    start_ = keywordindex+len(keyword)
    # Special Case "."
    while True:
        find_ = text.find(". ", start_)
        if not find_ == -1:
            no_safe = False
            for i, s in enumerate(safe):
                if text[0:find_][::-1].find(s[::-1]) == 0:
                    start_ = find_ + len(s)
                    break
                if i == len(safe)-1:
                    no_safe = True
            if no_safe is True:
                break
        else:
            break
    find_results.append(find_)

    find_results.extend([text.find(sentence_ending, keywordindex+len(keyword))
                         for sentence_ending in ["! ", "? "]])
    find_results_bigger_neg_1 = [i for i in find_results if i >= 0]
    if not find_results_bigger_neg_1:
        end = len(text)
    else:
        end = min(find_results_bigger_neg_1) + 1

    return list(range(start, end)), text[start:end]

def find_nth_occurrence(text, searchstr, nth=1, startindex=0):
    """
    Finds the index of the nth occurence of a searchstr in the text starting
    from the a given startindex.
    """
    start = text.find(searchstr, startindex)

    if start == -1:
        return len(text)-1

    for i in range(nth-1):
        find_index = text.find(searchstr, start+len(searchstr))
        if find_index == -1:
            return len(text)-1
        else:
            start = find_index

    return start

def rfind_nth_occurrence(text, searchstr, nth=1, endindex=None):
    """
    Finds the index of the nth occurence of a searchstr in the text going
    backwards from a given endindex.
    """
    if endindex is None:
        endindex = len(text)

    end = text.rfind(searchstr, 0, endindex)

    if end == -1:
        return 0

    for i in range(nth-1):
        rfind_index = text.rfind(searchstr, 0, end)
        if rfind_index == -1:
            return 0
        else:
            end = rfind_index

    return end

def keywords_in_context(text, keywords, max_words=5, sep="...", cut_sentences=True):
    """ Returns the relevant context around keywords in a larger text.

    Arguments
    ----------
    text : str
        Text which should be summerized around keywords.
    keywords : list of str
        Keywords whose context we want to extract out of the text.
    max_words : int
        Maximum number of words before und after a keyword if no sentence
        beginning or ending occurs and cut_sentences is set.
    sep : str
        String wich represents skipped portions of the text in the result.
    cut_sentences : bool
        Set if the context around a keyword is cut at the beginning or end of
        a sentence

    Returns
    -------
    Summarised text containing the keywords in context as string.
    """
    indices_lst = []
    for k in keywords:
        start = text.find(k)
        while not start == -1:
            indices_lst.append((k, start))
            start = text.find(k, start+len(k))

    result_indices = set()
    for index_tpl in indices_lst:
        keyword, index = index_tpl
        start = rfind_nth_occurrence(text, " ", nth=max_words+1, endindex=index)
        if not start == 0:
            start += 1 # +1 to Remove the first " "
        end = find_nth_occurrence(text, " ", nth=max_words+1, startindex=index+len(keyword))
        if end == len(text)-1:
            end += 1
        indices_of_text = set(range(start, end))
        if cut_sentences:
            sentence_indices, _ = cut_to_sentence(text, keyword, index)
            indices_of_text.intersection_update(set(sentence_indices))
        for i in indices_of_text:
            result_indices.add(i)

    result_indices = list(result_indices)
    result_indices.sort()

    result = ""
    i_before = -1
    for _i, i in enumerate(result_indices):
        if not (i-1) == i_before:
            result += " " + sep + " " + text[i]
            i_before = i
        else:
            result += text[i]
            i_before = i

        # If the last word is not the end of the text add the sperator.
        if _i == len(result_indices)-1:
            if not i == len(text)-1:
                result += " " + sep

    return result

def find_and_replace(text, find_str, replacement_str):
    """ Find and replace a find_str with a replacement_str in text. """
    start = text.find(find_str)
    offset = 0
    while start != -1:
        # update the index compatible to the whole text
        start = start + offset

        # replace (cut the original word out and insert the replacement)
        text = text[:start] + replacement_str + text[start+len(find_str):]

        offset = start + len(replacement_str)
        start = text[offset:].find(find_str)

    return text


if __name__ == "__main__":

    TEXT = ('Sed ut perspiciatis, unde omnis iste natus error sit voluptatem '
            'accusantium doloremque laudantium, totam rem aperiam eaque '
            'ipsa, quae ab illo inventore veritatis et quasi architecto '
            'beatae vitae dicta sunt, explicabo. Nemo enim ipsam voluptatem, '
            'quia voluptas sit, aspernatur aut odit aut fugit, sed quia '
            'consequuntur magni dolores eos, qui ratione voluptatem sequi '
            'nesciunt, neque porro quisquam est, qui dolorem ipsum, quia '
            'dolor sit amet consectetur adipisci[ng] velit, sed quia non '
            'numquam [do] eius modi tempora inci[di]dunt, ut labore et '
            'dolore magnam aliquam quaerat voluptatem. Ut enim ad minima '
            'veniam, quis nostrum exercitationem ullam corporis suscipit '
            'laboriosam, nisi ut aliquid ex ea commodi consequatur? Quis '
            'autem vel eum iure reprehenderit, qui in ea voluptate velit '
            'esse, quam nihil molestiae consequatur, vel illum, qui dolorem '
            'eum fugiat, quo voluptas nulla pariatur? At vero eos et '
            'accusamus et iusto odio dignissimos ducimus, qui blanditiis '
            'praesentium voluptatum deleniti atque corrupti, quos dolores '
            'et quas molestias excepturi sint, obcaecati cupiditate non '
            'provident, similique sunt in culpa, qui officia deserunt '
            'mollitia animi, id est laborum et dolorum fuga. Et harum quidem '
            'rerum facilis est et expedita distinctio. Nam libero tempore, '
            'cum soluta nobis est eligendi optio, cumque nihil impedit, quo '
            'minus id, quod maxime placeat, facere possimus, omnis voluptas '
            'assumenda est, omnis dolor repellendus. Temporibus autem '
            'quibusdam et aut officiis debitis aut rerum necessitatibus '
            'saepe eveniet, ut et voluptates repudiandae sint et molestiae '
            'non recusandae. Itaque earum rerum hic tenetur a sapiente '
            'delectus, ut aut reiciendis voluptatibus maiores alias '
            'consequatur aut perferendis doloribus asperiores repellat.')

    KEYWORDS = ["Sed", "lorem ipsum", "quo", "recusandae", "doloribus"]

    result_text = keywords_in_context(TEXT, KEYWORDS)
    # Highlight Keywords
    for k in KEYWORDS:
        result_text = find_and_replace(result_text, k, "\x1b[34m"+k+"\x1b[0m")

    print(result_text)
    