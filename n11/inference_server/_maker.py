from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from rich.console import Console

import joblib
import pandas as pd
import numpy as np
import gc
from typing import List
from pydantic import BaseModel
from pydantic.typing import List, Optional


console = Console()

class N11Info(BaseModel):
    about: str
    maintainer: str

class PredictionRequest(BaseModel):
    content: Optional[List[dict]]
    datapath: Optional[str]

class PredictionResponse(BaseModel):
    text: List[str]
    top5: List[List[str]]
    top5_probs: List[List[float]]

    rc: int
    messsage: str


def make_restful_api(model_name: str):
    app = FastAPI()

    # TODO: Add necessary checks for model and encoder files 

    @app.get("/", tags=["Landing"], summary="Redirect response")
    async def redirect_docs():
        return RedirectResponse("/docs")

    @app.get("/info", tags=["Information"], summary="HierNN Desription.")
    async def hiernn_info():
        return N11Info(
            about="N11 Product Categorization Prediction Service.",
            maintainer="dorukhan.afacan@globalmaksimum.com"
        )

    @app.post("/n11/api/predict", tags=["Task"], response_model=PredictionResponse)
    async def predict(request: PredictionRequest):
        try:
            if request.content is not None:
                df = pd.DataFrame().from_records(request.content)
            elif request.datapath is not None:
                df = pd.read_parquet(request.datapath)


        # TODO: Inference pipeline

            return PredictionResponse(text=texts,
                                      top5=top5,
                                      top5_probs=top5_probs,
                                      rc=200,
                                      message="Prediction completed")

        except Exception as e:
            return PredictionResponse(text=texts,
                                      top5=top5,
                                      top5_probs=top5_probs,
                                      rc=401,
                                      message=f"Prediction failed: {e}")

    return app