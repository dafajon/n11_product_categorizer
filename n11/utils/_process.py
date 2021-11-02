import re

def process_st_input(user_input: str):
    user_input = re.sub("\n+", "\n", user_input)
    texts = [text for text in user_input.split("\n") if text.strip()]

    request_body = [{"texts": texts}]

    return request_body
