# Scan a directory of audio files and get their spectogram. Requires ffmpeg to be installed.

from os import listdir, mkdir
from os.path import isfile, join
from subprocess import run

onlyfiles = [f for f in listdir('.') if isfile(join('.', f))]

filetype = input("Filetype (eg. .flac, .mp3, etc.) Include the dot ")

mkdir('./scans')
for i in onlyfiles:
    name = i[:len(i) - len(filetype)]
    run(['ffmpeg', '-y', '-i', f'{i}', '-lavfi', 'showspectrumpic=s=1000x512:mode=combined:color=rainbow:gain=0.5', f'./scans/{name}.png'])
