import numpy as np
from abc import ABC, abstractclassmethod

# Interfaces
############
class LexicalDiversityProcessor(ABC):

    @abstractclassmethod
    def calculate_lexical_diversity(self, user_text_split):
        pass


# Concrete classes
##################
class MtldProcessor(LexicalDiversityProcessor):

    def __init__(self):
        self.number_of_tokens = 0
        self.factor_count_with_remainder = 0
        self.factor_count_with_remainder_forward = 0
        self.factor_count_with_remainder_backward = 0
        self.mtld_score_forward = 0
        self.mtld_score_backward = 0
        self.mtld_mean = 0
        
        
    def _mtld_singlerun(self, user_text_split):
        self.number_of_tokens = len(user_text_split)
        segment_ttr = 1
        lengths_of_segments = []
        segment_list = []
        segment_types = []
        segment_tokens = []
        for word in user_text_split:
            if segment_ttr <= 0.72:
                lengths_of_segments.append(len(segment_list))
                segment_ttr = 1
                segment_list = []
            segment_list.append(word)
            segment_types = len(set(segment_list))
            segment_tokens = len(segment_list)
            segment_ttr = segment_types / segment_tokens
        result_for_calculation = 1-segment_ttr
        remainder_segment_percentage_ttr = result_for_calculation/0.28
        self.factor_count_with_remainder = len(lengths_of_segments) + remainder_segment_percentage_ttr
        mtld_score = self.number_of_tokens/self.factor_count_with_remainder
        return mtld_score

    def calculate_lexical_diversity(self, user_text_split):
        # forward processing
        self.mtld_score_forward = self._mtld_singlerun(user_text_split=user_text_split)
        self.factor_count_with_remainder_forward = self.factor_count_with_remainder
        
        
        # backward processing
        user_text_split = user_text_split[::-1]
        self.mtld_score_backward = self._mtld_singlerun(user_text_split=user_text_split)
        self.factor_count_with_remainder_backward = self.factor_count_with_remainder
        
        # calculating mean mtld
        mtld_scores = [self.mtld_score_forward, self.mtld_score_backward]   
        self.mtld_mean = np.mean(mtld_scores)