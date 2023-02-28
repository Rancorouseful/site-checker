import telebot
import requests
import time

domens = ['.ru', '.com', '.рф', '.net', '.org', '.ru.net', '.pro', '.ua', ]

bot = telebot.TeleBot("6200720876:AAEKwg9_Igs5IkN6HcEmul57giwh5Xe7I6I")

@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_message(message.chat.id, 'Введи сайт, который хочешь проверить')

@bot.message_handler(content_types=['text'])
def check(message):
    if '.' in message.text:
        site = f'https://www.{message.text}'
        try:
            response = requests.get(site)
            bot.send_message(message.chat.id, '{0} существует'.format(site))
        except:
            bot.send_message(message.chat.id, '{0} не существует'.format(site))
    elif ' ' not in message.text:
        msg = bot.send_message(message.chat.id, 'Проверка доменов...')

        existing_domains = []
        not_existing_domains = []

        for domen in domens:
            site = f'https://www.{message.text}{domen}'
            try:
                response = requests.get(site)
                existing_domains.append(site)
            except:
                not_existing_domains.append(site)
                
        bot.delete_message(message.chat.id, msg.message_id)

        time.sleep(0.5)

        if len(existing_domains)!=0:
            bot.send_message(message.chat.id, 'Существующие домены:\n{0}'.format('\n'.join(existing_domains)))
        if len(not_existing_domains)!=0:  
            bot.send_message(message.chat.id, 'Домены\n{0}\nне существуют.'.format('\n'.join(not_existing_domains))) 
        return
    else:
        bot.send_message(message.chat.id, 'Некорректно указан домен.')
bot.infinity_polling()