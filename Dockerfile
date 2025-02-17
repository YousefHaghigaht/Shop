FROM python:3.12

LABEL maintainer='yousefmpym1@gmail.com'
LABEL version=1.1

WORKDIR /src

COPY requirements.txt /src

RUN pip install -U pip
RUN pip install -r requirements.txt

COPY . /src

CMD ["python","manage.py","runserver"]
