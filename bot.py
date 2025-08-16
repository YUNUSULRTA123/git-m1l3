import telebot # библиотека telebot
import sys
import os
sys.path.append(os.getcwd())
from config import token # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, """ℹ️ Мои команды:
/start – 🖐 Стартовое сообщение, приветствие в чате  
/info – 📖 Краткая справка о командах бота  
/ban – 🔨 Забанить пользователя (отправляется в ответ на сообщение)
/unban – ♻️ Разбанить пользователя (отправляется в ответ на сообщение) 
/mute – 🔇 Замьютить пользователя (отправляется в ответ на сообщение) 
/unmute – 🔊 Размьютить пользователя (отправляется в ответ на сообщение)
В случае помощи обращайтесь - @yunus_pro_hour_of_code
⚠️ ВАЖНО: Нельзя банить или мьютить 👑 администраторов и создателя чата.
""")
    bot.reply_to(message, "Используйте меня с умом")
    
@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")

@bot.message_handler(commands=['unban'])
def unban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно забанить или же разбанить администратора.")
        else:
            bot.unban_chat_member(chat_id, user_id) # пользователь с user_id будет разбанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был разбанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите разбанить.")

@bot.message_handler(commands=['mute'])
def mute_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно замютить администратора.")
        else:
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=False) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был замютен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите замютить.")

@bot.message_handler(commands=['unmute'])
def unmute_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        if user_status == 'administrator' or user_status == 'creator':
            bot.reply_to(message, "Невозможно замютить или же размютить администратора.")
        else:
            bot.restrict_chat_member(chat_id, user_id, can_send_messages=True) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был размютен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите размютить.")

@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, 'Я принял нового участника!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if "https://" in message.text:
        user_info = {
            "chat_id": message.chat.id,
            "user_id": message.from_user.id,
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
            "text": message.text
        }
        bot.reply_to(message, f"Пользователь с ссылкой - {user_info}")
        try:
            bot.ban_chat_member(message.chat.id, message.from_user.id)
            bot.reply_to(message, f"""Пользователь @{message.reply_to_message.from_user.username} был забанен по причине отправки ссылок.
Отправлять ссылки в данный чат  КАТЕГОРИЧЕСКИ ЗАПРЕЩЕНО !!!!!""")
        except Exception as e:
            bot.reply_to(message, "Не удалось забанить пользователя")
    else:    
        bot.reply_to(message, message.text)

if __name__ == "__main__":
    print("Бот запустился...")
    bot.polling()
