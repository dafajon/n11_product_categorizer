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
    rc: int
    message: str
    #top5: List[List[str]]
    #top5_probs: List[List[float]]

    


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

            return PredictionResponse(titles=titles,
                                      descs=descriptions,
                                      preds=preds,
                                      rc=200,
                                      message="Prediction completed")
        except Exception as e:

            return PredictionResponse(titles=[], descs=[], preds=[], rc=500, message=f"Inference Error {e}")
     

    return app