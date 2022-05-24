from aiogram import Bot, types
import subprocess
from pathlib import Path
import speech_recognition as speech_r


# Загрузка голосового сообщения из чата
async def handle_file(file: types.File, file_name: str, path: str):
    bot = Bot(token="5343628425:AAGA9SgrATyJiqxHDDIUO4a3RDDiC8GCUiQ")
    Path(f"{path}").mkdir(parents=True, exist_ok=True)
    await bot.download_file(file_path=file.file_path, destination=f"{path}/{file_name}")


# Распознавание речи
async def recognise(filename):
    r = speech_r.Recognizer()
    with speech_r.AudioFile(filename) as source:
        audio_text = r.listen(source)
        try:
            text = str(r.recognize_google(audio_text, language="ru-RU"))
            print(text)
            return text
        except:
            print(0)
            return "0"


# Получение файла и подготовка для распознавания
async def voice_handler(voice: types.File, path: str):
    await handle_file(voice, f"{voice.file_id}.ogg", path)
    file_name_full = f"{path}/{voice.file_id}.ogg"
    file_name_converted = f"{path}/{voice.file_id}.wav"
    subprocess.run(['./FFmpeg/bin/ffmpeg.exe', '-i', file_name_full, file_name_converted])
    text = await recognise(file_name_converted)
    return text
