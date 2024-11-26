# CodeRaid Telegram Bot
Телеграм бот, отправляющий коды из 4-х чисел каждому участнику кодрейда в игре Rust.

### Инструкция по использованию:
1. Запустить бота на своем аккаунте.
2. Вводим команду `/gen x y`, где:
   * `/gen` отправка каждым сообщением по одному из вариантов 4-х значного числа;
   * `x` количество участников кодрейда;
   * `y` номер фрагмента списка чисел (числа будут генерироваться в порядке возрастания). Нужно заранее оговорить с остальными участниками какой номер будет присвоен каждому (начиная с 0, заканчивания `x - 1`);
3. При неудачной попытке удаляем сообщение с этим кодом и переходим на следующее.
