import telebot
import random
import datetime

token = '6167386914:AAF0VvsAJKqR_IGzdIQuoDeSarN2JNI6HDU'

bot = telebot.TeleBot(token)
HELP = """
- /help - напечатать справку по программе.
- /start - напечатать справку по программе.
- /add - добавить задачу в список в формате: /add <date task >.
- /show - напечатать все добавленные задачи в формате: /show <date>.
- /print - напечатать все добавленные задачи в формате: /print date.
- /random - добавлять случайную задачу на дату Сегодня."""

tasks = {}
RANDOM_TASKS = ['Записаться на курс в Нетологию', 'Написать Гвидо письмо', 'Покормить кошку', 'Помыть машину']


def add_todo(date, task):
    date = date.lower()
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = [task]


@bot.message_handler(commands=['add'])
def add_task(message):
    _, date, task = message.text.split(maxsplit=2)

    if len(task) < 3:
        text = 'Ошибка! Задача слишком короткая'
    else:
        add_todo(date, task)
        text = f'Задача: "{task}" записана на дату: "{date}"'

    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['random'])
def add_random_task(message):
    task = random.choice(RANDOM_TASKS)
    date = datetime.datetime.today().strftime('%d.%m.%Y')
    add_todo(date, task)
    bot.send_message(message.chat.id, f'Задача: "{task}" записана на cегодняшнюю дату: {date}')


@bot.message_handler(commands=['start', 'help'])
def help_start(message):
    bot.send_message(message.chat.id, HELP)


@bot.message_handler(commands=['show', 'print'])
def show_task(message):
    dates = message.text.split(maxsplit=1)[1].split()
    list_message = message.text.split(maxsplit=1)
    date = list_message[1]
    text = ''
    for date in dates:
        if date in tasks:
            text += date + '\n'
            for task in tasks[date]:
                text += f'- {task}\n'

        else:
            text = 'Задач на такую дату нет'
    bot.send_message(message.chat.id, text)


bot.polling(none_stop=True)
