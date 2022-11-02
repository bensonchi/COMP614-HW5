"""
COMP 614
Homework 5: Bag of Words
"""

import math
import numpy
import re
import string


def get_title_and_text(filename):
    """
    Given a the name of an XML file, extracts and returns the strings contained 
    between the <title></title> and <text></text> tags.
    """
    title_start = 0
    title_end = 0
    text_start = 0
    text_end = 0
    with open(filename, 'r', encoding='utf-8') as my_file:
        content = my_file.read()

        # search for the start of title string
        title_start_pattern = re.compile("<title(.)*?>")
        title_start_match = title_start_pattern.search(content)
        title_start = title_start_match.end()

        # search for the end of title string
        title_end_pattern = re.compile("</title>")
        title_end_match = title_end_pattern.search(content)
        title_end = title_end_match.start()

        # search for the start of text string
        text_start_pattern = re.compile("<text(.)*?>")
        text_start_match = text_start_pattern.search(content)
        text_start = text_start_match.end()

        # search for the end of text string
        text_end_pattern = re.compile("</text>")
        text_end_match = text_end_pattern.search(content)
        text_end = text_end_match.start()

        title_string, text_string = content[title_start:title_end], content[text_start:text_end]
        title_string = title_string.replace('\n', ' ')
        text_string = text_string.replace('\n', ' ')
    return title_string, text_string


def get_words(text):
    """
    Given the full text of an XML file, filters out the non-body text (text that
    is contained within {{}}, [[]], [], <>, etc.) and punctuation and returns a 
    list of the remaining words, each of which should be converted to lowercase.
    """
    # filtered_string = re.sub('{{(.)*?}}|[[(.)*?]]|[(.)*?]|<(.)*?>', ' ', text)
    filtered_string = re.sub('(?s){{(.)*?}}|\[\[(.)*?\]\]|\[(.)*?\]|<(.)*?>|&lt;(.)*?&gt;|{\|(.)*?\|}', ' ', text)
    filtered_string = re.sub('File', ' ', filtered_string)
    filtered_string = filtered_string.lower()

    punctuation_to_remove = "[" + string.punctuation + "](?![st]\\s)"
    filtered_string = re.sub(punctuation_to_remove, ' ', filtered_string)
    # print(filtered_string)
    output_list = re.split('\s+', filtered_string.strip())
    # print(output_list)
    return output_list


# with open('test_files/test16.xml', 'r', encoding='utf-8') as my_file:
#     content = my_file.read()
#     get_words(content)


def count_words(words):
    """
    Given a list of words, returns the total number of words as well as a 
    dictionary mapping each unique word to its frequency of occurrence.
    """
    word_dict = dict()
    for word in words:
        if word not in word_dict:
            word_dict[word] = 1
        else:
            word_dict[word] += 1
    return len(words), word_dict


def count_all_words(filenames):
    """
    Given a list of filenames, returns three things. First, a list of the titles,
    where the i-th title corresponds to the i-th input filename. Second, a
    dictionary mapping each filename to an inner dictionary mapping each unique
    word in that file to its relative frequency of occurrence. Last, a dictionary 
    mapping each unique word --- including all words found across all files --- 
    to its total frequency of occurrence across all of the input files.
    """
    all_titles = []
    title_to_counter = dict()
    total_counts = dict()
    for filename in filenames:
        title, text = get_title_and_text(filename)
        all_titles.append(title)
        words_list = get_words(text)
        word_count, word_dict = count_words(words_list)
        for word, count in word_dict.items():
            if word not in total_counts:
                total_counts[word] = count
            else:
                total_counts[word] += count
            word_dict[word] = count/word_count
        title_to_counter[title] = word_dict

    return all_titles, title_to_counter, total_counts


def encode_word_counts(all_titles, title_to_counter, total_counts, num_words):
    """
    Given two dictionaries in the format output by count_all_words and an integer
    num_words representing the number of top words to encode, finds the top 
    num_words words in total_counts and builds a matrix where the element in 
    position (i, j) is the relative frequency of occurrence of the j-th most 
    common overall word in the i-th article (i.e., the article corresponding to 
    the i-th title in titles).
    """

    return numpy.matrix([[]])


def nearest_neighbors(matrix, all_titles, title, num_nbrs):
    """
    Given a matrix, a list of all titles whose data is encoded in the matrix, such
    that the i-th title corresponds to the i-th row, a single title whose data is
    encoded in the matrix, and the desired number of neighbors to be found, finds 
    and returns the closest neighbors to the article with the given title.
    """
    return []


def run():
    """
    Encodes the wikipedia dataset into a matrix, prompts the user to choose an
    article, and then runs the knn algorithm to find the 5 nearest neighbors
    of the chosen article.
    """
    # Encode the wikipedia dataset in a matrix
    # filenames = comp614_module5.ALL_FILES
    filenames = ''
    all_titles, title_to_counter, total_counts = count_all_words(filenames)
    mat = encode_word_counts(all_titles, title_to_counter, total_counts, 20000)

    # Print all articles
    print("Enter the integer corresponding to the article whose nearest" +
          " neighbors you would like to find. Your options are:")
    for idx in range(len(all_titles)):
        print("\t" + str(idx) + ". " + all_titles[idx])

    # Prompt the user to choose an article
    while True:
        choice = input("Enter your choice here: ")
        try:
            choice = int(choice)
            break
        except ValueError:
            print("Error: you must enter an integer between 0 and " +
                  str(len(all_titles) - 1) + ", inclusive.")

    # Compute and print the results
    nbrs = nearest_neighbors(mat, all_titles, all_titles[choice], 5)
    print("\nThe 5 nearest neighbors of " + all_titles[choice] + " are:")
    for nbr in nbrs:
        print("\t" + nbr)


# Leave the following line commented when you submit your code to OwlTest/CanvasTest,
# but uncomment it to perform the analysis for the discussion questions.
# run()
