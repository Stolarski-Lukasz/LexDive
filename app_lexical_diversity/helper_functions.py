import nltk
from nltk.stem import WordNetLemmatizer

def lemmatize_list_of_words(list_of_words):
    lemmatizer = WordNetLemmatizer()
    sentence_tagged = nltk.pos_tag(list_of_words)
    sentence_as_lemmas = []
    for pair in sentence_tagged:
        # dealing with pronouns
        if pair[0] == "me" or pair[0] == "my" or (pair[0] == "mine" and pair[1] != "NN"):
            sentence_as_lemmas.append("I")
        elif pair[0] == "your" or pair[0] == "yours":
            sentence_as_lemmas.append("you")
        elif pair[0] == "him" or pair[0] == "his":
            sentence_as_lemmas.append("he")
        elif pair[0] == "her" or pair[0] == "hers":
            sentence_as_lemmas.append("she")
        elif pair[0] == "its":
            sentence_as_lemmas.append("it")
        elif pair[0] == "us" or pair[0] == "our" or pair[0] == "ours":
            sentence_as_lemmas.append("we")
        elif pair[0] == "them" or pair[0] == "their" or pair[0] == "theirs":
            sentence_as_lemmas.append("they")
        # dealing with articles
        elif pair[0] == "an":
            sentence_as_lemmas.append("a")
        # major parts of speech
        elif pair[1] == "JJ" or pair[1] == "JJR" or pair[1] == "JJS":
            lemma = lemmatizer.lemmatize(pair[0], "a")
            sentence_as_lemmas.append(lemma)
        elif pair[1] == "VB" or pair[1] == "VBD" or pair[1] == "VBG" or pair[1] == "VBN" or pair[
            1] == "VBP" or \
                        pair[
                            1] == "VBZ":
            lemma = lemmatizer.lemmatize(pair[0], "v")
            sentence_as_lemmas.append(lemma)
        elif pair[1] == "NN" or pair[1] == "NNP" or pair[1] == "NNS":
            lemma = lemmatizer.lemmatize(pair[0], "n")
            sentence_as_lemmas.append(lemma)
        elif pair[1] == "RB" or pair[1] == "RBR" or pair[1] == "RBS":
            lemma = lemmatizer.lemmatize(pair[0], "r")
            sentence_as_lemmas.append(lemma)
        else:
            sentence_as_lemmas.append(pair[0])
    return sentence_as_lemmas


def get_subsamples_list(intended_text, size_of_subsamples, number_of_samples, number_of_tokens_in_intended_sample):
    word_counter = 1
    words_processed_counter = 1
    subsamples_counter = 1
    subsamples_list = []
    subsample = []
    subsample_number = 1
    switch = ""
    # the loop and the conditional statements below are only for obaining the list of individual subsamples
    for word in intended_text:
        if subsamples_counter <= number_of_samples:
            if word_counter <= size_of_subsamples:
                subsample.append(word)
                word_counter += 1
                words_processed_counter += 1
                switch = "normal"
            else:
                single_result = []
                single_result.append(subsample_number)
                single_result.append(subsample)
                subsamples_list.append(single_result)
                word_counter = 2
                subsamples_counter += 1
                subsample = []
                subsample.append(word)
                subsample_number += 1
                words_processed_counter += 1
                switch = "ending"
    if switch == "normal":
        single_result = []
        single_result.append(subsample_number)
        single_result.append(subsample)
        subsamples_list.append(single_result)
    elif switch == "ending":
        missing_tokens_in_last_subsample = (number_of_tokens_in_intended_sample - words_processed_counter) + 2
        single_result = []
        single_result.append(subsample_number)
        subsample = intended_text[missing_tokens_in_last_subsample * -1:]
        single_result.append(subsample)
        subsamples_list.append(single_result)

    return subsamples_list


def get_ordinal_ending(equal_text_beginning_as_string):
    beginning_word_ordinal_ending = ""
    if equal_text_beginning_as_string[-1:] == "1":
        beginning_word_ordinal_ending = "st"
    elif equal_text_beginning_as_string[-1:] == "2":
        beginning_word_ordinal_ending = "nd"
    elif equal_text_beginning_as_string[-1:] == "3":
        beginning_word_ordinal_ending = "rd"
    else:
        beginning_word_ordinal_ending = "th"

    return beginning_word_ordinal_ending