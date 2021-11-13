import streamlit as st
import pandas as pd
import eli5
import joblib
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import matplotlib.pyplot as plt

from IPython.display import HTML
from streamlit.components.v1 import html as sthtml
from streamlit import components

from sklearn.metrics import classification_report



@st.cache
def data():
    data = pd.read_csv('data/valid_n11.csv')
    data = data[~data.CATEGORY_ID.isna()]
    data.CATEGORY_ID = data.CATEGORY_ID.astype(int)
    return data, data['CATEGORY_ID'].value_counts()

@st.cache
def worst_wc(inp_df, pipe):
    preds = pipe.predict(inp_df)
    y_val = inp_df['CATEGORY_ID']
    report_= classification_report(y_val, preds, output_dict=True)
    report=pd.DataFrame.from_dict(report_).T[:-3].reset_index().rename(columns={'index': 'CATEGORY_ID'})
    report['CATEGORY_ID'] = report['CATEGORY_ID'].astype('int')
    z=report.sort_values(by='f1-score', ascending=False)[-10:]['CATEGORY_ID'].tolist()
    texts = " ".join(review for review in inp_df[inp_df['CATEGORY_ID'].isin(z)]['TITLE'])
    
    # generating wordcloud
    wordcloud = WordCloud(max_words=1500,
                          max_font_size=350, random_state=42,
                          width=2000, height=1000,
                          colormap = "gist_stern")
    wordcloud.generate(texts)
    return wordcloud


def app():
    df, _  = data()
    pipe = joblib.load("data/pipeline.joblib")

    ht = eli5.show_weights(pipe[1:], top=(5, 5), targets=[1001396,
        1002509,
        1000953,
        1000950,
        1002517,
        1001428,
        1002513,
        1182207,
        1002518,
        1187203])

    raw_html = ht._repr_html_()
    components.v1.html(raw_html, scrolling=True, width=1270, height=368)

    w_wordcloud = worst_wc(df, pipe)
    fig_, ax = plt.subplots(figsize = (24, 13))
    ax.imshow(w_wordcloud, interpolation='bilinear')
    ax.axis("off")
    st.pyplot(fig_)

if __name__ == '__main__':
    app()