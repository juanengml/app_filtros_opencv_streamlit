FROM python:3.8-slim-buster
COPY . /app
WORKDIR /app
RUN pip install -r requirimentes.txt
EXPOSE 8501
CMD streamlit run app.py