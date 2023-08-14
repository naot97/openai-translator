import openai
from typing import Dict
import tiktoken
import os
import time
from config import common as config

openai.api_key = os.environ.get("OPENAI_KEY","")
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
def _get_chat_completion(message, model="gpt-3.5-turbo", n=1, stop=None, temperature=1):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[message],
        n=n,
        stop=stop,
        temperature=temperature,
    )

    return response.choices[0].message.content

def chat(messages: str) -> str:
    assistant_response = _get_chat_completion(messages)
    return assistant_response

def create_message(dest: str, chunk: str) -> Dict[str, str]:
    return {
        "role": "user",
        "content": f'{config.prompt.format(dest, chunk)}',
    }

def count_message_tokens(message, model='gpt-3.5-turbo'):
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print('Warning: model not found. Using cl100k_base encoding.')
        encoding = tiktoken.get_encoding('cl100k_base')
    if model == 'gpt-3.5-turbo':
        token_per_message = (
            4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        )

    num_tokens = len(encoding.encode(message)) + token_per_message
    num_tokens += 3 # for { }
    return num_tokens

def count_string_tokens(string: str, model: str = 'gpt-3.5-turbo') -> int:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(string))

def get_translation_from_list(dest: str, text_lst: [str], cost: float = 0) -> str:
    text_lst = [text.replace('\n','') for text in text_lst]
    text_lst = [text.replace('|','') for text in text_lst]
    merge_text = ''
    answers = []
    total_cost = 0
    for i, text in enumerate(text_lst):
        print(text)
        if  count_message_tokens(f'{merge_text}||{text}') < config.LIMIT_TOKEN_NUMBER :
            merge_text = f'{merge_text}||{text}' if len(merge_text) > 0 else text
            hit_limit = False
        else:
            hit_limit = True

        if  i == len(text_lst) - 1 or hit_limit:
            answer, cost = get_translation_from_text(dest, merge_text)
            answers = answers + map(lambda x: x.strip(), answer.split('||')) 
            total_cost += cost
            merge_text = text

    
    return answers, total_cost

def get_translation_from_text(dest: str, text: str, cost: float = 0) -> str:
    answer = ''
    cost = 0
    sum_tokens = 0
    if count_message_tokens(text) < config.LIMIT_TOKEN_NUMBER:
        message = create_message(dest, text)
        tokens_for_chunk = count_message_tokens(message['content'])
        cost += config.GPT35_INPUT_PRICING * tokens_for_chunk / 1000
        sum_tokens += tokens_for_chunk
        attempt = 0
        while attempt < config.max_attemp:
            try:
                answer = chat(message)
                break
            except Exception as e:
                print(e)
                time.sleep(20)
                attempt += 1
                if attempt >= config.max_attemp:
                    raise Exception(f"Can not send request to OpenAI")
                
                continue
        answer_tokens = count_string_tokens(answer)
        sum_tokens += answer_tokens
        cost += answer_tokens * config.GPT35_OUTPUT_PRICING / 1000
    else:
        raise Exception(f"Sentence is too long, please input not greater than {config.LIMIT_TOKEN_NUMBER} tokens.")

    return answer, cost


