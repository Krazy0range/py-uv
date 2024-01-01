from math import floor
import random
import time
import os
from pygame import mixer
from mutagen.mp3 import MP3

width = 80

def end():
    clear()
    mixer.quit()
    quit()

def play_song(file_path):
    mixer.music.load(file_path)

    mixer.music.play()

    while mixer.music.get_busy():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            end()
        
def clear():
    os.system('cls')
        
def resetLine():
    print(f"\033[A\r{' '*80}\r", end='')

def print_menu(menu):
    index_width = 5
    is_even = lambda x: x % 2 == 0
    even_off = '\033[48;5;235;3m'
    odd_off = '\033[48;5;240;3m'
    reset_dim = '\033[23m'
    even = '\033[48;5;235m'
    odd = '\033[48;5;240m'
    reset = '\033[0m'
    for index, item in enumerate(menu):
        print(f'{even_off if is_even(index) else odd_off}{str(index).ljust(index_width, " ")}{reset_dim}{even if is_even(index) else odd}{item.ljust(width - index_width, " ")}{reset}')

def choose(menu, multiple=False, fancy_menu=None):
    if fancy_menu:
        if len(menu) != len(fancy_menu):
            raise Exception

    print_menu(fancy_menu or menu)
    
    while True:
        choice = ""
        try:
            choice = input(f'\033[31m{">>".ljust(80, " ")}\033[0m\r\033[3C')
        except KeyboardInterrupt:
            end()
            
        if choice == "":
            resetLine()
            continue
        
        if choice == "quit":
            end()

        if not multiple:
            choice_num = 0
            try:
                _num = int(choice)
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

def select_shuffle():
    yes = "shuffle songs"
    no = "don't shuffle songs"
    choice = choose([no, yes])
    if choice == yes:
        return True
    elif choice == no:
        return False

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

def play_songs(songs, shuffle):
    _songs = songs
    if shuffle:
        random.shuffle(_songs)
    
    for song in _songs:
        time = get_time(song)
        print(f'  {time} ' +song.split('\\')[-1][0:-4])
        
    for index, song in enumerate(_songs):
        num = len(_songs) - index
        up = '\033[A' * num
        down = '\n' * num
        print(f"{up}\r>{down}", end='')
        play_song(song)
        print(f"{up}\r {down}", end='')

uv_folder_path = 'C:\\Users\\Teo\\Documents\\UV'

def main():
    clear()
    folder = select_folder()
    clear()
    songs = select_songs(folder)
    clear()
    shuffle = len(songs) > 1 and select_shuffle()
    clear()
    play_songs(songs, shuffle)

if __name__ == "__main__":
    mixer.init()
    
    main()
    
    mixer.quit()