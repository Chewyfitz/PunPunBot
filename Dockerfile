FROM python:3.8

WORKDIR /usr/src/bot

COPY . .

RUN pip install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

CMD python run.py
