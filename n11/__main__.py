import click
import uvicorn
import datetime
import joblib
import pandas as pd
from rich.console import Console

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline

from .inference_server import make_restful_api
from .utils import make_tokenizer

today = datetime.today().strftime('%Y-%m-%d')
console = Console()

@click.group(help="N11 Product Categorizer Commandline")
def cli():
    pass

@click.option("-d", "--datapath", help="Path to dataset")
@click.option("-x", "--text-col", help="Text column", default="DESCRIPTION")
@click.option("-t", "--title-col", help="Title column", default="TITLE")
@click.option("-l", "--label-col", help="Label column", default="CATEGORY_ID")
def train(datapath: str, text_col: str, title_col: str, label_col: str):
    try:
        import nltk
        nltk.download('stopwords')
        from nltk.corpus import stopwords
        stopwords = set(stopwords.words('turkish'))
    except:
        raise ImportError("NLTK not available")

    console.log("Reading data...")

    df = pd.read_csv(datapath, nrows=5_000)

    column_trans = ColumnTransformer(
        [("word_ngram", TfidfVectorizer(strip_accents='unicode', ngram_range=(1, 2), stop_words=stopwords, sublinear_tf=True, smooth_idf=False, tokenizer=make_tokenizer(5)), [text_col, title_col]),
         ("char_ngram", TfidfVectorizer(strip_accents='unicode', ngram_range=(1, 3), stop_words=stopwords, sublinear_tf=True, smooth_idf=False, analyzer="char"), [text_col, title_col])]

    )

    pipe = Pipeline([("column_transformer", column_trans),
                     ("linear_svc", LinearSVC(C=3.995737425961318, intercept_scaling=2.7229092594601005))])

    console.log("Fitting pipeline...")
    pipe.fit(df[[text_col, title_col]], df[label_col])

    joblib.dump(pipe, f"n11/models/pipeline_{today}.joblib")

    console.log("Pipeline saved!")

@cli.command(help="Serve a trained and dumped model")
@click.option("-m", "--model", help="Name of the model to be served")
@click.option( "-h", "--host", help="Hostname", default="0.0.0.0")
@click.option("-l","--log-level",
              type=click.Choice(['debug', 'info'], case_sensitive=False), help="Logging Level", default="info")
@click.option("-r", "--re_load", is_flag=True, default=False, help="enable/disable auto reload for development.")
@click.option("-p", "--port", help="Port", default=8000)
def serve(model, host, log_level, re_load, port):
    app = make_restful_api(model)
    uvicorn.run(app, host=host, log_level=log_level, reload=re_load, port=port)


if __name__ == '__main__':
    cli()
