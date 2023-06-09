# --------------------------------------------------------------
# Django imports
# --------------------------------------------------------------
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import UserCreationForm
from django.utils.decorators import method_decorator
from django.http import JsonResponse
# --------------------------------------------------------------
# Project imports
# --------------------------------------------------------------
from .forms import SignUpForm
from .models import Dialogue
from .utils.openai_utils import get_completion_and_token_count
from .utils.decorators import ajax_required

# --------------------------------------------------------------
# 3rd Party imports
# --------------------------------------------------------------
import openai
from decouple import config


@login_required
def home(request):
    lang_list = ['c', 'clike', 'cpp', 'css', 'html', 'java', 'javascript', 'markup', 'php', 'python', 'rust', 'sql']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        # Check to make sure the lang is selected
        if lang == "Select Programming Language":
            messages.success(request, "Hey, You forgot to select the programming language!")
            return render(request, 'home.html', {'lang_list': lang_list, 'code':code, 'lang':lang})
        else:

            # OpenAI
            openai.api_key = config('OPENAI_API_KEY')
            openai.Model.list()
            try:
                response = openai.Completion.create(
                    model = 'text-davinci-003',
                    prompt = f"Respond only with code. Fix this {lang} code: {code}",
                    temperature = 0,
                    max_tokens = 1500,
                    top_p = 1.0,
                    )
                print("in try", "lang:", lang, response)
                response = (response["choices"][0]["text"]).strip()
                return render(request, 'home.html', {'lang_list': lang_list, 'code':code, 'response':response, 'lang':lang})
            except Exception as e:
                print("in Exception", e)
                return render(request, 'home.html', {'lang_list': lang_list, 'code':code, 'response':e, 'lang':lang})

    return render(request, 'home.html', {'lang_list': lang_list})

@login_required
def write_code(request):
    lang_list = ['c', 'clike', 'cpp', 'css', 'html', 'java', 'javascript', 'markup', 'php', 'python', 'rust', 'sql']

    if request.method == "POST":
        code = request.POST['code']
        lang = request.POST['lang']
        # Check to make sure the lang is selected
        if lang == "Select Programming Language":
            messages.success(request, "Hey, You forgot to select the programming language!")
            return render(request, 'write_code.html', {'lang_list': lang_list, 'code':code, 'lang':lang})
        else:

            # OpenAI
            openai.api_key = config('OPENAI_API_KEY')
            openai.Model.list()
            try:
                response = openai.Completion.create(
                    model = 'text-davinci-003',
                    prompt = f"Respond only with code in {lang} programming language. {code}",
                    temperature = 0,
                    max_tokens = 1500,
                    top_p = 1.0,
                    )
                print("in try", "lang:", lang, response)
                response = (response["choices"][0]["text"]).strip()
                return render(request, 'write_code.html', {'lang_list': lang_list, 'code':code, 'response':response, 'lang':lang})
            except Exception as e:
                print("in Exception", e)
                return render(request, 'write_code.html', {'lang_list': lang_list, 'code':code, 'response':e, 'lang':lang})

    return render(request, 'write_code.html', {'lang_list': lang_list})

@login_required
def ask_me(request):

    if request.method == "POST":
        question = request.POST['question']
        question_utf = question.encode()
        # Check to make sure the question is provided
        if question == "":
            messages.success(request, "بخش سوال خالی است!")
            return render(request, 'ask_me.html', {})
        else:
            # OpenAI
            openai.api_key = config('OPENAI_API_KEY')
            openai_message = [
                {
                    'role':'system', 
                    'content':"""You are an omniscient, the user will ask you a question in Farsi (Persian), answer the question in Persian and as thorough and simple as possible"""
                    },    
                {
                    'role':'user',
                    'content':f"{question_utf}"
                    },  
                ] 
            try:
                response, token_dict, id = get_completion_and_token_count(openai_message,max_tokens=2500)
                ans = response.strip()
                tokens = int(token_dict["total_tokens"])
                print(f"in try, tokens: {tokens}, id: {id}")
                record = Dialogue(question=question, answer=ans, user=request.user, total_tokens=tokens, openai_id=id)
                record.save()
                return render(request, 'ask_me.html', {'response':ans, 'question':question})
            except Exception as e:
                print("in Exception", e)
                return render(request, 'ask_me.html', {'question':question, 'response':e})

    return render(request, 'ask_me.html', {})


# @login_required
# @method_decorator(ajax_required)
# def ask_me(request):

#     if request.method == "POST":
#         question = request.POST['question']
#         question_utf = question.encode()
#         data = {'result': 'Error', 'message': "Something went wrong, please try again", "redirect": False, "data":None}
#         # Check to make sure the question is provided
#         if question == "":
#             messages.success(request, "بخش سوال خالی است!")
#             return render(request, 'ask_me.html', {})
#         else:
#             # OpenAI
#             openai.api_key = config('OPENAI_API_KEY')
#             openai_message = [
#                 {
#                     'role':'system', 
#                     'content':"""You are an omniscient, the user will ask you a question in Farsi (Persian), answer the question in Persian and as thorough and simple as possible"""
#                     },    
#                 {
#                     'role':'user',
#                     'content':f"{question_utf}"
#                     },  
#                 ] 
#             try:
#                 response, token_dict, id = get_completion_and_token_count(openai_message,max_tokens=2500)
#                 ans = response.strip()
#                 data.update({
#                     'result': "Success",
#                     'message': "ChatGPT has suggested some names",
#                     'data': ans
#                 })
#                 # response = (response["choices"][0]["text"]).strip()
#                 tokens = int(token_dict["total_tokens"])
#                 print(f"in try, tokens: {tokens}, id: {id}")
#                 record = Dialogue(question=question, answer=ans, user=request.user, total_tokens=tokens, openai_id=id)
#                 record.save()
#                 # return render(request, 'ask_me.html', {'response':ans, 'question':question})
#                 return JsonResponse(data)
#             except Exception as e:
#                 print("in Exception", e)
#                 data["message"] = e
#                 return JsonResponse(data, status=400)
#                 # return render(request, 'ask_me.html', {'question':question, 'response':e})

#     return render(request, 'ask_me.html', {})


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username ,password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have logged in!")
            return redirect('home')
        else:
            messages.success(request, "Error logging in!")
            return redirect('home')        
        
    return render(request, 'home.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, "logged out!")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username ,password=password)
            login(request, user)
            messages.success(request, "Registered OK, login...")
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {"form":form})

@login_required
def ask_me_arch(request):
    dialogues = Dialogue.objects.filter(user_id=request.user.id).order_by('-created_at')
    return render(request, 'ask_me_arch.html', {"dialogues":dialogues})


@login_required
def edit_me(request):
    return render(request, 'edit_me.html', {})
    if request.method == "POST":
        question = request.POST['question']

        # Check to make sure the question is provided
        if question == "":
            messages.success(request, "Hey, You forgot to ask!")
            return render(request, 'ask_me.html', {})
        else:

            # OpenAI
            openai.api_key = config('OPENAI_API_KEY')
            openai.Model.list()
            try:
                # response = openai.Completion.create(
                #     model = 'text-davinci-003',
                #     prompt = f"Respond the following statement or question in English: {question}",
                #     temperature = 0,
                #     max_tokens = 1500,
                #     top_p = 1.0,
                #     )
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo-0301",
                    messages=[
                        {
                            "role": "user", 
                            "content": f"Respond the following statement or question in English: {question}!"
                        }
                    ]
                    
                    )
                print("in try", response)
                # response = (response["choices"][0]["text"]).strip()
                ans = (response["choices"][0]["message"]["content"]).strip()
                tokens = int(response["usage"]["total_tokens"])
                id = response["id"]
                record = Dialogue(question=question, answer=ans, user=request.user, total_tokens=tokens, openai_id=id)
                record.save()
                return render(request, 'ask_me.html', {'response':ans, 'question':question})
            except Exception as e:
                print("in Exception", e)
                return render(request, 'ask_me.html', {'question':question, 'response':e})

    return render(request, 'ask_me.html', {})