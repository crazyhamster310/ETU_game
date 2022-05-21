from aiogram import Bot, Dispatcher, types
from data_base import con, cur


async def start(message: types.Message):
    # Добавление пользователя в БД (или обновление имени при повторном вызове)
    try:
        cur.execute(f"insert into user values (\"{message.chat.id}\", \"{message.chat.full_name}\")")
    except:
        cur.execute(f"update user set name=\"{message.chat.full_name}\" where ID_user=\"{message.chat.id}\"")
    con.commit()
    # Приветственное сообщение
    await message.answer("Добро пожаловать в квест \"Поступи в Университет\"\n\nВведите /info, чтобы получить больше информации об игре\nДля начала/продолжения квеста используйте /quest\nЧтобы сбросить прогресс прохождения, отправьте /cancel\n\nПриятной игры!", reply_markup=types.ReplyKeyboardRemove())


# Вывод информации об игре
async def info(message: types.Message):
    await message.answer("Для выбора реплик в диалогах можно использовать голосовые сообщения, содержащие номер выбранного ответа\n\nДля Вашего удобства текст игры будет дублироваться в голосовых сообщениях\n\nСюжет:\n     Действие происходит в июне. Главным героем является 11-классник Миша, который собирается поступать в один из лучших ВУЗов страны. Получив результаты ЕГЭ, Миша не верит своим глазам: у него по всем экзаменам <b>0 баллов</b>.\n     Он был тем, на кого возлагали свои надежды все учителя, тем, кто имел по всем предметам <b>средний балл 5.00</b>. Да и сам Миша рассчитывал на высокий балл!\n     Пока все его друзья выбирают высшие образовательные учреждения, он ищет решения своей проблемы. Его переполняет гнев и ярость. Тут явно произошла какая-то ошибка. Даже те, кто с горем пополам аттестовались в 11 классе сумели получить результаты выше результатов отличника-олимпиадника.\n     Через время до него дошел слух о том, что в другой школе его города <b>круглый троечник</b>, который совсем не готовился к экзаменам, получил по всем экзаменам <b>100 баллов</b>. Какая несправедливость! <i>А вдруг этот человек украл его баллы?</i>…", parse_mode=types.ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())


# Регистрация команд
def register_handlers_menu(dp: Dispatcher):
    dp.register_message_handler(start, commands="start")
    dp.register_message_handler(info, commands="info")


# Маленькое меню для бота
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Вывести приветствие"),
        types.BotCommand(command="/quest", description="Начать/Продолжить квест"),
        types.BotCommand(command="/cancel", description="Сбросить прогресс прохождения"),
        types.BotCommand(command="/info", description="Вывести информацию об игре")
    ]
    await bot.set_my_commands(commands)
