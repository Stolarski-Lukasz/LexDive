from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from nltk import pos_tag

from .app_text_statistics_module import TextStatisticsProcessor, LemmatizationProcessor



@csrf_exempt
def count_tokens(request):
    user_text_split = TextStatisticsProcessor().split_text(request)
    number_of_tokens = len(user_text_split)
    data = {'result': number_of_tokens}
    return JsonResponse(data)


@csrf_exempt
def count_types(request):
    text_statistics_processor = TextStatisticsProcessor()
    user_text_split = text_statistics_processor.split_text(request)
    types_count_listoftuples = text_statistics_processor.count_types(user_text_split)
    ranked_types_listoflists = text_statistics_processor.rank_types(types_count_listoftuples)
    data = {'types_list': ranked_types_listoflists}
    return JsonResponse(data)


@csrf_exempt
def count_lemmas(request):
    text_statistics_processor = TextStatisticsProcessor()
    user_text_split = text_statistics_processor.split_text(request)
    user_text_tagged = pos_tag(user_text_split)
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text_tagged(user_text_tagged)
    lemmatization_processor.get_lexeme_list()
    lemmatization_processor.add_rank_to_lexeme_list()
    data = {'lemmas_list': lemmatization_processor.complete_lexeme_list}
    return JsonResponse(data)