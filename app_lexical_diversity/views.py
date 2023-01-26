from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from lexdive_modules.my_request_module import RequestProcessor
from lexdive_modules.my_text_sampling_module import SplitTextSamplingProcessor, EqualTextSamplingProcessor, AuxiliarySamplingProcessor
from lexdive_modules.my_lemmatization_module import LemmatizationProcessor
from lexdive_modules.my_ld_module import MtldProcessor, TtrProcessor, HerdansCProcessor, GuiraudsRProcessor, UberUProcessor
from lexical_diversity import lex_div as ld



@csrf_exempt
def count_mtld_whole_text(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lexical diversity processing
    mtld_processor = MtldProcessor()
    mtld_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
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
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas
    
    # lexical diversity processing
    mtld_processor = MtldProcessor()
    mtld_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
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
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lexical diversity processing
    lexical_diversity = ld.hdd(user_text_list)
    lexical_diversity = str(lexical_diversity)

    data = {"hdd_value": round(float(lexical_diversity), 4)}
    return JsonResponse(data)


@csrf_exempt
def count_ttr_whole_text(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lexical diversity processing
    ttr_processor = TtrProcessor()
    lexical_diversity = ttr_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    # data PATTERN for ttr
    data = {"ttr_value": round(float(lexical_diversity), 4),
            "number_of_tokens": ttr_processor.number_of_tokens,
            "number_of_types": ttr_processor.number_of_typesorlemmas}
    return JsonResponse(data)


@csrf_exempt
def count_ttr_whole_text_lemmas(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lemmatization  
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    ttr_processor = TtrProcessor()
    lexical_diversity = ttr_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"ltr_value": round(float(lexical_diversity), 4),
            "number_of_tokens": ttr_processor.number_of_tokens,
            "number_of_lemmas": ttr_processor.number_of_typesorlemmas}
    return JsonResponse(data)



@csrf_exempt
def count_ttr_split_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lexical diversity processing
    ttr_processor = TtrProcessor()
    lexical_diversity = ttr_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    # data PATTERN for split text sampling
    data = {"ttr_value": round(float(lexical_diversity), 4),
            "generated_sample_length": ttr_processor.number_of_tokens,
            "number_of_types": ttr_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)




@csrf_exempt
def count_ttr_split_text_lemmas(request): 
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lemmatization  
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    ttr_processor = TtrProcessor()
    lexical_diversity = ttr_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"ttr_value": round(float(lexical_diversity), 4),
            "generated_sample_length": ttr_processor.number_of_tokens,
            "number_of_lemmas": ttr_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_ttr_equal_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lexical diversity processing
    ttr_processor = TtrProcessor()
    lexical_diversity = ttr_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"ttr_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": ttr_processor.number_of_tokens,
            "number_of_types": ttr_processor.number_of_typesorlemmas,
            "generated_sample": user_text_list}
    return JsonResponse(data)



@csrf_exempt
def count_ttr_equal_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lemmatization  
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    ttr_processor = TtrProcessor()
    lexical_diversity = ttr_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"ttr_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": ttr_processor.number_of_tokens,
            "number_of_lemmas": ttr_processor.number_of_typesorlemmas,
            "generated_sample": user_text_list}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_whole_text(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lexical diversity processing
    herdans_c_processor = HerdansCProcessor()
    lexical_diversity = herdans_c_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "number_of_tokens": herdans_c_processor.number_of_tokens,
            "number_of_types": herdans_c_processor.number_of_typesorlemmas}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_whole_text_lemmas(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    herdans_c_processor = HerdansCProcessor()
    lexical_diversity = herdans_c_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "number_of_tokens": herdans_c_processor.number_of_tokens,
            "number_of_lemmas": herdans_c_processor.number_of_typesorlemmas}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_split_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lexical diversity processing
    herdans_c_processor = HerdansCProcessor()
    lexical_diversity = herdans_c_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "generated_sample_length": herdans_c_processor.number_of_tokens,
            "number_of_types": herdans_c_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_split_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    herdans_c_processor = HerdansCProcessor()
    lexical_diversity = herdans_c_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "generated_sample_length": herdans_c_processor.number_of_tokens,
            "number_of_lemmas": herdans_c_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_equal_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lexical diversity processing
    herdans_c_processor = HerdansCProcessor()
    lexical_diversity = herdans_c_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"herdans_c_value": round(float(lexical_diversity), 4),
        "sample_beginning_info": sample_beginning_info,
        "number_of_tokens": herdans_c_processor.number_of_tokens,
        "number_of_types": herdans_c_processor.number_of_typesorlemmas,
        "generated_sample": user_text_list}
    return JsonResponse(data)



@csrf_exempt
def count_herdans_c_equal_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    herdans_c_processor = HerdansCProcessor()
    lexical_diversity = herdans_c_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"herdans_c_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": herdans_c_processor.number_of_tokens,
            "number_of_lemmas": herdans_c_processor.number_of_typesorlemmas,
            "generated_sample": user_text_list}
    return JsonResponse(data)



@csrf_exempt
def count_guirauds_r_whole_text(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lexical diversity processing
    guirauds_r_processor = GuiraudsRProcessor()
    lexical_diversity = guirauds_r_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "number_of_tokens": guirauds_r_processor.number_of_tokens,
            "number_of_types": guirauds_r_processor.number_of_typesorlemmas}
    return JsonResponse(data)



@csrf_exempt
def count_guirauds_r_whole_text_lemmas(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    guirauds_r_processor = GuiraudsRProcessor()
    lexical_diversity = guirauds_r_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "number_of_tokens": guirauds_r_processor.number_of_tokens,
            "number_of_lemmas": guirauds_r_processor.number_of_typesorlemmas}
    return JsonResponse(data)



@csrf_exempt
def count_guirauds_r_split_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lexical diversity processing
    guirauds_r_processor = GuiraudsRProcessor()
    lexical_diversity = guirauds_r_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "generated_sample_length": guirauds_r_processor.number_of_tokens,
            "number_of_types": guirauds_r_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)


@csrf_exempt
def count_guirauds_r_split_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    guirauds_r_processor = GuiraudsRProcessor()
    lexical_diversity = guirauds_r_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "generated_sample_length": guirauds_r_processor.number_of_tokens,
            "number_of_lemmas": guirauds_r_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)


@csrf_exempt
def count_guirauds_r_equal_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lexical diversity processing
    guirauds_r_processor = GuiraudsRProcessor()
    lexical_diversity = guirauds_r_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": guirauds_r_processor.number_of_tokens,
            "number_of_types": guirauds_r_processor.number_of_typesorlemmas,
            "generated_sample": user_text_list}
    return JsonResponse(data)


@csrf_exempt
def count_guirauds_r_equal_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    guirauds_r_processor = GuiraudsRProcessor()
    lexical_diversity = guirauds_r_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"guirauds_r_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": guirauds_r_processor.number_of_tokens,
            "number_of_lemmas": guirauds_r_processor.number_of_typesorlemmas,
            "generated_sample": user_text_list}
    return JsonResponse(data)



@csrf_exempt
def count_uber_u_whole_text(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lexical diversity processing
    uber_u_processor = UberUProcessor()
    lexical_diversity = uber_u_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "number_of_tokens": uber_u_processor.number_of_tokens,
            "number_of_types": uber_u_processor.number_of_typesorlemmas}
    return JsonResponse(data)



@csrf_exempt
def count_uber_u_whole_text_lemmas(request):
    # request processing
    user_text_list = RequestProcessor().user_text_to_list(request)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    uber_u_processor = UberUProcessor()
    lexical_diversity = uber_u_processor.calculate_lexical_diversity(user_text_list=user_text_list)
    
    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "number_of_tokens": uber_u_processor.number_of_tokens,
            "number_of_lemmas": uber_u_processor.number_of_typesorlemmas}
    return JsonResponse(data)




@csrf_exempt
def count_uber_u_split_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lexical diversity processing
    uber_u_processor = UberUProcessor()
    lexical_diversity = uber_u_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "generated_sample_length": uber_u_processor.number_of_tokens,
            "number_of_types": uber_u_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)



@csrf_exempt
def count_uber_u_split_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    number_of_tokens = len(user_text_list)
    intended_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))
    size_of_subsamples = int(request_processor.get_resource(request=request, resource_name='size_of_subsamples'))

    # sampling
    split_text_sampling_processor = SplitTextSamplingProcessor(intended_text_length=intended_text_length,
                                                                size_of_subsamples=size_of_subsamples,
                                                                number_of_tokens=number_of_tokens)
    user_text_list = split_text_sampling_processor.sample_text(user_text_list=user_text_list)
    auxilairy_sampling_processor = AuxiliarySamplingProcessor()
    subsamples_list = auxilairy_sampling_processor.get_subsamples_list(intended_text=user_text_list, 
                                                                size_of_subsamples=size_of_subsamples, 
                                                                number_of_samples=split_text_sampling_processor.number_of_samples)

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    uber_u_processor = UberUProcessor()
    lexical_diversity = uber_u_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "generated_sample_length": uber_u_processor.number_of_tokens,
            "number_of_lemmas": uber_u_processor.number_of_typesorlemmas,
            "size_of_subsamples_used": size_of_subsamples,
            "number_of_subsamples": split_text_sampling_processor.number_of_samples,
            "size_of_gaps": int(split_text_sampling_processor.gap_size),
            "subsamples_list": subsamples_list}
    return JsonResponse(data)
  
  
@csrf_exempt
def count_uber_u_equal_text(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lexical diversity processing
    uber_u_processor = UberUProcessor()
    lexical_diversity = uber_u_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"uber_u_value": round(float(lexical_diversity), 4),
        "sample_beginning_info": sample_beginning_info,
        "number_of_tokens": uber_u_processor.number_of_tokens,
        "number_of_types": uber_u_processor.number_of_typesorlemmas,
        "generated_sample": user_text_list}
    return JsonResponse(data)



@csrf_exempt
def count_uber_u_equal_text_lemmas(request):
    # request processing
    request_processor = RequestProcessor()
    user_text_list = request_processor.user_text_to_list(request)
    equal_text_beginning = int(request_processor.get_resource(request=request, resource_name='sample_beginning'))
    equal_text_length = int(request_processor.get_resource(request=request, resource_name='sample_length'))

    # sampling
    equal_text_sampling_processor = EqualTextSamplingProcessor(equal_text_beginning=equal_text_beginning, equal_text_length=equal_text_length)
    user_text_list = equal_text_sampling_processor.sample_text(user_text_list=user_text_list)

    # info text generation
    equal_text_beginning_as_string = str(equal_text_beginning)
    beginning_word_ordinal_ending = AuxiliarySamplingProcessor().get_ordinal_ending(equal_text_beginning_as_string)
    sample_beginning_info = "The generated sample starts with the " + str(equal_text_beginning) + beginning_word_ordinal_ending + " word of the entire text."

    # lemmatization
    lemmatization_processor = LemmatizationProcessor()
    lemmatization_processor.lemmatize_text(user_text_list=user_text_list)
    user_text_list = lemmatization_processor.text_as_lemmas

    # lexical diversity processing
    uber_u_processor = UberUProcessor()
    lexical_diversity = uber_u_processor.calculate_lexical_diversity(user_text_list=user_text_list)

    data = {"uber_u_value": round(float(lexical_diversity), 4),
            "sample_beginning_info": sample_beginning_info,
            "number_of_tokens": uber_u_processor.number_of_tokens,
            "number_of_lemmas": uber_u_processor.number_of_typesorlemmas,
            "generated_sample": user_text_list}
    return JsonResponse(data)
