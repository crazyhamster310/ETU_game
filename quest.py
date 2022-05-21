from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State
from voice import voice_handler
from data_base import con, cur

answers = []
waiting_for_answer = State()
id_quest = 1


# Вывод текстового и голосового сообщений, клавиатуры
async def story(message: types.Message):
    global id_quest, answers
    answers = []
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    cur.execute(f"select * from quest where ID_quest={id_quest}")
    text_story = cur.fetchone()
    cur.execute(f"select * from audio where ID_quest={id_quest}")
    audio_story = cur.fetchone()
    voice = open(audio_story[2], "rb")
    await message.answer_voice(voice)
    await message.answer(text_story[1])
    answers.append("1")
    voice = open(audio_story[3], "rb")
    await message.answer_voice(voice)
    voice.close()
    await message.answer("1." + text_story[2])
    if text_story[4]:
        answers.append("2")
        voice = open(audio_story[4], "rb")
        await message.answer_voice(voice)
        await message.answer("2." + text_story[4])
        voice.close()
    if text_story[6]:
        answers.append("3")
        voice = open(audio_story[5], "rb")
        await message.answer_voice(voice)
        await message.answer("3." + text_story[6])
        voice.close()
    keyboard.add(*answers)
    await message.answer("Ты выбираешь?", reply_markup=keyboard)
    await waiting_for_answer.set()


# Машина состояний для проверки корректности ввода номера варианта
async def answer_chosen(message: types.Message, state: FSMContext):
    global answers, id_quest
    text = ""
    if message.content_type == types.ContentType.VOICE:
        voice = await message.voice.get_file()
        path = f"./voices/{message.chat.full_name}"
        text = await voice_handler(voice, path)
    elif message.content_type == types.ContentType.TEXT:
        text = message.text
    if text not in answers:
        await message.answer("Некорректный ответ. Повторите попытку")
        return
    await state.update_data(chosen_answer=text)
    user_data = await state.get_data()
    await message.answer("Ответ принят", reply_markup=types.ReplyKeyboardRemove())
    await state.finish()
    if isinstance(message.content_type, types.ContentType.VOICE):
        cur.execute(f"insert into user_story (ID_quest,ID_user,action_num,audio_name) values ({id_quest}, {message.chat.id}, {int(user_data['chosen_answer'])}, \'{path + '/' + voice.file_id + '.ogg'}\')")
    else:
        cur.execute(f"insert into user_story (ID_quest,ID_user,action_num) values ({id_quest}, {message.chat.id}, {int(user_data['chosen_answer'])})")
    con.commit()
    await quest(message)


# Начало прохождения квеста или возвращение к нему после других команд
async def quest(message: types.Message):
    cur.execute(f"select * from user_story where ID_user={message.chat.id} order by ID_story desc")
    last = cur.fetchone()
    global id_quest
    if (not last) or last[1] == -1:
        id_quest = 1
        await story(message)
    else:
        cur.execute(f"select * from quest where ID_quest={last[1]}")
        id_quest = cur.fetchone()[last[3] * 2 + 1]
        if id_quest == -1:
            await message.answer("Вы прошли квест!\n\nПоздравляем!")
            cur.execute(f"insert into user_story (ID_quest, ID_user) values ({id_quest}, {message.chat.id})")
            con.commit()
        else:
            await story(message)


# Сброс прогресса квеста
async def cancel(message: types.Message):
    cur.execute(f"select * from user_story where ID_user={message.chat.id} order by ID_story desc")
    last = cur.fetchone()
    if last and last[1] != -1:
        try:
            cur.execute(f"update user_story set ID_quest=-1 where ID_story={last[0]}")
            await message.answer("Прогресс сброшен.", reply_markup=types.ReplyKeyboardRemove())
        except:
            await message.answer("Ошибка сброса: в квесте не выбрано ни одного ответа.", reply_markup=types.ReplyKeyboardRemove())
    else:
        await message.answer("Ошибка сброса: в квесте не выбрано ни одного ответа.", reply_markup=types.ReplyKeyboardRemove())
    con.commit()


# Регистрация команд
def register_handlers_quest(dp: Dispatcher):
    dp.register_message_handler(quest, commands="quest", state="*")
    dp.register_message_handler(cancel, commands="cancel", state="*")
    dp.register_message_handler(answer_chosen, state=waiting_for_answer, content_types=[types.ContentType.TEXT, types.ContentType.VOICE])
