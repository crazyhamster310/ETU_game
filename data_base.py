import sqlite3
import pyttsx3
import os

con = sqlite3.connect('telegram_quest.db')
cur = con.cursor()


# Добавление текста в таблицу quest из текстового файла
def new_quest_text():
    f = open('strings_for_db.txt', "rt")
    text = ""
    cur.execute(f"insert into quest (description) values (\'{text}\')")
    con.commit()
    for line in f:
        if line == "1\n":
            temp = f.readline()
            cur.execute(f"update quest set Action1_text=\'{temp}\' where description=\'{text}\'")
        elif line == "2\n":
            temp = f.readline()
            cur.execute(f"update quest set Action2_text=\'{temp}\' where description=\'{text}\'")
        elif line == "3\n":
            temp = f.readline()
            cur.execute(f"update quest set Action3_text=\'{temp}\' where description=\'{text}\'")
        else:
            temp_text = text + line + "\n"
            cur.execute(f"update quest set description=\'{temp_text}\' where description=\'{text}\'")
            text += line + "\n"
        con.commit()


# Запись аудио-сообщений и добавление их имен в таблицу audio
def new_quest_audio():
    tts = pyttsx3.init()
    ru_voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
    tts.setProperty('voice', ru_voice_id)
    cur.execute("select * from quest")
    quest = cur.fetchall()
    if not os.path.exists("audio"):
        os.mkdir("audio")
    for zap in quest:
        cur.execute(f"insert into audio (ID_quest) values ({zap[0]})")
        con.commit()
        file_path = "./audio/description_" + str(zap[0]) + ".ogg"
        tts.save_to_file(zap[1], file_path)
        tts.runAndWait()
        cur.execute(f"update audio set audio_description=\'{file_path}\' where ID_quest={zap[0]}")
        con.commit()
        if zap[2]:
            tts.stop()
            file_path = "./audio/action1_" + str(zap[0]) + ".ogg"
            tts.save_to_file(zap[2], file_path)
            tts.runAndWait()
            cur.execute(f"update audio set action1_audio=\'{file_path}\' where ID_quest={zap[0]}")
            con.commit()
        if zap[4]:
            tts.stop()
            file_path = "./audio/action2_" + str(zap[0]) + ".ogg"
            tts.save_to_file(zap[4], file_path)
            tts.runAndWait()
            cur.execute(f"update audio set action2_audio=\'{file_path}\' where ID_quest={zap[0]}")
            con.commit()
        if zap[6]:
            tts.stop()
            file_path = "./audio/action3_" + str(zap[0]) + ".ogg"
            tts.save_to_file(zap[6], file_path)
            tts.runAndWait()
            cur.execute(f"update audio set action3_audio=\'{file_path}\' where ID_quest={zap[0]}")
            con.commit()


# new_quest_text()
# new_quest_audio()
