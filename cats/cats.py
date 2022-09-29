"""Typing test implementation"""

from hashlib import new
import math
from utils import lower, split, remove_punctuation, lines_from_file
from ucb import main, interact, trace
from datetime import datetime
import string


###########
# Phase 1 #
###########


def pick(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns True. If there are fewer than K such paragraphs, return
    the empty string.

    Arguments:
        paragraphs: a list of strings
        select: a function that returns True for paragraphs that can be selected
        k: an integer

    >>> ps = ['hi', 'how are you', 'fine']
    >>> s = lambda p: len(p) <= 4
    >>> pick(ps, s, 0)
    'hi'
    >>> pick(ps, s, 1)
    'fine'
    >>> pick(ps, s, 2)
    ''
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    new_lst = []
    for ele in paragraphs:
        if select(ele):
            new_lst.append(ele)
    if k <= len(new_lst) - 1:
        return new_lst[k]
    else:
        return ''
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether
    a paragraph contains one of the words in TOPIC.

    Arguments:
        topic: a list of words related to a subject

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> pick(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def select(paragraph):
        paragraph = ''.join([i for i in paragraph if i not in string.punctuation])
        sp_lst = paragraph.split()
        for ele in sp_lst:
            if ele.lower() in topic:
                return True
        return False
    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    Arguments:
        typed: a string that may contain typos
        reference: a string without errors

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    >>> accuracy('', '')
    100.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    ind = 0
    total_num = len(typed_words)
    acc_num = 0
    if total_num == 0:
        if len(reference_words) == 0:
            return 100.0
        else:
            return 0.0
    for words in typed_words[:len(reference_words)]:
        if words == reference_words[ind]:
            acc_num += 1
        ind += 1
    return 100 * acc_num / total_num
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string.

    Arguments:
        typed: an entered string
        elapsed: an amount of time in seconds

    >>> wpm('hello friend hello buddy hello', 15)
    24.0
    >>> wpm('0123456789',60)
    2.0
    """
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    return len(typed) * 12 / elapsed
    # END PROBLEM 4


###########
# Phase 2 #
###########

def autocorrect(typed_word, word_list, diff_function, limit):
    """Returns the element of WORD_LIST that has the smallest difference
    from TYPED_WORD. Instead returns TYPED_WORD if that difference is greater
    than LIMIT.

    Arguments:
        typed_word: a string representing a word that may contain typos
        word_list: a list of strings representing reference words
        diff_function: a function quantifying the difference between two words
        limit: a number

    >>> ten_diff = lambda w1, w2, limit: 10 # Always returns 10
    >>> autocorrect("hwllo", ["butter", "hello", "potato"], ten_diff, 20)
    'butter'
    >>> first_diff = lambda w1, w2, limit: (1 if w1[0] != w2[0] else 0) # Checks for matching first char
    >>> autocorrect("tosting", ["testing", "asking", "fasting"], first_diff, 10)
    'testing'
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    return_word = typed_word
    small_diff = limit + 0.001
    for word in word_list:
        if word == typed_word:
            return word
        if diff_function(typed_word, word, limit) < small_diff:
            small_diff = diff_function(typed_word, word, limit)
            return_word = word
    return return_word
    # END PROBLEM 5


def feline_fixes(typed, reference, limit):
    """A diff function for autocorrect that determines how many letters
    in TYPED need to be substituted to create REFERENCE, then adds the difference in
    their lengths and returns the result.

    Arguments:
        typed: a starting word
        reference: a string representing a desired goal word
        limit: a number representing an upper bound on the number of chars that must change

    >>> big_limit = 10
    >>> feline_fixes("nice", "rice", big_limit)    # Substitute: n -> r
    1
    >>> feline_fixes("range", "rungs", big_limit)  # Substitute: a -> u, e -> s
    2
    >>> feline_fixes("pill", "pillage", big_limit) # Don't substitute anything, length difference of 3.
    3
    >>> feline_fixes("roses", "arose", big_limit)  # Substitute: r -> a, o -> r, s -> o, e -> s, s -> e
    5
    >>> feline_fixes("rose", "hello", big_limit)   # Substitute: r->h, o->e, s->l, e->l, length difference of 1.
    5
    """
    # BEGIN PROBLEM 6
    if limit == -1:
        return 0
    elif len(typed) == 0 or len(reference) == 0:
        return abs(len(typed) - len(reference))
    elif typed[0] == reference[0]:
        return feline_fixes(typed[1:], reference[1:], limit)
    else:
        return 1 + feline_fixes(typed[1:], reference[1:], limit - 1)
    # END PROBLEM 6


def hidden_kittens(typed, reference, limit):
    """A diff function that returns the number of times REFERENCE appears as a
    (potentially non-continuous) substring of TYPED. If REFERENCE appears 0 or > LIMIT times
    within TYPED, return a number greater than LIMIT.

    Arguments:
        typed: a starting word
        reference: a string representing a desired goal word
        limit: a number representing an upper bound on the number of substrings found

    >>> limit = 5
    >>> hidden_kittens("ccatgts", "cats", limit)
    4
    >>> hidden_kittens("123123123", "123", limit) > limit # 123 appears 10 times in 123123123
    True
    >>> hidden_kittens("hiddnehddi", "hidden", limit) > limit # hidden appears 0 times in hiddnehddi
    True
    """
    # BEGIN PROBLEM 7
    "*** YOUR CODE HERE ***"
    def helper(typed, reference, limit):
        if reference == '':
            return 1
        elif typed == '':
            return 0
        elif typed[0] == reference[0]:
            return helper(typed[1:], reference[1:], limit - 1) + helper(typed[1:], reference, limit - 1)
        else:
            return helper(typed[1:], reference, limit)
    if helper(typed, reference, limit) == 0:
        return limit + 1
    else:
        return helper(typed, reference, limit)
    # END PROBLEM 7


def final_diff(typed, reference, limit):
    """A diff function that takes in a string TYPED, a string REFERENCE, and a number LIMIT.
    If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function.'


FINAL_DIFF_LIMIT = 6  # REPLACE THIS WITH YOUR LIMIT


###########
# Phase 3 #
###########


def report_progress(typed, prompt, user_id, upload):
    """Upload a report of your id and progress so far to the multiplayer server.
    Returns the progress so far.

    Arguments:
        typed: a list of the words typed so far
        prompt: a list of the words in the typing prompt
        user_id: a number representing the id of the current user
        upload: a function used to upload progress to the multiplayer server

    >>> print_progress = lambda d: print('ID:', d['id'], 'Progress:', d['progress'])
    >>> # The above function displays progress in the format ID: __, Progress: __
    >>> print_progress({'id': 1, 'progress': 0.6})
    ID: 1 Progress: 0.6
    >>> typed = ['how', 'are', 'you']
    >>> prompt = ['how', 'are', 'you', 'doing', 'today']
    >>> report_progress(typed, prompt, 2, print_progress)
    ID: 2 Progress: 0.6
    0.6
    >>> report_progress(['how', 'aree'], prompt, 3, print_progress)
    ID: 3 Progress: 0.2
    0.2
    """
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    corr = 0
    for i in range(len(typed)):
        if typed[i] == prompt[i]:
            corr += 1
        else:
            break
    ratio = corr / len(prompt)
    print('ID: ' + str(user_id) + ' Progress: ' + str(ratio))
    return ratio
    # END PROBLEM 8


def time_per_word(words, times_per_player):
    """Given timing data, return a match dictionary, which contains a
    list of words and the amount of time each player took to type each word.

    Arguments:
        words: a list of words, in the order they are typed.
        times_per_player: A list of lists of timestamps including the time
                          the player started typing, followed by the time
                          the player finished typing each word.

    >>> p = [[75, 81, 84, 90, 92], [19, 29, 35, 36, 38]]
    >>> match = time_per_word(['collar', 'plush', 'blush', 'repute'], p)
    >>> match["words"]
    ['collar', 'plush', 'blush', 'repute']
    >>> match["times"]
    [[6, 3, 6, 2], [10, 6, 1, 2]]
    """
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    word_lst = words
    time_lst = []
    for i in range(len(times_per_player)):
        time_lst.append(times_per_player[i][:-1])
    for i in range(len(time_lst)):
        for j in range(len(time_lst[i])):
            time_lst[i][j] = times_per_player[i][j + 1] - times_per_player[i][j]
    
    dcry = {
        'words': word_lst,
        'times': time_lst 
    }
    return dcry
    # END PROBLEM 9


def fastest_words(match):
    """Return a list of lists of which words each player typed fastest.

    Arguments:
        match: a match dictionary as returned by time_per_word.

    >>> p0 = [5, 1, 3]
    >>> p1 = [4, 1, 6]
    >>> fastest_words(match(['Just', 'have', 'fun'], [p0, p1]))
    [['have', 'fun'], ['Just']]
    >>> p0  # input lists should not be mutated
    [5, 1, 3]
    >>> p1
    [4, 1, 6]
    """
    player_indices = range(len(match["times"]))  # contains an *index* for each player
    word_indices = range(len(match["words"]))    # contains an *index* for each word
    # BEGIN PROBLEM 10
    "*** YOUR CODE HERE ***"
    return_lst = []
    for _ in range(len(match['times'])):
        return_lst.append([])
    for i in range(len(match['times'][0])):
        lst = [ele[i] for ele in match['times']]
        min_value = min(lst)
        min_index = lst.index(min_value)
        return_lst[min_index].append(match['words'][i])
    return return_lst
    # END PROBLEM 10


def match(words, times):
    """A dictionary containing all words typed and their times.

    Arguments:
        words: A list of strings, each string representing a word typed.
        times: A list of lists for how long it took for each player to type
            each word.
            times[i][j] = time it took for player i to type words[j].

    Example input:
        words: ['Hello', 'world']
        times: [[5, 1], [4, 2]]
    """
    assert all([type(w) == str for w in words]), 'words should be a list of strings'
    assert all([type(t) == list for t in times]), 'times should be a list of lists'
    assert all([isinstance(i, (int, float)) for t in times for i in t]), 'times lists should contain numbers'
    assert all([len(t) == len(words) for t in times]), 'There should be one word per time.'
    return {"words": words, "times": times}


def get_word(match, word_index):
    """A utility function that gets the word with index word_index"""
    assert 0 <= word_index < len(match["words"]), "word_index out of range of words"
    return match["words"][word_index]


def time(match, player_num, word_index):
    """A utility function for the time it took player_num to type the word at word_index"""
    assert word_index < len(match["words"]), "word_index out of range of words"
    assert player_num < len(match["times"]), "player_num out of range of players"
    return match["times"][player_num][word_index]


def match_string(match):
    """A helper function that takes in a match dictionary and returns a string representation of it"""
    return f"match({match['words']}, {match['times']})"


enable_multiplayer = False  # Change to True when you're ready to race.

##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = pick(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
