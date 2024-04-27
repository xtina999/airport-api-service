FROM python:3.12.2
LABEL maintainer="tina.vasylenko@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

#RUN pip install -r requirements.txt
#RUN pip install --progress-bar off -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
#RUN adduser \
#    --disabled-password \
#    --no-create-home \
#    my_user
#
#
#USER my_user
