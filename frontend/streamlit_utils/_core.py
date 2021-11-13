import html as ihtml
import re
import warnings
from functools import partial

import pandas as pd
from bs4 import BeautifulSoup
from sadedegel.bblock.word_tokenizer import ICUTokenizer

warnings.filterwarnings("ignore")

from sklearn.base import TransformerMixin

class TextCleaner(TransformerMixin):
    def __init__(self, to_clean: list):
        self.to_clean = to_clean

    def clean_text(self, text):
        text = BeautifulSoup(ihtml.unescape(text)).text
        text = re.sub(r"http[s]?://\S+", "", text)
        text = re.sub(r"\s+", " ", text)
        return text

    def fit(self, X, y=None):
        return self

    def transform(self, X, y=None):
        X = pd.DataFrame(X).copy()
        X['all_text'] = ''
        for col in self.to_clean:
            X['all_text'] = X['all_text'] + ' ' + X[col]
        X['all_text'] = X['all_text'].apply(self.clean_text)
        return X.all_text

# setting custom tokenizer for sklearn tf-idf

tokenizer = ICUTokenizer()

def custom_tokenizer(doc: str, prefix_len: int = 5, tokenizer=tokenizer):
    tokens = [t.lower_[:prefix_len] for t in tokenizer(doc)]
    return tokens

def make_tokenizer(prefix_len):
    ct = partial(custom_tokenizer, prefix_len=prefix_len)
    return ct
