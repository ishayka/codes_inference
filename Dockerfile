FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip install flask
EXPOSE 105
CMD python app.py
