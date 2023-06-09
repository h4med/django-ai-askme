import openai

def get_completion_and_token_count(messages, 
                                   model="gpt-3.5-turbo", 
                                   temperature=0, 
                                   max_tokens=500):
    
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, 
        max_tokens=max_tokens,
    )
    
    content = response.choices[0].message["content"]
    
    token_dict = {
    'prompt_tokens':response['usage']['prompt_tokens'],
    'completion_tokens':response['usage']['completion_tokens'],
    'total_tokens':response['usage']['total_tokens'],
    }
    id = response["id"]
    return content, token_dict, id