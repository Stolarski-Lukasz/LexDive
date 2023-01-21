from abc import ABC, abstractclassmethod

class RequestProcessor(ABC):

    @abstractclassmethod
    def split_text(self, request):
        pass

class RequestTextProcessor(RequestProcessor):

    def split_text(self, request):
        user_text = request.POST.dict()
        user_text = user_text['user_text']
        return user_text.split()