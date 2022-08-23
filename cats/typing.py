"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1

    if k >= len(paragraphs):
        return ''

    if not select(paragraphs[k]):
        paragraphs.remove(paragraphs[k])
        return choose(paragraphs, select, k)


    return paragraphs[k]
    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    # assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2

    def select(sentence):
        sentence = remove_punctuation(sentence)  # removes punctuation
        sentence = lower(sentence)               # lowers the sentence
        words_list = split(sentence)             # splits the sentence

        for word in words_list:
            for keywords in topic:
                if word == keywords:
                    return True

        return False

    return select
    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

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
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    correct_attempts = 0
    total_attempts   = 0

    if typed_words == []:
        return 0.0

    if len(typed_words) > len(reference_words):
        for i in range(len(typed_words) - len(reference_words)):
            reference_words.append([])

    if len(typed_words) < len(reference_words):
        for i in range(len(reference_words) - len(typed_words)):
            reference_words.remove(reference_words[-1])

    for k in range(len(typed_words)):
        total_attempts += 1
        if typed_words[k] == reference_words[k]:
            correct_attempts += 1


    return correct_attempts / total_attempts * 100
    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4

    num_of_chars = len(typed)
    num_of_words = num_of_chars / 5
    words_per_minute = num_of_words / elapsed * 60
    return words_per_minute
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5

    diff_list = []

    for i in range(len(valid_words)):
        if user_word == valid_words[i]:
            return user_word

        diff_list.append(diff_function(user_word, valid_words[i], limit))

    correct = diff_list.index(min(diff_list))

    if min(diff_list) > limit:
        return user_word

    return valid_words[correct]
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # assert False, 'Remove this line'
    # BEGIN PROBLEM 6
    checker = -1
    diff    = 0
    blank   = " "

    def spelling_check(start, goal, checker, diff, limit):

        checker += 1
        # print(start, goal, checker, diff, limit)
        if len(start) < len(goal):
            start += blank

        if len(start) > len(goal):
            goal += blank

        if checker == len(goal):
            return diff

        if start[checker] != goal[checker]:
            diff += 1
            start = start[:checker] + goal[checker] + start[checker + 1:]

        if diff > limit:
            return limit + 1

        return spelling_check(start, goal, checker, diff, limit)


    return spelling_check(start, goal, checker, diff, limit)

    # END PROBLEM 6

def edit_diff(start, goal, limit):
    """A diff function that computes the edit distance from START to GOAL."""
    # assert False, 'Remove this line'

    # diff    = 0
    # counter = 1
    # blank   = " "

    # def diff_checker(start, goal, counter, limit, diff):

    #     add_start        = start[:counter - 1] + goal[counter - 1] + start[counter - 1:]
    #     remove_start     = start[:counter - 1]                     + start[counter:]
    #     substitute_start = start[:counter - 1] + goal[counter - 1] + start[counter:]
    #     start_list       = [add_start, substitute_start, remove_start]

    #     add_diff         = swap_diff(add_start, goal, limit) 
    #     remove_diff      = swap_diff(remove_start, goal, limit)
    #     substitute_diff  = swap_diff(substitute_start, goal, limit)
    #     diff_list        = [add_diff, substitute_diff, remove_diff]

    #     # print(counter, diff, diff_list, start_list)

    #     if len(start) < len(goal):
    #         start += blank

    #     if len(start) > len(goal):
    #         goal += blank

    #     if diff > limit:
    #         return limit + 1

    #     if start == goal:
    #         return diff

    #     if start[counter - 1] == goal[counter - 1]:
    #         counter += 1
    #         return diff_checker(start, goal, counter, limit, diff)

    #     if start[counter - 1] != goal[counter - 1]:
    #         diff += 1
    #         return diff_checker(start_list[diff_list.index(min(diff_list))], goal, counter, limit, diff)

    # return diff_checker(start, goal, counter, limit, diff)

    diff    = 0
    blank   = " "

    def diff_checker(start, goal, limit, diff):

        if len(start) == 0:
            start += blank

        if len(goal) == 0:
            goal += blank

        add_start        = goal[0] + start[0:]
        remove_start     = start[1:]
        substitute_start = goal[0] + start[1:]
        start_list       = [add_start, substitute_start, remove_start]

        add_diff         = swap_diff(add_start, goal, limit) 
        remove_diff      = swap_diff(remove_start, goal, limit)
        substitute_diff  = swap_diff(substitute_start, goal, limit)
        diff_list        = [add_diff, substitute_diff, remove_diff]

        if diff > limit:
            return limit + 1

        if start == goal:
            return diff

        if start[-1] == goal[-1]:
            return diff_checker(start[:-1], goal[:-1], limit, diff)

        if start[0] == goal[0]:
            return diff_checker(start[1:], goal[1:], limit, diff)

        diff += 1

        return diff_checker(start_list[diff_list.index(min(diff_list))], goal, limit, diff)

    return diff_checker(start, goal, limit, diff)


# def final_diff(start, goal, limit):
#     """A diff function. If you implement this function, it will be used."""
#     assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8

    blank    = " "
    progress = 0

    for i in range(len(prompt)):
        if len(typed) < len(prompt):
            typed.append(blank)

        if typed[i] != prompt[i]:
            break

        progress += 1

    player = {'id': id, 'progress': progress/len(prompt) }
    send(player)

    return progress/len(prompt)
    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9

    fastest_words_list = []
    elapsed_times_list  = []

    for i in range(n_words):
        elapsed_times_list.append([])

    for i in range(n_players):
        fastest_words_list.append([])

    for i in range(n_players):
        for j in range(n_words):
            elapsed_times_list[j].append(elapsed_time(word_times[i][j + 1]) - elapsed_time(word_times[i][j]))


    for i in range(len(elapsed_times_list)):
        times = elapsed_times_list[i]
        for j in range(len(times)):
            if min(times) + margin > times[j]:
                fastest_words_list[j].append(word(word_times[0][index_times + 1]))
    

    return fastest_words_list

    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


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
        reference = choose(paragraphs, select, i)
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