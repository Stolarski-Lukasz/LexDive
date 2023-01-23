# from abc import ABC, abstractclassmethod

# class RequestProcessor(ABC):

#     @abstractclassmethod
#     def get_resource(self, request, name):
#         pass

#     @abstractclassmethod
#     def split_text(self, request, name):
#         pass

class RequestProcessor():

    def get_resource(self, request, resource_name):
        request_dict = request.POST.dict()
        return request_dict[resource_name]

    def split_text(self, request, resource_name="user_text"):
        request_dict = request.POST.dict()
        user_text = request_dict[resource_name]
        return user_text.split()