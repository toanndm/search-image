FROM python:3 
WORKDIR /app
COPY . /app/
RUN apt-get update
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./server.py