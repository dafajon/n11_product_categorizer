import click
import uvicorn
from datetime import datetime
import joblib
import pandas as pd
from rich.console import Console

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

from .inference_server import make_restful_api
from .utils import make_tokenizer, TextCleaner

today = datetime.today().strftime('%Y-%m-%d')
console = Console()

@click.group(help="N11 Product Categorizer Commandline")
def cli():
    pass

@cli.command(help="Run a training task on a specified dataset")
@click.option("-d", "--datapath", help="Path to dataset", default="~/.n11_data/train_n11.csv")
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
    df = pd.read_csv(datapath, sep='|',  encoding='utf-8')

    pipe = Pipeline([("text_clean", TextCleaner(to_clean=[title_col, text_col])),
                     ("text_transform", TfidfVectorizer(strip_accents='unicode', ngram_range=(1, 2), 
                                                        stop_words=stopwords, sublinear_tf=True, 
                                                        smooth_idf=False, tokenizer=make_tokenizer(5), 
                                                        max_df=0.85, min_df=200)),
                     ('logreg', LogisticRegression(solver='sag',random_state=42, n_jobs=-1))])

    console.log("Fitting pipeline...")
    pipe.fit(df[[text_col, title_col]], df[label_col].values)

    joblib.dump(pipe, f"backend/n11/models/pipeline.joblib")
    console.log("Pipeline saved!")


@cli.command(help="Serve a trained and dumped model")
@click.option("-m", "--model", help="Name of the model to be served", default=f"pipeline")
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
