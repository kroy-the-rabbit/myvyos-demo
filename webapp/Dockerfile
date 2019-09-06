FROM python:3.7
ADD . /code
WORKDIR /code
RUN pip install -r requirements.txt
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
CMD python run.py
