import telebot  # Telegram bot
from telebot import types  # Для кнопок


# const
FILENAME_LIST = "list.txt"  # В конце обязателен перенос строки для корректной обработки последнего кода. В нем должно быть ровно 10 000 чисел
FILENAME_TOKEN = "token.txt"  # В конце не должно быть знака переноса строки


# Возвращает фрагмент списка по параметрам
# p_count - количество разбитых кусков
# p_index - номер куска списка
# МОЖЕТ РАБОТАТЬ НЕКОРРЕКТНО С ПРОИЗВОЛЬНЫМИ ЗНАЧЕНИЯМИ
def getFragmentList(p_list, p_count, p_index):
    # Разбиваем список на равные части
    x = len(p_list) // p_count
    result = [p_list[i:i + x] for i in range(0, len(p_list), x)]  # Если на равные части разбить не удалось, то остаточный список будет в конце

    # Если же остаточный список появился
    if p_count != len(result):
        list_buffer = result.pop()  # Вытаскиваем остаток в буфер
        # и раскидываем его элементы по первым кускам
        counter = 0  # Счетчик на всякий случай
        for i in list_buffer:
            if counter == p_count:
                counter = 0
                continue
            result[counter].append(i)
            counter += 1
    
    return result[p_index]  # Возвращаем кусок p_list по его номеру


# Возвращает фрагмент списка по параметрам
# p_count - количество разбитых кусков
# p_index - номер куска списка
# МОЖЕТ РАБОТАТЬ НЕКОРРЕКТНО С ПРОИЗВОЛЬНЫМИ ЗНАЧЕНИЯМИ
def getFragmentList(list, p_count, p_index):
    result = []
    return result

# Запуск кода, если этот файл - не модуль другого кода
if __name__ == '__main__':
    # Инициализация бота
    file_token = open(FILENAME_TOKEN, 'r')
    bot_token = file_token.readline()
    bot = telebot.TeleBot(bot_token)
    file_token.close()

    # Команда /start
    @bot.message_handler(commands=['start'])  # команды, на которые он отвечает
    def start(message):
        print(message.from_user.id, message.text)

        # Баг с кнопкой?
        a = telebot.types.ReplyKeyboardRemove()
        bot.send_message(message.from_user.id, 'Подготовка к запуску...', reply_markup=a)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.from_user.id, "Бот работает. Пользуйся командой /gen, но учти, что бот делался на коленке и возможны ошибки", reply_markup=markup)

    # Команда /gen x y
    # x - количество участников кодрейда
    # y - номер участника (от 0 до x -1)
    @bot.message_handler(commands=['gen'])
    def gen(message):
        print(message.from_user.id, message.text)
        message_to_parse = message.text  # Иногда отправленное сообщение нужно пропарсить
        user_id = message.from_user.id  # Вместо тысячи слов)
        if (message_to_parse == '/gen'):  # Справочная информация о команде /gen
            bot.send_message(user_id, "/gen генерирует для тебя список по 2-м параметрам."+
                             "\n/gen count index\ncount - количество участников (минимум 2)\nindex - номер участника (отсчет начинается с 0 и не может быть больше или равен количеству участников)\n"+
                             "Не забудь поставить по пробелу между аргументами команды и любая команда начинается с /"+
                             "Пример команды:\n/gen 8 1\nСписок делится на 8 участников, вам достается 2-я часть этого списка")
        else:  # Обработка команды
            if (message_to_parse.count(" ") == 2):
                # Вытаскиваем аргументы и проверяем их
                member_count = message_to_parse[message_to_parse.find(" ") + 1:message_to_parse.rfind(" ")]  # Количество участников
                member_id = message_to_parse[message_to_parse.rfind(" ") + 1:]  # Номер участника
                try:  # Пробуем преобразовать аргументы в число и проверяем значения
                    member_count = int(member_count)
                    member_id = int(member_id)
                    if (member_count > 1 and 0 <= member_id < member_count):  # Аргументы корректные
                        bot.send_message(user_id, "Команда введена корректно")
                        # вывод списка и перенос
                    else:
                        raise ValueError()  # Иначе аргументы имеют нелогичные значения
                except ValueError:  # Ошибка указания параметра команды
                    bot.send_message(user_id, "Аргументы команды /gen введены некорректно")

            else:  # Ошибка указания параметра команды
                bot.send_message(user_id, "Команда /gen введена некорректно")


    bot.polling(none_stop=True, interval=0) # обязательная для работы бота часть
