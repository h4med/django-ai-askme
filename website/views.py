from django.shortcuts import render
from django.contrib import messages
from decouple import config
import openai



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