import os

# Возвращает список с кодами 0000..9999 в порядке возрастания
def getCodeList():
    code_list = []  # Список, в котором будет хранится все возможные варианты для двери
    for i in range (10000):
        code = str(i)
        for j in range(3):
            if len(code) != 4:
                code = '0' + code
            else:
                break
        code_list.append(code)
    return code_list


# Возвращает список с кодами 0000..9999 где в начале самые используемые коды
def getCodeListFromFile(filename):
    code_list = []
    file_list = open(filename, 'r')
    for i in range(10000):
        str_to_parse = file_list.readline()  # Потому что чтение происходит вместе с символом переноса
        code_list.append(str_to_parse[:-1])
    file_list.close()
    return code_list

print(len(getCodeListFromFile('list.txt')[-1]))
