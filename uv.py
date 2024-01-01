from math import floor
from pygame import mixer
from mutagen.mp3 import MP3
import time
import os

def play_mp3(file_path):
    try:
        # Load the MP3 file
        mixer.music.load(file_path)

        # Play the MP3 file
        mixer.music.play()

        # Wait while the music is playing
        while mixer.music.get_busy():
            time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
        
def clear():
    os.system('cls')
        
def resetLine():
    print(f"\033[A\r{' '*80}\r", end='')

def choose(menu, multiple=False, fancy_menu=None):
    if len(menu) != len(fancy_menu):
        raise Exception

    if fancy_menu:
        for index, item in enumerate(fancy_menu):
            if index < 10:
                print(f'{index}  {item}')
            else:
                print(f'{index} {item}')
    else:
        for index, item in enumerate(menu):
            if index < 10:
                print(f'{index}  {item}')
            else:
                print(f'{index} {item}')
    
    while True:
        choice = input(">> ")
        if choice == "":
            resetLine()
            continue

        if not multiple:
            choice_num = 0
            try:
                _num= int(choice)
                if (_num < 0 or _num >= len(menu)):
                    raise Exception
                choice_num = int(choice)
            except:
                resetLine()
                continue
            choice_item = menu[choice_num]
            return choice_item
        else:
            choices = choice.split()
            choices_num = []
            try:
                for num in choices:
                    _num = int(num)
                    if (_num < 0 or _num >= len(menu)):
                        raise Exception
                    choices_num.append(_num)
            except:
                resetLine()
                continue
            choice_items = [menu[num] for num in choices_num]
            return choice_items

def get_subfolders(directory):
    try:
        subfolders = [f.path for f in os.scandir(directory) if f.is_dir()]
        return subfolders
    except OSError as e:
        print(f"Error: {e}")
        return []

def get_files(directory):
    try:
        files = [f.path for f in os.scandir(directory) if f.is_file()]
        
        if directory + '\\desktop.ini' in files:
            files.remove(directory + '\\desktop.ini')
            
        return files
    except OSError as e:
        print(f"Error: {e}")
        return []

def select_folder():
    folder = get_subfolders(uv_folder_path)
    _folders = [folder.split('\\')[-1] for folder in folder]
    folder = choose(folder, fancy_menu=_folders)
    return folder

def select_songs(folder):
    songs = get_files(folder)
    _songs = [song.split('\\')[-1][0:-4] for song in songs]
    vibes = choose(songs, multiple=True, fancy_menu=_songs)
    return vibes

def get_time(song):
    duration = int(MP3(song).info.length)
    seconds = duration % 60
    minutes = floor((duration / 60))
    hours = floor(minutes / 60)
    minutes %= 60
    
    seconds_str = str(seconds).rjust(2, '0')
    
    if hours > 0:
        minutes_str = str(minutes).rjust(2, '0')
    else:
        minutes_str = str(minutes)
        
    hours_str = str(hours)
    
    time = ""
    
    if hours > 0:
        time = f'{hours_str}:{minutes_str}:{seconds_str}'.ljust(7, ' ')
    else:
        time = f'{minutes_str}:{seconds_str}'.ljust(7, ' ')
    
    return time

def play_songs(songs):
    for song in songs:
        time = get_time(song)
        print(f'  {time} ' +song.split('\\')[-1][0:-4])
    
    for index, song in enumerate(songs):
        num = len(songs) - index
        up = '\033[A' * num
        down = '\n' * num
        print(f"{up}\r>{down}", end='')
        play_mp3(song)
        print(f"{up}\r {down}", end='')

uv_folder_path = 'C:\\Users\\Teo\\Documents\\UV'

if __name__ == "__main__":
    mixer.init()
    
    clear()
    folder = select_folder()
    clear()
    songs = select_songs(folder)
    clear()
    play_songs(songs)
    
    mixer.quit()