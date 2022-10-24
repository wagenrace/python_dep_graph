FROM python:3.9

WORKDIR /code
RUN useradd wagenrace -m 
USER wagenrace

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app

CMD ["/home/wagenrace/.local/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--proxy-headers"]
