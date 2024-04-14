import telebot;
from telebot import types;
#import time
from datetime import datetime

#from dateutil.parser import parse
#import logging

bot = telebot.TeleBot('YOUR_SECRET_TOKEN');

@bot.message_handler(content_types=['text'])
def start_message(message):
  bot.send_message(message.chat.id,"Приветствую, я бот для поиска попутчиков!")    

  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
  markup.add("Я водитель","Я пассажир")
  
  bot.send_message(message.chat.id, "Выберите свою роль в поездке:", reply_markup=markup)
  
  bot.register_next_step_handler(message, choosing_direction) #добавляем следующий шаг, перенаправляющий пользователя на message_input_step

def choosing_direction(message):
  global role
  role = message.text
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
  markup.add("В Город_1","В Город_2","В Город_3","В Город_4")
  
  bot.send_message(message.chat.id, "Выберите направление поездки:", reply_markup=markup)
  
  bot.register_next_step_handler(message, choosing_seats)

def choosing_seats(message):
  global direction
  direction = message.text
    
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
  markup.add("1","2","3","4")
  
  bot.send_message(message.chat.id, "Выберите необходимое количество мест:", reply_markup=markup)
  
  bot.register_next_step_handler(message, choosing_date)

def choosing_date(message):
  global seats
  seats = message.text
    
  bot.send_message(message.chat.id, "Введите дату поездки в формате ДД.ММ")
  
  bot.register_next_step_handler(message, choosing_time)

def choosing_time(message):
  global dateOfTrip
  
  try:
    dateOfTrip = message.text.replace(".","-") + '-' + datetime.now().year.__str__()
    dateOfTrip = datetime.strptime(dateOfTrip, '%d-%m-%Y')
    bot.send_message(message.chat.id, "Введите время поездки в формате ЧЧ:ММ")
    bot.register_next_step_handler(message, getting_phone)
  except ValueError:
    bot.send_message(message.chat.id, 'Не верный формат даты, необходимо ДД.ММ')
    bot.register_next_step_handler(message, choosing_time)
  
def getting_phone(message):
  global timeOfTrip
  
  try:
    timeOfTrip = message.text
    datetime.strptime(timeOfTrip, '%H:%M')
    bot.send_message(message.chat.id, "Введите контактный номер для связи")
    bot.register_next_step_handler(message, apply_publication)
  except ValueError:
    bot.send_message(message.chat.id, 'Не верный формат времени, необходимо ЧЧ:ММ')
    bot.register_next_step_handler(message, getting_phone)
  
def apply_publication(message):
    global phoneNumber
    phoneNumber = message.text.replace("+","\+")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add("Да","Нет")
    bot.send_message(message.chat.id, "Вы поедете: " + dateOfTrip.strftime("%d\-%m\-%Y")
                     + "\nВ: " + timeOfTrip
                     + "\nКуда: " + direction 
                     + "\nКак: " + role 
                     + "\nКоличество мест: " + seats
                     + "\nТелефон для связи: " + phoneNumber
                     + "\n*Опубликовать?*",
                     parse_mode='MarkdownV2',
                     reply_markup=markup)
    bot.register_next_step_handler(message, publish)

def publish(message):
  if message.text == "Да":
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add("START")
    bot.send_message(message.chat.id, "Опубликовано в Группу! Ждите звонка.")
    channel_id = "YOUR_CHANNEL_ID" #Private channel
    bot.send_message(channel_id, 
                     "\U0001F697 Поездка: " + dateOfTrip.strftime("%d-%m-%Y")
                     + "\nВ: " + timeOfTrip
                     + "\nКуда: #" + direction.replace(" ","_")
                     + "\nКак: #" + role.replace(" ","_")
                     + "\nКоличество мест: " + seats
                     + "\nТелефон для связи: " + phoneNumber.replace("\+","+"))
    bot.send_message(message.chat.id,"Для публикации еще одной поездки нажмите START.", reply_markup=markup)

  elif message.text == "Нет":
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=2)
    markup.add("START")
    bot.send_message(message.chat.id, "Окей, давай попробуем еще раз!)"
                     + "\nНажмите START", reply_markup=markup)
    bot.register_next_step_handler(message, start_message)

bot.polling(non_stop=True, interval=0)