import operator
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


class LemmatizationProcessor:

    def __init__(self):
        self.text_as_lemmas = []
        self.lexemes_dict = {}
        self.lexeme_list = []
        self.complete_lexeme_list = []

    def lemmatize_text(self, user_text_list):
        user_text_tagged = nltk.pos_tag(user_text_list)
        for pair in user_text_tagged:
            # dealing with pronouns
            if pair[0] == "me" or pair[0] == "my" or (pair[0] == "mine" and pair[1] != "NN"):
                self.text_as_lemmas.append("I")
            elif pair[0] == "your" or pair[0] == "yours":
                self.text_as_lemmas.append("you")
            elif pair[0] == "him" or pair[0] == "his":
                self.text_as_lemmas.append("he")
            elif pair[0] == "her" or pair[0] == "hers":
                self.text_as_lemmas.append("she")
            elif pair[0] == "its":
                self.text_as_lemmas.append("it")
            elif pair[0] == "us" or pair[0] == "our" or pair[0] == "ours":
                self.text_as_lemmas.append("we")
            elif pair[0] == "them" or pair[0] == "their" or pair[0] == "theirs":
                self.text_as_lemmas.append("they")
            # dealing with articles
            elif pair[0] == "an":
                self.text_as_lemmas.append("a")
            # major parts of speech
            elif pair[1] == "JJ" or pair[1] == "JJR" or pair[1] == "JJS":
                lemma = lemmatizer.lemmatize(pair[0], "a")
                self.text_as_lemmas.append(lemma)
            elif pair[1] == "VB" or pair[1] == "VBD" or pair[1] == "VBG" or pair[1] == "VBN" or pair[
                1] == "VBP" or \
                            pair[
                                1] == "VBZ":
                lemma = lemmatizer.lemmatize(pair[0], "v")
                self.text_as_lemmas.append(lemma)
            elif pair[1] == "NN" or pair[1] == "NNP" or pair[1] == "NNS":
                lemma = lemmatizer.lemmatize(pair[0], "n")
                self.text_as_lemmas.append(lemma)
            elif pair[1] == "RB" or pair[1] == "RBR" or pair[1] == "RBS":
                lemma = lemmatizer.lemmatize(pair[0], "r")
                self.text_as_lemmas.append(lemma)
            else:
                self.text_as_lemmas.append(pair[0])
        return self.text_as_lemmas

    def get_lexeme_list(self):
        for word in self.text_as_lemmas:
            if word in self.lexemes_dict:
                self.lexemes_dict[word] += 1
            else:
                self.lexemes_dict[word] = 1
        self.lexeme_list = sorted(self.lexemes_dict.items(), key=operator.itemgetter(1), reverse=True)

    def add_rank_to_lexeme_list(self):
        rank = 1
        for element in self.lexeme_list:
            addition = []
            addition.append(rank)
            addition.append(element[0])
            addition.append(element[1])
            self.complete_lexeme_list.append(addition) 
            rank += 1