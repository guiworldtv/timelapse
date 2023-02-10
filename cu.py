import streamlink
import moviepy.editor as mp
import subprocess
import os
import time

# URL do stream de vídeo
video_url = "https://5a7d54e35f9d2.streamlock.net/morromendanha1/morromendanha1.stream/chunklist_w182959856.m3u8"

# URL do stream de áudio
audio_url = "http://200.137.217.155:8010/radiouniversitaria"

# Tempo de captura de cada frame (em segundos)
capture_time = 2

# Número de frames a serem capturados
num_frames = 240  # reduzido para 2 minutos de duração

# FPS da timelapse
fps = 30

# Iniciar o stream de vídeo
video_streams = streamlink.streams(video_url)
video_stream = video_streams["best"]

# Iniciar a captura de frames
for i in range(num_frames):
    filename = "frame_{}.png".format(i)
    subprocess.call(["ffmpeg", "-i", video_stream.url, "-vframes", "1", "-r", str(fps), filename])
    time.sleep(capture_time)

# Criar o vídeo a partir dos frames capturados
filenames = ["frame_{}.png".format(i) for i in range(num_frames)]
clip = mp.ImageSequenceClip(filenames, fps=fps)

# Adicionar a faixa de áudio ao vídeo
audio_clip = mp.AudioFileClip(audio_url)
final_clip = mp.CompositeVideoClip([clip, audio_clip])

final_clip.write_videofile("timelapse.mp4", preset='ultrafast')

# Limpar os arquivos de frame
for filename in filenames:
    os.remove(filename)
