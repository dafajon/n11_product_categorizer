from click.types import FloatRange
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from rich.console import Console
import sys

import joblib
import pandas as pd
import numpy as np
import os
import gc
from pydantic import BaseModel
from pydantic.typing import List, Optional


console = Console()

class N11Info(BaseModel):
    about: str
    maintainer: str

class PredictionRequest(BaseModel):
    content: Optional[List[dict]] 
    datapath: Optional[str] = None

class PredictionResponse(BaseModel):
    titles: List[str]
    descs: List[str]
    preds: List[int]
    top3: List[List[int]]
    top3prob: List[List[float]]
    rc: int
    message: str    


def make_restful_api(model_name: str, title_col: str = "TITLE", text_col: str = "DESCRIPTION"):
    app = FastAPI()

    try:
        if os.path.exists(f"n11/models/{model_name}.joblib"):
            console.log(f"Importing pipeline")
            pipe = joblib.load(f"n11/models/{model_name}.joblib")
        else:
            raise ValueError(f"The model file {model_name} does not exist. Please train one today.") 
    except Exception as e:
        console.log(f"{e}")
        sys.exit(1)

    @app.get("/", tags=["Landing"], summary="Redirect response")
    async def redirect_docs():
        return RedirectResponse("/docs")

    @app.get("/info", tags=["Information"], summary="N11 Desription.")
    async def n11_info():
        return N11Info(
            about="N11 Product Categorization Prediction Service.",
            maintainer="dorukhan.afacan@globalmaksimum.com"
        )

    @app.post("/n11/api/predict", tags=["Task"], response_model=PredictionResponse)
    async def inference(request: PredictionRequest):
        try:
            if request.content is not None:
                df = pd.DataFrame().from_records(request.content)
            elif request.datapath is not None:
                df = pd.read_parquet(request.datapath)

            preds = list(pipe.predict(df))
            titles = df[title_col].values.tolist()
            descriptions = df[text_col].values.tolist()

            class_labels = pipe.named_steps['logreg'].classes_
            prob_preds = pipe.predict_proba(df)
            top_n_pred = np.argsort(prob_preds, axis=1)[: ,-3:][:, ::-1]

            top3 = [[class_labels[ix] for ix in instance] for instance in top_n_pred]
            top3prob = [[prob_preds[i, ix] for ix in instance] for i, instance in enumerate(top_n_pred)]
            
            return PredictionResponse(titles=titles,
                                      descs=descriptions,
                                      preds=preds,
                                      top3=top3,
                                      top3prob=top3prob,
                                      rc=200,
                                      message="Prediction completed")
        except Exception as e:

            return PredictionResponse(titles=[], descs=[], preds=[], top3=[], top3prob=[], rc=500, message=f"Inference Error {e}")
     

    return app