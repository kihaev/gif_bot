FROM python:3.7

RUN pip install python-telegram-bot
RUN pip install requests

RUN mkdir /gif_bot
ADD . /gif_bot
WORKDIR /gif_bot

CMD python /gif_bot/bot.py
