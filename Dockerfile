FROM python:3 
WORKDIR /app
COPY . /app/
RUN pip install -r requirements.txt
EXPOSE 3000
CMD python ./server.py