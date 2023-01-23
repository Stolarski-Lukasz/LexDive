from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from nltk import pos_tag

from lexdive_modules.my_request_module import RequestProcessor
from lexdive_modules.my_text_statistics_module import TextStatisticsProcessor
from lexdive_modules.my_lemmatization_module import LemmatizationProcessor




@csrf_exempt
def count_tokens(request):
    user_text_split = RequestProcessor().split_text(request)
    number_of_tokens = len(user_text_split)
    data = {'result': number_of_tokens}
    return JsonResponse(data)


@csrf_exempt
def count_types(request):
    user_text_split = RequestProcessor().split_text(request)
    text_statistics_processor = TextStatisticsProcessor()
    types_count_listoftuples = text_statistics_processor.count_types(user_text_split)
    ranked_types_listoflists = text_statistics_processor.rank_types(types_count_listoftuples)
    data = {'types_list': ranked_types_listoflists}
    return JsonResponse(data)


@csrf_exempt
def count_lemmas(request):
    user_text_split = RequestProcessor().split_text(request)
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_split)
    lemmatization_processor.get_lexeme_list()
    lemmatization_processor.add_rank_to_lexeme_list()
    data = {'lemmas_list': lemmatization_processor.complete_lexeme_list}
    return JsonResponse(data)
