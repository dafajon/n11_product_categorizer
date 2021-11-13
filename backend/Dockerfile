FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

RUN mkdir /fastapi

COPY requirements.txt /fastapi

WORKDIR /fastapi

RUN pip install -r requirements.txt

COPY . /fastapi

RUN pip install -e .

EXPOSE 8000

CMD ["n11", "serve"]
