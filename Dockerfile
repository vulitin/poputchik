FROM python:3.8.10
ADD bot.py .
RUN pip install pyTelegramBotAPI
RUN pip install wheel
RUN pip install telebot
CMD python3 ./bot.py