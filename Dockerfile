FROM python:3.9

COPY ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

COPY ./src ./app/src
ENV FLASK_APP=/app/src

ENTRYPOINT [ "flask", "run", "--host=0.0.0.0", "--debug" ]