from main import DB_Manager
from config import *
from telebot import TeleBot

bot = TeleBot(TOKEN)
manager = DB_Manager(DATABASE)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот для получения статистики игроков НБА. 
Чтобы узнать статистику игрока, отправь мне его имя в формате /player <имя игрока>.
Чтобы получить список игроков из определенной команды, отправь мне команду в формате /team <название команды>.
Чтобы получить личную информацию игрока, отправь мне его имя в формате /data <имя игрока>.
""")

@bot.message_handler(commands=['player'])
def player_stats_command(message):
    player_name = message.text.split(' ', 1)[1]
    player_info = manager.get_player_stats_by_name(player_name)
    if player_info:
        player_id = player_info[0][0]
        stats = manager.get_player_stats_by_name(player_id)
        if stats:
            stats_message = f"Статистика игрока {player_name}:\n"
            for stat in stats:
                stats_message += f"Сезон: {stat[1]}, Игры: {stat[2]}, Очки: {stat[3]}, Подборы: {stat[4]}, Передачи: {stat[5]}\n"
            bot.send_message(message.chat.id, stats_message)
        else:
            bot.send_message(message.chat.id, f"Нет статистики для игрока {player_name}.")
    else:
        bot.send_message(message.chat.id, f"Игрок {player_name} не найден в базе данных.")
    
@bot.message_handler(commands=['data'])
def player_stats_command(message):
    player_name = message.text.split(' ', 1)[1]
    player_info = manager.get_player_data_by_name(player_name)
    if player_info:
        player_id = player_info[0][0]
        stats = manager.get_player_data_by_name(player_id)
        if stats:
            stats_message = f"Данные игрока {player_name}:\n"
            for stat in stats:
                stats_message += f"Сезон: {stat[1]}, Возраст: {stat[2]}, Рост: {stat[3]}, Вес: {stat[4]}, Колледж: {stat[5]}, Страна: {stat[6]}, Год_Драфта: {stat[7]}, Пик: {stat[8]}\n"
            bot.send_message(message.chat.id, stats_message)
        else:
            bot.send_message(message.chat.id, f"Нет данных для игрока {player_name}.")
    else:
        bot.send_message(message.chat.id, f"Игрок {player_name} не найден в базе данных.")

@bot.message_handler(commands=['team'])
def team_players_command(message):
    team_name = message.text.split(' ', 1)[1]
    players = manager.get_players_by_team(team_name)
    if players:
        players_list = "\n".join([f"{player[1]} ({player[2]})" for player in players])
        bot.send_message(message.chat.id, f"Нынешние игроки команды {team_name}:\n{players_list}")
    else:
        bot.send_message(message.chat.id, f"Команда {team_name} не найдена в базе данных.")

bot.infinity_polling()