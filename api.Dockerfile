FROM python:3.11-slim-bookworm

RUN apt-get update

RUN apt-get autoremove -y \
    && apt-get clean -y \
    && apt-get autoclean -y

WORKDIR /home

COPY ./pyproject.toml ./requirements.txt ./

COPY ./app ./app

RUN pip install --no-cache-dir --upgrade -r requirements.txt

CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000" ]