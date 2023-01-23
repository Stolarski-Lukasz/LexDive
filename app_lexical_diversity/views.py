from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from itertools import cycle, compress
import math
import numpy as np

from lexical_diversity import lex_div as ld

# from app_lexical_diversity.helper_functions import lemmatize_list_of_words, get_subsamples_list, get_ordinal_ending
from lexdive_modules.my_request_module import RequestProcessor
from lexdive_modules.my_lemmatization_module import LemmatizationProcessor
from lexdive_modules.my_ld_module import MtldProcessor
from lexdive_modules.my_text_sampling_module import SplitTextSamplingProcessor, EqualTextSamplingProcessor, AuxiliarySamplingProcessor

from collections import Counter
import en_core_web_sm



@csrf_exempt
def count_mtld_whole_text(request):
    # request processing
    user_text_split = RequestProcessor().split_text(request)

    # lexical diversity processing
    mtld_processor = MtldProcessor()
    mtld_processor.calculate_lexical_diversity(user_text_split=user_text_split)
    
    data = {"mtld_value": round(float(mtld_processor.mtld_mean), 4),
            "number_of_tokens": mtld_processor.number_of_tokens,
            "factor_count_forward": round(float(mtld_processor.factor_count_with_remainder_forward), 4),
            "forward_mtld": round(float(mtld_processor.mtld_score_forward), 4),
            "factor_count_backward": round(float(mtld_processor.factor_count_with_remainder_backward), 4),
            "backward_mtld": round(float(mtld_processor.mtld_score_backward), 4)}
    return JsonResponse(data)


@csrf_exempt
def count_mtld_whole_text_lemmas(request):
    # request processing
    user_text_split = RequestProcessor().split_text(request)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_split)
    user_text_split_lemmas = lemmatization_processor.text_as_lemmas
    
    # lexical diversity processing
    mtld_processor = MtldProcessor()
    mtld_processor.calculate_lexical_diversity(user_text_split=user_text_split_lemmas)
    
    data = {"mtld_value": round(float(mtld_processor.mtld_mean), 4),
            "number_of_tokens": mtld_processor.number_of_tokens,
            "factor_count_forward": round(float(mtld_processor.factor_count_with_remainder_forward), 4),
            "forward_mtld": round(float(mtld_processor.mtld_score_forward), 4),
            "factor_count_backward": round(float(mtld_processor.factor_count_with_remainder_backward), 4),
            "backward_mtld": round(float(mtld_processor.mtld_score_backward), 4)}
    return JsonResponse(data)


@csrf_exempt
def count_hdd_whole_text(request):
    # request processing
    user_text_split = RequestProcessor().split_text(request)

    # lexical diversity processing
    lexical_diversity = ld.hdd(user_text_split)
    lexical_diversity = str(lexical_diversity)

    data = {"hdd_value": round(float(lexical_diversity), 4)}
    return JsonResponse(data)


@csrf_exempt
def count_ttr_whole_text(request):
    # request processing
    user_text_split = RequestProcessor().split_text(request)

    # lexical diversity processing
    number_of_tokens = len(user_text_split)
    user_text_split_types = set(user_text_split)
    number_of_types = len(user_text_split_types)
    lexical_diversity = number_of_types / number_of_tokens
    lexical_diversity = str(lexical_diversity)
    
    data = {"ttr_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_types": number_of_types}
    return JsonResponse(data)


@csrf_exempt
def count_ttr_whole_text_lemmas(request):
    # request processing
    user_text_split = RequestProcessor().split_text(request)

    # lemmatization  
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_split)
    user_text_split_lemmas = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    number_of_tokens = len(user_text_split)
    user_text_split_lemmas_set = set(user_text_split_lemmas)
    number_of_lemmas = len(user_text_split_lemmas_set)
    lexical_diversity = number_of_lemmas / number_of_tokens
    lexical_diversity = str(lexical_diversity)
    
    data = {"ltr_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_lemmas": number_of_lemmas}
    return JsonResponse(data)


# SPLIT TEXT PATTERN
@csrf_exempt
def count_ttr_split_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_split = request_processor.split_text(request)
    number_of_tokens = len(user_text_split)
    intended_text_length = request_processor.get_resource(request=request, resource_name='sample_length')
    intended_text_length = int(intended_text_length)
    size_of_subsamples = request_processor.get_resource(request=request, resource_name='size_of_subsamples')
    size_of_subsamples = int(size_of_subsamples)

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    intended_text = split_text_sampling_processor.sample_text(user_text_split=user_text_split)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=intended_text, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lexical diversity processing
    lexical_diversity = split_text_sampling_processor.number_of_types_in_intended_sample / split_text_sampling_processor.number_of_tokens_in_intended_sample
    lexical_diversity = str(lexical_diversity)

    

    data = {"ttr_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_types": split_text_sampling_processor.number_of_types_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)




@csrf_exempt
def count_ttr_split_text_lemmas(request): 
    # request processing
    request_processor = RequestProcessor()
    user_text_split = request_processor.split_text(request)
    number_of_tokens = len(user_text_split)
    intended_text_length = request_processor.get_resource(request=request, resource_name='sample_length')
    intended_text_length = int(intended_text_length)
    size_of_subsamples = request_processor.get_resource(request=request, resource_name='size_of_subsamples')
    size_of_subsamples = int(size_of_subsamples)

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    intended_text = split_text_sampling_processor.sample_text(user_text_split=user_text_split)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=intended_text, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)


    # lemmatization  
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(intended_text)
    user_text_split_lemmas = lemmatization_processor.text_as_lemmas
    number_of_lemmas_in_intended_sample = len(set(user_text_split_lemmas))

    # lexical diversity processing
    lexical_diversity = number_of_lemmas_in_intended_sample / split_text_sampling_processor.number_of_tokens_in_intended_sample
    lexical_diversity = str(lexical_diversity)

    data = {"ttr_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_lemmas": number_of_lemmas_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_ttr_equal_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_split = request_processor.split_text(request)
    equal_text_beginning = request_processor.get_resource(request=request, resource_name='sample_beginning')
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = request_processor.get_resource(request=request, resource_name='sample_length')
    equal_text_length = int(equal_text_length)

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    intended_text = equal_text_sampling_processor.sample_text(user_text_split=user_text_split)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lexical diversity processing
    lexical_diversity = equal_text_sampling_processor.number_of_types_in_intended_sample / equal_text_sampling_processor.number_of_tokens_in_intended_sample
    lexical_diversity = str(lexical_diversity)

    data = {"ttr_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": equal_text_sampling_processor.number_of_tokens_in_intended_sample,
            "number_of_types": equal_text_sampling_processor.number_of_types_in_intended_sample,
            "generated_sample": intended_text}
    return JsonResponse(data)


# HERE
@csrf_exempt
def count_ttr_equal_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_split = request_processor.split_text(request)
    equal_text_beginning = request_processor.get_resource(request=request, resource_name='sample_beginning')
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = request_processor.get_resource(request=request, resource_name='sample_length')
    equal_text_length = int(equal_text_length)

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    intended_text = equal_text_sampling_processor.sample_text(user_text_split=user_text_split)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lemmatization  
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(intended_text)
    user_text_split_lemmas = lemmatization_processor.text_as_lemmas
    number_of_lemmas_in_intended_sample = len(set(user_text_split_lemmas))

    # lexical diversity processing
    lexical_diversity = number_of_lemmas_in_intended_sample / equal_text_sampling_processor.number_of_tokens_in_intended_sample
    lexical_diversity = str(lexical_diversity)
    
    data = {"ttr_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": equal_text_sampling_processor.number_of_tokens_in_intended_sample,
            "number_of_lemmas": number_of_lemmas_in_intended_sample,
            "generated_sample": user_text_split_lemmas}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_whole_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    number_of_tokens = len(data)
    data = set(data)
    number_of_types = len(data)
    lexical_diversity = math.log10(number_of_types) / math.log10(number_of_tokens)
    lexical_diversity = str(lexical_diversity)
    
    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_types": number_of_types}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_whole_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()    
    sentence_as_lemmas = lemmatize_list_of_words(data)
    number_of_tokens = len(data)
    sentence_as_lemmas_set = set(sentence_as_lemmas)
    number_of_lemmas = len(sentence_as_lemmas_set)
    
    lexical_diversity = math.log10(number_of_lemmas) / math.log10(number_of_tokens)
    lexical_diversity = str(lexical_diversity)
    
    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_lemmas": number_of_lemmas}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_split_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    intended_text_length = return_value['sample_length']
    intended_text_length = int(intended_text_length)
    size_of_subsamples = return_value['size_of_subsamples']
    size_of_subsamples = int(size_of_subsamples)
    original_text_length = len(data)
    number_of_samples = intended_text_length / size_of_subsamples
    gap_size = (original_text_length - intended_text_length) / number_of_samples
    criteria = cycle(
        [True] * int(size_of_subsamples) + [False] * int(gap_size))
    intended_text = list(compress(data, criteria))
    intended_text = intended_text[:intended_text_length]

    number_of_tokens_in_intended_sample = len(intended_text)
    types_in_intended_sample = set(intended_text)
    number_of_types_in_intended_sample = len(types_in_intended_sample)
    lexical_diversity = math.log10(number_of_types_in_intended_sample) / math.log10(number_of_tokens_in_intended_sample)
    lexical_diversity = str(lexical_diversity)
    
    subsamples_list = get_subsamples_list(intended_text, size_of_subsamples, number_of_samples, number_of_tokens_in_intended_sample)

    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_types": number_of_types_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": number_of_samples,
            "size_of_gaps": int(gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_split_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    intended_text_length = return_value['sample_length']
    intended_text_length = int(intended_text_length)
    size_of_subsamples = return_value['size_of_subsamples']
    size_of_subsamples = int(size_of_subsamples)
    original_text_length = len(data)
    number_of_samples = intended_text_length / size_of_subsamples
    gap_size = (original_text_length - intended_text_length) / number_of_samples
    criteria = cycle(
        [True] * int(size_of_subsamples) + [False] * int(gap_size))
    intended_text = list(compress(data, criteria))
    intended_text = intended_text[:intended_text_length]

    number_of_tokens_in_intended_sample = len(intended_text)
    lemmas_in_intended_sample_list = lemmatize_list_of_words(intended_text)
    lemmas_in_intended_sample_set = set(lemmas_in_intended_sample_list)
    number_of_lemmas_in_intended_sample = len(lemmas_in_intended_sample_set)
    lexical_diversity = math.log10(number_of_lemmas_in_intended_sample) / math.log10(number_of_tokens_in_intended_sample)
    lexical_diversity = str(lexical_diversity)

    subsamples_list = get_subsamples_list(lemmas_in_intended_sample_list, size_of_subsamples, number_of_samples, number_of_tokens_in_intended_sample)
    print(number_of_lemmas_in_intended_sample)
    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_lemmas": number_of_lemmas_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": number_of_samples,
            "size_of_gaps": int(gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_equal_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    equal_text_beginning = return_value['sample_beginning']
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = return_value['sample_length']
    equal_text_length = int(equal_text_length)
    
    # whole_text_length = len(data)
    equal_text = data[equal_text_beginning-1:equal_text_length+(equal_text_beginning-1)]
    number_of_tokens_in_equal_text = len(equal_text)
    list_of_types_in_equal_text = set(equal_text)
    number_of_types_in_equal_text = len(list_of_types_in_equal_text)
    lexical_diversity = math.log10(number_of_types_in_equal_text) / math.log10(number_of_tokens_in_equal_text)
    lexical_diversity = str(lexical_diversity)
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = ""
    if equal_text_beginning_as_string[-1:] == "1":
        beginning_word_ordinal_ending = "st"
    elif equal_text_beginning_as_string[-1:] == "2":
        beginning_word_ordinal_ending = "nd"
    elif equal_text_beginning_as_string[-1:] == "3":
        beginning_word_ordinal_ending = "rd"
    else:
        beginning_word_ordinal_ending = "th"
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    data = {"herdans_c_value": round(float(lexical_diversity), 4),
        "sample_beginning_info": sample_beginning_info,
        "number_of_tokens": number_of_tokens_in_equal_text,
        "number_of_types": number_of_types_in_equal_text,
        "generated_sample": equal_text}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_equal_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    equal_text_beginning = return_value['sample_beginning']
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = return_value['sample_length']
    equal_text_length = int(equal_text_length)
    equal_text = data[equal_text_beginning-1:equal_text_length+(equal_text_beginning-1)]
    number_of_tokens_in_equal_text = len(equal_text)

    list_of_lemmas_in_equal_text = lemmatize_list_of_words(equal_text)
    number_of_lemmas_in_equal_text = len(set(list_of_lemmas_in_equal_text))

    lexical_diversity = math.log10(number_of_lemmas_in_equal_text) / math.log10(number_of_tokens_in_equal_text)
    lexical_diversity = str(lexical_diversity)
    
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": number_of_tokens_in_equal_text,
            "number_of_lemmas": number_of_lemmas_in_equal_text,
            "generated_sample": list_of_lemmas_in_equal_text}
    return JsonResponse(data)



@csrf_exempt
def count_guirauds_r_whole_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    number_of_tokens = len(data)
    data = set(data)
    number_of_types = len(data)
    lexical_diversity = number_of_types / math.sqrt(number_of_tokens)
    lexical_diversity = str(lexical_diversity)
    
    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_types": number_of_types}
    return JsonResponse(data)



@csrf_exempt
def count_guirauds_r_whole_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()    
    sentence_as_lemmas = lemmatize_list_of_words(data)
    number_of_tokens = len(data)
    sentence_as_lemmas_set = set(sentence_as_lemmas)
    number_of_lemmas = len(sentence_as_lemmas_set)
   
    lexical_diversity = number_of_lemmas / math.sqrt(number_of_tokens)
    lexical_diversity = str(lexical_diversity)
    
    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_lemmas": number_of_lemmas}
    return JsonResponse(data)



@csrf_exempt
def count_guirauds_r_split_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    intended_text_length = return_value['sample_length']
    intended_text_length = int(intended_text_length)
    size_of_subsamples = return_value['size_of_subsamples']
    size_of_subsamples = int(size_of_subsamples)
    original_text_length = len(data)
    number_of_samples = intended_text_length / size_of_subsamples
    gap_size = (original_text_length - intended_text_length) / number_of_samples
    criteria = cycle(
        [True] * int(size_of_subsamples) + [False] * int(gap_size))
    intended_text = list(compress(data, criteria))
    intended_text = intended_text[:intended_text_length]
    
    number_of_tokens_in_intended_sample = len(intended_text)
    types_in_intended_sample = set(intended_text)
    number_of_types_in_intended_sample = len(types_in_intended_sample)
    lexical_diversity = number_of_types_in_intended_sample / math.sqrt(number_of_tokens_in_intended_sample)
    lexical_diversity = str(lexical_diversity)

    subsamples_list = get_subsamples_list(intended_text, size_of_subsamples, number_of_samples, number_of_tokens_in_intended_sample)

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_types": number_of_types_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": number_of_samples,
            "size_of_gaps": int(gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)


@csrf_exempt
def count_guirauds_r_split_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    intended_text_length = return_value['sample_length']
    intended_text_length = int(intended_text_length)
    size_of_subsamples = return_value['size_of_subsamples']
    size_of_subsamples = int(size_of_subsamples)
    original_text_length = len(data)
    number_of_samples = intended_text_length / size_of_subsamples
    gap_size = (original_text_length - intended_text_length) / number_of_samples
    criteria = cycle(
        [True] * int(size_of_subsamples) + [False] * int(gap_size))
    intended_text = list(compress(data, criteria))
    intended_text = intended_text[:intended_text_length]

    number_of_tokens_in_intended_sample = len(intended_text)
    lemmas_in_intended_sample_list = lemmatize_list_of_words(intended_text)
    lemmas_in_intended_sample_set = set(lemmas_in_intended_sample_list)
    number_of_lemmas_in_intended_sample = len(lemmas_in_intended_sample_set)
    lexical_diversity = number_of_lemmas_in_intended_sample / math.sqrt(number_of_tokens_in_intended_sample)
    lexical_diversity = str(lexical_diversity)

    subsamples_list = get_subsamples_list(lemmas_in_intended_sample_list, size_of_subsamples, number_of_samples, number_of_tokens_in_intended_sample)

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_lemmas": number_of_lemmas_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": number_of_samples,
            "size_of_gaps": int(gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)


@csrf_exempt
def count_guirauds_r_equal_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    equal_text_beginning = return_value['sample_beginning']
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = return_value['sample_length']
    equal_text_length = int(equal_text_length)
    
    # whole_text_length = len(data)
    equal_text = data[equal_text_beginning-1:equal_text_length+(equal_text_beginning-1)]
    number_of_tokens_in_equal_text = len(equal_text)
    list_of_types_in_equal_text = set(equal_text)
    number_of_types_in_equal_text = len(list_of_types_in_equal_text)
    lexical_diversity = number_of_types_in_equal_text / math.sqrt(number_of_tokens_in_equal_text)
    lexical_diversity = str(lexical_diversity)
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = ""
    if equal_text_beginning_as_string[-1:] == "1":
        beginning_word_ordinal_ending = "st"
    elif equal_text_beginning_as_string[-1:] == "2":
        beginning_word_ordinal_ending = "nd"
    elif equal_text_beginning_as_string[-1:] == "3":
        beginning_word_ordinal_ending = "rd"
    else:
        beginning_word_ordinal_ending = "th"
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": number_of_tokens_in_equal_text,
            "number_of_types": number_of_types_in_equal_text,
            "generated_sample": equal_text}
    return JsonResponse(data)


@csrf_exempt
def count_guirauds_r_equal_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    equal_text_beginning = return_value['sample_beginning']
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = return_value['sample_length']
    equal_text_length = int(equal_text_length)
    equal_text = data[equal_text_beginning-1:equal_text_length+(equal_text_beginning-1)]
    number_of_tokens_in_equal_text = len(equal_text)

    list_of_lemmas_in_equal_text = lemmatize_list_of_words(equal_text)
    number_of_lemmas_in_equal_text = len(set(list_of_lemmas_in_equal_text))

    lexical_diversity = number_of_lemmas_in_equal_text / math.sqrt(number_of_tokens_in_equal_text)
    lexical_diversity = str(lexical_diversity)
    
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": number_of_tokens_in_equal_text,
            "number_of_lemmas": number_of_lemmas_in_equal_text,
            "generated_sample": list_of_lemmas_in_equal_text}
    return JsonResponse(data)



@csrf_exempt
def count_uber_u_whole_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    number_of_tokens = len(data)
    data = set(data)
    number_of_types = len(data)
    lexical_diversity = ((math.log10(number_of_tokens))**2) / (math.log10(number_of_tokens) - math.log10(number_of_types))
    lexical_diversity = str(lexical_diversity)
    
    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_types": number_of_types}
    return JsonResponse(data)


@csrf_exempt
def count_uber_u_whole_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()    
    sentence_as_lemmas = lemmatize_list_of_words(data)
    number_of_tokens = len(data)
    sentence_as_lemmas_set = set(sentence_as_lemmas)
    number_of_lemmas = len(sentence_as_lemmas_set)

    lexical_diversity = ((math.log10(number_of_tokens))**2) / (math.log10(number_of_tokens) - math.log10(number_of_lemmas))
    lexical_diversity = str(lexical_diversity)
    
    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "number_of_tokens": number_of_tokens,
            "number_of_lemmas": number_of_lemmas}
    return JsonResponse(data)




@csrf_exempt
def count_uber_u_split_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    intended_text_length = return_value['sample_length']
    intended_text_length = int(intended_text_length)
    size_of_subsamples = return_value['size_of_subsamples']
    size_of_subsamples = int(size_of_subsamples)
    original_text_length = len(data)
    number_of_samples = intended_text_length / size_of_subsamples
    gap_size = (original_text_length - intended_text_length) / number_of_samples
    criteria = cycle(
        [True] * int(size_of_subsamples) + [False] * int(gap_size))
    intended_text = list(compress(data, criteria))
    intended_text = intended_text[:intended_text_length]

    number_of_tokens_in_intended_sample = len(intended_text)
    types_in_intended_sample = set(intended_text)
    number_of_types_in_intended_sample = len(types_in_intended_sample)
    lexical_diversity = ((math.log10(number_of_tokens_in_intended_sample))**2) / (math.log10(number_of_tokens_in_intended_sample) - math.log10(number_of_types_in_intended_sample))
    lexical_diversity = str(lexical_diversity)
    
    subsamples_list = get_subsamples_list(intended_text, size_of_subsamples, number_of_samples, number_of_tokens_in_intended_sample)

    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_types": number_of_types_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": number_of_samples,
            "size_of_gaps": int(gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_uber_u_split_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    intended_text_length = return_value['sample_length']
    intended_text_length = int(intended_text_length)
    size_of_subsamples = return_value['size_of_subsamples']
    size_of_subsamples = int(size_of_subsamples)
    original_text_length = len(data)
    number_of_samples = intended_text_length / size_of_subsamples
    gap_size = (original_text_length - intended_text_length) / number_of_samples
    criteria = cycle(
        [True] * int(size_of_subsamples) + [False] * int(gap_size))
    intended_text = list(compress(data, criteria))
    intended_text = intended_text[:intended_text_length]

    number_of_tokens_in_intended_sample = len(intended_text)
    lemmas_in_intended_sample_list = lemmatize_list_of_words(intended_text)
    lemmas_in_intended_sample_set = set(lemmas_in_intended_sample_list)
    number_of_lemmas_in_intended_sample = len(lemmas_in_intended_sample_set)
    print(number_of_lemmas_in_intended_sample)
    lexical_diversity = ((math.log10(number_of_tokens_in_intended_sample))**2) / (math.log10(number_of_tokens_in_intended_sample) - math.log10(number_of_lemmas_in_intended_sample))
    lexical_diversity = str(lexical_diversity)

    subsamples_list = get_subsamples_list(lemmas_in_intended_sample_list, size_of_subsamples, number_of_samples, number_of_tokens_in_intended_sample)

    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "generated_sample_length": len(intended_text),
            "number_of_lemmas": number_of_lemmas_in_intended_sample,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": number_of_samples,
            "size_of_gaps": int(gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)
  
  
@csrf_exempt
def count_uber_u_equal_text(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    equal_text_beginning = return_value['sample_beginning']
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = return_value['sample_length']
    equal_text_length = int(equal_text_length)
    
    # whole_text_length = len(data)
    equal_text = data[equal_text_beginning-1:equal_text_length+(equal_text_beginning-1)]
    number_of_tokens_in_equal_text = len(equal_text)
    list_of_types_in_equal_text = set(equal_text)
    number_of_types_in_equal_text = len(list_of_types_in_equal_text)
    lexical_diversity = ((math.log10(number_of_tokens_in_equal_text))**2) / (math.log10(number_of_tokens_in_equal_text) - math.log10(number_of_types_in_equal_text))
    lexical_diversity = str(lexical_diversity)
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = ""
    if equal_text_beginning_as_string[-1:] == "1":
        beginning_word_ordinal_ending = "st"
    elif equal_text_beginning_as_string[-1:] == "2":
        beginning_word_ordinal_ending = "nd"
    elif equal_text_beginning_as_string[-1:] == "3":
        beginning_word_ordinal_ending = "rd"
    else:
        beginning_word_ordinal_ending = "th"
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    data = {"uber_u_value": round(float(lexical_diversity), 4),
        "sample_beginning_info": sample_beginning_info,
        "number_of_tokens": number_of_tokens_in_equal_text,
        "number_of_types": number_of_types_in_equal_text,
        "generated_sample": equal_text}
    return JsonResponse(data)



@csrf_exempt
def count_uber_u_equal_text_lemmas(request):
    return_value = request.POST.dict()
    user_text = return_value['user_text']
    data = user_text.split()
    equal_text_beginning = return_value['sample_beginning']
    equal_text_beginning = int(equal_text_beginning)
    equal_text_length = return_value['sample_length']
    equal_text_length = int(equal_text_length)
    equal_text = data[equal_text_beginning-1:equal_text_length+(equal_text_beginning-1)]
    number_of_tokens_in_equal_text = len(equal_text)

    list_of_lemmas_in_equal_text = lemmatize_list_of_words(equal_text)
    number_of_lemmas_in_equal_text = len(set(list_of_lemmas_in_equal_text))

    lexical_diversity = ((math.log10(number_of_tokens_in_equal_text))**2) / (math.log10(number_of_tokens_in_equal_text) - math.log10(number_of_lemmas_in_equal_text))
    lexical_diversity = str(lexical_diversity)
    
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": number_of_tokens_in_equal_text,
            "number_of_lemmas": number_of_lemmas_in_equal_text,
            "generated_sample": list_of_lemmas_in_equal_text}
    return JsonResponse(data)
