from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
import operator


# Create your views here.
@csrf_exempt
def count_tokens(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    user_text = user_text.split()
    number_of_tokens = len(user_text)
    data = {'result': number_of_tokens}
    return JsonResponse(data)



@csrf_exempt
def count_types(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    user_text = user_text.split()
    list_of_types = set(user_text)
    number_of_types = len(list_of_types)

    # arranging types
    types_dict = {}
    def get_type_list(some_list):
        for word in some_list:
            if word in types_dict:
                types_dict[word] += 1
            else:
                types_dict[word] = 1
        resulting_list = sorted(types_dict.items(), key=operator.itemgetter(1), reverse=True)
        return resulting_list

    types_list = get_type_list(user_text)

    # change types_list to lists of lists and add rank of type
    rank = 1
    complete_types_list = []
    for element in types_list:
        addition = []
        addition.append(rank)
        addition.append(element[0])
        addition.append(element[1])
        complete_types_list.append(addition) 
        rank += 1
    data = {'types_list': complete_types_list}
    return JsonResponse(data)


  
lemmatizer = WordNetLemmatizer()
@csrf_exempt
def count_lemmas(request):
    user_text = request.POST.dict()
    user_text = user_text['user_text']
    user_text = user_text.split()
    
    user_text_tagged = pos_tag(user_text)
    sentence_as_lemmas = []
    for pair in user_text_tagged:

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
            lemma = lemmatizer.lemmatize(pair[0], "n")
            sentence_as_lemmas.append(lemma)
        else:
            sentence_as_lemmas.append(pair[0])


    lexemes_dict = {}
    for word in sentence_as_lemmas:
        if word in lexemes_dict:
            lexemes_dict[word] += 1
        else:
            lexemes_dict[word] = 1
    lexeme_list = sorted(lexemes_dict.items(), key=operator.itemgetter(1), reverse=True)

    # change types_list to lists of lists and add rank of type
    rank = 1
    complete_lexeme_list = []
    for element in lexeme_list:
        addition = []
        addition.append(rank)
        addition.append(element[0])
        addition.append(element[1])
        complete_lexeme_list.append(addition) 
        rank += 1
    
    data = {'lemmas_list': complete_lexeme_list}
    return JsonResponse(data)