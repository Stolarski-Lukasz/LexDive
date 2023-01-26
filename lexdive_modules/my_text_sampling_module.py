from itertools import cycle, compress
from abc import ABC, abstractclassmethod

# Interfaces
############
class SamplingProcessor(ABC):

    @abstractclassmethod
    def sample_text(self, user_text_list):
        pass


# Concrete classes from Interfaces
##################################
class SplitTextSamplingProcessor(SamplingProcessor):

    def __init__(self, intended_text_length, size_of_subsamples, number_of_tokens):
        self.intended_text_length = intended_text_length
        self.size_of_subsamples = size_of_subsamples
        self.number_of_tokens = number_of_tokens
        self.number_of_samples = 0
        self.gap_size = 0
        # self.number_of_tokens_in_intended_sample = 0
        # self.number_of_types_in_intended_sample = 0

    def sample_text(self, user_text_list):
        self.number_of_samples = self.intended_text_length / self.size_of_subsamples
        self.gap_size = (self.number_of_tokens - self.intended_text_length) / self.number_of_samples
        criteria = cycle(
            [True] * int(self.size_of_subsamples) + [False] * int(self.gap_size))
        intended_text = list(compress(user_text_list, criteria))
        intended_text = intended_text[:self.intended_text_length]
        # self.number_of_tokens_in_intended_sample = len(intended_text)
        # self.number_of_types_in_intended_sample = len(set(intended_text))
        return intended_text


class EqualTextSamplingProcessor(SamplingProcessor):

    def __init__(self, equal_text_beginning, equal_text_length):
        self.equal_text_beginning = equal_text_beginning
        self.equal_text_length = equal_text_length
        # self.number_of_tokens_in_intended_sample = 0
        # self.number_of_types_in_intended_sample = 0
        

    def sample_text(self, user_text_list):
        equal_text = user_text_list[self.equal_text_beginning-1:self.equal_text_length+(self.equal_text_beginning-1)]
        # self.number_of_tokens_in_intended_sample = len(equal_text)
        # self.number_of_types_in_intended_sample = len(set(equal_text))
        return equal_text


# Other classes
###############
class AuxiliarySamplingProcessor():

    # this method is only for the outcome of SplitTextSamplingProcessor - may be removed there later
    def get_subsamples_list(self, intended_text, size_of_subsamples, number_of_samples):
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
            missing_tokens_in_last_subsample = (self.number_of_tokens_in_intended_sample - words_processed_counter) + 2
            single_result = []
            single_result.append(subsample_number)
            subsample = intended_text[missing_tokens_in_last_subsample * -1:]
            single_result.append(subsample)
            subsamples_list.append(single_result)

        return subsamples_list

    # this method is only for the outcome of EqualTextSamplingProcessor - may be removed there later
    def get_ordinal_ending(self, equal_text_beginning_as_string):
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