# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.views import generic
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from ..utils.decorators import ajax_required
from ..utils.mixins import FormErrors
from ..forms import InputForm
from ..utils.openai_utils import get_completion_and_token_count
from ..models import Dialogue

# --------------------------------------------------------------
# 3rd Party imports
# --------------------------------------------------------------
import openai
from decouple import config

openai.api_key = config('OPENAI_API_KEY')

@method_decorator(login_required, name='dispatch')
class AskMeView(generic.FormView):
    template_name = "ask_me_fa.html"
    form_class = InputForm

    
    @method_decorator(ajax_required)
    def post(self, request,*args, **kwargs):
        data = {'result': 'Error', 'message': "Something went wrong, please try again", "redirect": False, "data":None}
        form = InputForm(request.POST)
        if form.is_valid():
            input = form.cleaned_data.get("input")
            openai.api_key = config('OPENAI_API_KEY')
            openai_message = [
                {
                    'role':'system', 
                    'content':"""You are a knowledgeable and honest assistant and you only answer the questions that are asked in Farsi/Persian and you only answer in Farsi. Question is delimited by triple backticks."""
                    },    
                {
                    'role':'user',
                    'content':f"question: ```{input}```"
                    },  
                ] 
            # openai_message = [
            #     {
            #         'role':'user', 
            #         'content':f"""You are a knowledgeable and honest assistant, answer the question, it is delimited by triple backticks, it is in Persian and you only answer in persian. question: ```{input}```"""
            #         }
            #     ]             
            response, token_dict, id = get_completion_and_token_count(openai_message,max_tokens=2500)
            ans = response.strip()
            tokens = int(token_dict["total_tokens"])
            print(f"in try, tokens: {tokens}, id: {id}")
            record = Dialogue(question=input, answer=ans, user=request.user, total_tokens=tokens, openai_id=id)
            record.save()
            data.update({
                'result': "Success",
                'message': "ChatGPT has suggested some names",
                'data': ans
            })
            return JsonResponse(data)
        
        else:
            data["message"] = FormErrors(form)
            return JsonResponse(data, status=400)        
    

    # def get(self, request):
    # # handle the get request
    #     return render(request, 'ask_me_fa.html')