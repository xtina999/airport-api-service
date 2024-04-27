FROM python:3.12.2
LABEL maintainer="tina.vasylenko@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /files/media
# Додаємо нового користувача з ім'ям my_user
RUN adduser  \
    --disabled-password \
    --no-create-home  \
    my_user

# Змінюємо власника для папки /files/media на нового користувача my_user
RUN chown -R my_user /files/media

# Змінюємо дозволи доступу до папки /files/media
RUN chmod -R 755 /files/media

# Встановлюємо користувача за замовчуванням для подальших операцій
USER my_user