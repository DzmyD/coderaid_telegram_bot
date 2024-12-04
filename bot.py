import telebot  # Telegram bot
from telebot import types  # Для кнопок


# const
FILENAME_LIST = "list.txt"  # В конце обязателен перенос строки для корректной обработки последнего кода. В нем должно быть ровно 10 000 чисел
FILENAME_TOKEN = "token.txt"  # В конце не должно быть знака переноса строки
MAX_LEN_TEXT_MESSAGE = 4096  # Максимальное количество символов в 1 сообщении


# Придется создать класс, в котором будет записаны
# id сообщений от бота для каждого пользователя, использовавшего /gen x y
# Если команда используется заново, пересоздаем список id сообщений
# Если используется левая команда, очищаем список для этого пользователя
# Если список кодов перебран, удаляем этого пользователя из словаря
class ListGenId:
    # Поле словаря
    # user_id: [bot_message_id, bot_message_id0, ...]
    __user_dictionary = {}  # __ -> приватное поле

    # Конструктор
    def __init__(self):
        print("class ListGenId has been initialisated")
    
    # Добавить пользователя
    def addUser(self, p_user_id, p_list_messages):
        new_user = {p_user_id: p_list_messages}
        self.__user_dictionary.update(new_user)
    
    # Получить список bot_message_id
    # return deafult, если пользователь не был найден
    def getListMessageId(self, p_user_id, deafult={}):
        if p_user_id in self.__user_dictionary:
            return self.__user_dictionary[p_user_id]
        return deafult
    
    # Удаление пользователя
    # return {user_id: list_messages}
    # return {} если пользователь не был найден
    def delUser(self, p_user_1d):
        if p_user_1d in self.__user_dictionary:
            return_value = self.__user_dictionary[p_user_1d]
            del self.__user_dictionary[p_user_1d]
            return return_value
        return {}
    
    # Изменение списка
    # return False, если пользователь не был найден
    def changeUserList(self, p_user_id, p_list_messages):
        if p_user_id in self.__user_dictionary:
            self.__user_dictionary[p_user_id] = p_list_messages
            return True
        return False


# Возвращает список с кодами 0000..9999 где в начале самые используемые коды
# Считывает из файла и инверсирует полученный список
def getCodeListFromFile(filename):
    code_list = []
    file_list = open(filename, 'r')
    for i in range(10000):
        str_to_parse = file_list.readline()  # Потому что чтение происходит вместе с символом переноса
        code_list.append(str_to_parse[:-1])
    file_list.close()

    code_list.reverse()
    return code_list
'''
# Возвращает список с кодами 0000..9999 где в начале самые используемые коды
def getCodeListFromFile(filename):
    code_list = []
    for i in range(14):
        code_list.append(str(i))
    return code_list
'''
    

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


# Запуск кода, если этот файл - не модуль другого кода
if __name__ == '__main__':
    # Инициализация бота
    file_token = open(FILENAME_TOKEN, 'r')
    bot_token = file_token.readline()
    bot = telebot.TeleBot(bot_token)
    file_token.close()
    message_id_user_codes = ListGenId()


    # Команда /start
    @bot.message_handler(commands=['start'])  # команды, на которые он отвечает
    def start(message):
        print(message.date, message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.text)
        print(message_id_user_codes.getListMessageId(message.from_user.id))

        # Баг с кнопкой?
        a = telebot.types.ReplyKeyboardRemove()
        if message_id_user_codes.getListMessageId(message.from_user.id, False) != False:
            message_id_user_codes.delUser(message.from_user.id)
        bot.send_message(message.from_user.id, 'Подготовка к запуску...', reply_markup=a)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        bot.send_message(message.from_user.id, "Бот работает. Пользуйся командой /gen, но учти, что бот делался на коленке и возможны ошибки", reply_markup=markup)

    # Команда /gen x y
    # x - количество участников кодрейда
    # y - номер участника (от 0 до x -1)
    @bot.message_handler(commands=['gen'])
    def gen(message):
        print(message.date, message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.text)
        print(message_id_user_codes.getListMessageId(message.from_user.id))
        message_to_parse = message.text  # Иногда отправленное сообщение нужно пропарсить
        user_id = message.from_user.id  # Вместо тысячи слов)
        if (message_to_parse == '/gen'):  # Справочная информация о команде /gen
            a = telebot.types.ReplyKeyboardRemove()  # Заранее удаляем кнопки
            if message_id_user_codes.getListMessageId(user_id, False) != False:
                message_id_user_codes.delUser(user_id)
            bot.send_message(user_id, "/gen генерирует для тебя список по 2-м параметрам."+
                             "\n/gen count index\ncount - количество участников (минимум 2)\nindex - номер участника (отсчет начинается с 0 и не может быть больше или равен количеству участников)\n"+
                             "Не забудь поставить по пробелу между аргументами команды и любая команда начинается с /"+
                             "Пример команды:\n/gen 8 1\nСписок делится на 8 участников, вам достается 2-я часть этого списка", reply_markup=a)
        else:  # Обработка команды
            if (message_to_parse.count(" ") == 2):
                # Вытаскиваем аргументы и проверяем их
                member_count = message_to_parse[message_to_parse.find(" ") + 1:message_to_parse.rfind(" ")]  # Количество участников
                member_id = message_to_parse[message_to_parse.rfind(" ") + 1:]  # Номер участника
                try:  # Пробуем преобразовать аргументы в число и проверяем значения
                    member_count = int(member_count)
                    member_id = int(member_id)
                    if (member_count > 1 and 0 <= member_id < member_count):  # Аргументы корректные
                        a = telebot.types.ReplyKeyboardRemove()  # Заранее удаляем кнопки
                        if message_id_user_codes.getListMessageId(user_id, False) != False:
                            message_id_user_codes.delUser(user_id)
                        bot.send_message(user_id, "Команда введена корректно", reply_markup=a)
                        bot.send_message(user_id, "Удачного кодрейда!\nПомни, кнопка *Удалить* удаляет самый нижний код.\nВот ваш список:\n")
                        bot_text_message = ""

                        # Создаем список по параметрам и записываем его в bot_text_message
                        # Возможны проблемы с длиной сообщений, поэтому их стоит разбивать
                        # Telegram ограничивает длину сообщений в 4096 символов
                        len_message_counter = 0
                        list_message_bot_id = []  # Список для объекта
                        flag = False
                        main_list = getFragmentList(getCodeListFromFile(FILENAME_LIST), member_count, member_id)
                        for i in main_list:
                            if len_message_counter + 5 >= MAX_LEN_TEXT_MESSAGE:
                                bot_msg = bot.send_message(user_id, bot_text_message)
                                list_message_bot_id.append(bot_msg)
                                bot_text_message = ""
                                len_message_counter = 0
                                if main_list[-1] == i:
                                    flag = True
                                continue
                            bot_text_message = bot_text_message + i + "\n"
                            len_message_counter += 5
                    
                        # Создание кнопки Удалить
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
                        del_button = types.KeyboardButton("Удалить код")
                        markup.add(del_button)
                        if not flag:
                            bot_msg = bot.send_message(user_id, bot_text_message, reply_markup=markup)
                            list_message_bot_id.append(bot_msg)
                        message_id_user_codes.addUser(user_id, list_message_bot_id)
                    else:
                        raise ValueError()  # Иначе аргументы имеют нелогичные значения
                except ValueError:  # Ошибка указания параметра команды
                    a = telebot.types.ReplyKeyboardRemove()  # Заранее удаляем кнопки
                    if message_id_user_codes.getListMessageId(user_id, False) != False:
                        message_id_user_codes.delUser(user_id)
                    bot.send_message(user_id, "Аргументы команды /gen введены некорректно", reply_markup=a)

            else:  # Ошибка указания параметра команды
                a = telebot.types.ReplyKeyboardRemove()  # Заранее удаляем кнопки
                if message_id_user_codes.getListMessageId(user_id, False) != False:
                    message_id_user_codes.delUser(user_id)
                bot.send_message(user_id, "Команда /gen введена некорректно", reply_markup=a)

        

    @bot.message_handler(content_types='text')
    def message_reply(message):
        print(message.date, message.from_user.id, message.from_user.first_name, message.from_user.last_name, message.text)
        print(message_id_user_codes.getListMessageId(message.from_user.id))
        message_to_parse = message.text  # Иногда отправленное сообщение нужно пропарсить
        user_id = message.from_user.id  # Вместо тысячи слов)
        # Обработка команды Удалить код
        if (message_to_parse == "Удалить код"):
            # Для начала удаляем сообщение польвователя
            bot.delete_message(user_id, message.message_id)

            # Ищем последнее сообщение бота для этого пользователя
            list_msg_bot = message_id_user_codes.getListMessageId(user_id)
            last_msg_bot = list_msg_bot.pop()
            bot_text_to_parse = last_msg_bot.text


            if bot_text_to_parse.count("\n") >= 1:
                bot_text_to_parse = bot_text_to_parse[:bot_text_to_parse.rfind("\n"):]

                markup = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
                del_button = types.KeyboardButton("Удалить код")
                markup.add(del_button)
                bot.delete_message(user_id, last_msg_bot.message_id)

                msg_bot = bot.send_message(user_id, bot_text_to_parse, reply_markup=markup)
                list_msg_bot.append(msg_bot)
                message_id_user_codes.changeUserList(user_id, list_msg_bot)
                print('edited')
            elif len(list_msg_bot) == 0:
                bot.delete_message(user_id, last_msg_bot.message_id)
                markup = types.ReplyKeyboardRemove()
                bot.send_message(user_id, "Коды перебраны", reply_markup=markup)
                print("done")
            else:
                bot.delete_message(user_id, last_msg_bot.message_id)
                last_msg_bot = list_msg_bot.pop()

                markup = types.ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)
                del_button = types.KeyboardButton("Удалить код")
                markup.add(del_button)

                bot_msg = bot.send_message(user_id, last_msg_bot.text, reply_markup=markup)
                list_msg_bot.append(bot_msg)
                message_id_user_codes.changeUserList(user_id, list_msg_bot)
                print("next message")
            
                


    bot.polling(none_stop=True, interval=0) # обязательная для работы бота часть
