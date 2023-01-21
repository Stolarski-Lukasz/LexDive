import operator


class TextStatisticsProcessor:

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




    

    

