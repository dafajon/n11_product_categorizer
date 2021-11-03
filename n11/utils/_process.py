import re
from sadedegel.bblock.word_tokenizer import ICUTokenizer
from functools import partial

tokenizer = ICUTokenizer()

def custom_tokenizer(doc: str, prefix_len: int, tokenizer=tokenizer):
        #tokens = [t.lower_ for t in tokenizer(doc)]
        tokens = [t.lower_[:prefix_len] for t in tokenizer(doc)]
        return tokens

def make_tokenizer(prefix_len):
    ct = partial(custom_tokenizer, prefix_len=prefix_len)
    return ct
