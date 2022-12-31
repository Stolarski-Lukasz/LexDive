import operator
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()


class TextStatisticsProcessor:

    def split_text(self, request):
        user_text = request.POST.dict()
        user_text = user_text['user_text']
        return user_text.split()

    def count_types(self, user_text_split):
        types_dict = {}
        for word in user_text_split:
            if word in types_dict:
                types_dict[word] += 1
            else:
                types_dict[word] = 1
        types_listoftuples = sorted(types_dict.items(), key=operator.itemgetter(1), reverse=True)
        return types_listoftuples

    def rank_types(self, types_list):
        rank = 1
        ranked_types_listoflists = []
        for element in types_list:
            addition = []
            addition.append(rank)
            addition.append(element[0])
            addition.append(element[1])
            ranked_types_listoflists.append(addition) 
            rank += 1
        return ranked_types_listoflists


class LemmatizationProcessor:

    def __init__(self):
        self.sentence_as_lemmas = []
        self.lexemes_dict = {}
        self.lexeme_list = []
        self.complete_lexeme_list = []

    def _lemmatize_pronouns(self, pair):
        if pair[0] == "me" or pair[0] == "my" or (pair[0] == "mine" and pair[1] != "NN"):
            self.sentence_as_lemmas.append("I")
        elif pair[0] in ["your", "yours"]:
            self.sentence_as_lemmas.append("you")
        elif pair[0] in ["him", "his"]:
            self.sentence_as_lemmas.append("he")
        elif pair[0] in ["her", "hers"]:
            self.sentence_as_lemmas.append("she")
        elif pair[0] == "its":
            self.sentence_as_lemmas.append("it")
        elif pair[0] in ["us", "our", "ours"]:
            self.sentence_as_lemmas.append("we")
        elif pair[0] in ["them", "their", "theirs"]:
            self.sentence_as_lemmas.append("they")

    def _lemmatize_articles(self, pair):
        if pair[0] == "an":
            self.sentence_as_lemmas.append("a")
    
    def _lemmatize_major_parts_of_speech(self, pair):
        if pair[1] in ["JJ", "JJR", "JJS"]:
            lemma = lemmatizer.lemmatize(pair[0], "a")
            self.sentence_as_lemmas.append(lemma)
        elif pair[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
            lemma = lemmatizer.lemmatize(pair[0], "v")
            self.sentence_as_lemmas.append(lemma)
        elif pair[1] in ["NN", "NNP", "NNS"]:
            lemma = lemmatizer.lemmatize(pair[0], "n")
            self.sentence_as_lemmas.append(lemma)
        elif pair[1] in ["RB", "RBR", "RBS"]:
            lemma = lemmatizer.lemmatize(pair[0], "n")
            self.sentence_as_lemmas.append(lemma)
        else:
            self.sentence_as_lemmas.append(pair[0])

    def lemmatize_text_tagged(self, user_text_tagged):
        for pair in user_text_tagged:
            self._lemmatize_pronouns(pair)
            self._lemmatize_articles(pair)
            self._lemmatize_major_parts_of_speech(pair)

    def get_lexeme_list(self):
        for word in self.sentence_as_lemmas:
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

    

    

