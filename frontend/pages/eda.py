import os
import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import wordcloud as wc
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import chi2
from sklearn.metrics import classification_report


@st.cache
def data():
    data = pd.read_csv('data/train_n11.csv')
    data = data[~data.CATEGORY_ID.isna()]
    data.CATEGORY_ID = data.CATEGORY_ID.astype(int)
    return data, data['CATEGORY_ID'].value_counts()

def app():
    st.title("Exploratory Data Analysis on the Training Data")
    train_data, _temp= data()
    st.dataframe(train_data.head())
    palet = ['#FF0000',
    '#FD482A',
    '#F96849',
    '#F28368',
    '#E89B87',
    '#DAB1A6',
    '#7F7F7F',
    '#5E5E5E',
    '#3F3F3F',
    '#222222',
    '#000000']

    plt.style.use('ggplot')

    st.header("Category Product Distribution")

    requested = st.selectbox('Popularity Lists', ['Top 10', 'Bottom 10', 'All'])
    if requested == 'Top 10':
        _temp = _temp.iloc[:10]
    elif requested == 'Bottom 10':
        _temp = _temp.iloc[-10:]
    elif requested == 'All':
        _temp = _temp.sort_values()

    fig, ax = plt.subplots(1, 2)
    fig.autofmt_xdate(rotation=30)
    sns.barplot(y=_temp.values, x=_temp.index, ax=ax[0], palette = palet)
    ax[0].tick_params(axis='x', which='major', labelsize=5)
    ax[0].tick_params(axis='y', which='major', labelsize=5)

    ax[1].pie(_temp, labels=_temp.index, colors = palet, textprops={'fontsize': 5}, autopct='%1.1f%%')
    st.pyplot(fig)

    @st.cache
    def create_wc(cat):
        split_title = train_data[train_data.CATEGORY_ID == cat].TITLE.str.split().values.tolist()
        corpus = ' '.join([t.lower() for x in split_title for t in x])
        wordcloud = wc.WordCloud(width=2000, height=1000, max_words=200, colormap='gist_stern', random_state=42).generate(
            corpus)
        return wordcloud

    def correlations(cat):
        vec = TfidfVectorizer(strip_accents='unicode', ngram_range=(1, 2), sublinear_tf=True, smooth_idf=False, max_df=0.85,
                            min_df=200)
        f = train_data.copy()
        features = vec.fit_transform(f.TITLE).toarray()

        labels = f.CATEGORY_ID

        N = 3

        features_chi2 = chi2(features, labels == cat)
        indices = np.argsort(features_chi2[0])
        feature_names = np.array(vec.get_feature_names())[indices]
        unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
        bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
        
        return ', '.join(unigrams[-N:]), ', '.join(bigrams[-N:])

    cat = st.selectbox('Category ID', train_data.CATEGORY_ID.unique().tolist())
    wordcloud = create_wc(cat)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig)
    unigrams, bigrams = correlations(cat)
    st.markdown("  * Most Correlated Unigrams are: %s" % (unigrams))
    st.markdown("  * Most Correlated Bigrams are: %s" % (bigrams))


if __name__ == '__main__':
    app()
