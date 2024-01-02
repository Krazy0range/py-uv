from math import floor
import random
import time
import os
import sys
from pygame import mixer
from mutagen.mp3 import MP3
import cursor

width = 120

def end():
    clear()
    # print('\033[?25h')
    cursor.show()
    mixer.quit()
    sys.exit()
        
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

class InvalidChoice(Exception):
    pass

class RaiseInvalidChoice():
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type == ValueError:
            raise InvalidChoice()
        return False

def choose_one(menu, choice):
    num = 0
    
    with RaiseInvalidChoice(): num = int(choice)
    
    if (num < 0 or num >= len(menu)):
        raise InvalidChoice()
    
    choice_item = menu[num]
    return choice_item

def expand_ranges(choices):
    _choices = choices.copy()
    for index, choice in enumerate(_choices):
        if '-' in choice:
            bounds = choice.split('-')

            if len(bounds) != 2:
                raise InvalidChoice()

            del choices[index]
            
            _start = int(bounds[0])
            _end = int(bounds[1])
            swapped = False
            
            if _start > _end:
                swapped = True
                _temp = _start
                _start = _end
                _end = _temp
            
            nums = range(_start, _end+1, 1)
            if not swapped:
                nums = reversed(nums)
                
            for n in nums:
                choices.insert(index, n)

def choose_multiple(menu, choice):
    choices = choice.split()
    choices_num = []
    
    expand_ranges(choices)
    for num in choices:
        with RaiseInvalidChoice(): _num = int(num)
        
        if (_num < 0 or _num >= len(menu)):
            raise InvalidChoice()
        choices_num.append(_num)
    
    choice_items = [menu[num] for num in choices_num]
    return choice_items

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
            
        result = None

        try:
            if not multiple:
                result = choose_one(menu, choice)
            else:
                result = choose_multiple(menu, choice)
        except InvalidChoice:
            resetLine()
            continue
        else:
            return result

def get_subfolders(directory):
    subfolders = [f.path for f in os.scandir(directory) if f.is_dir()]
    return subfolders

def get_files(directory):
    files = [f.path for f in os.scandir(directory) if f.is_file()]
    
    if directory + '\\desktop.ini' in files:
        files.remove(directory + '\\desktop.ini')
        
    return files

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

def spinner_gen():
    while True:
        yield('⠙')
        yield('⠸')
        yield('⠴')
        yield('⠦')
        yield('⠇')
        yield('⠋')

def play_song(song, height):
    mixer.music.load(song)
    mixer.music.play()
    
    elapsed_time = 0
    up = '\033[A' * height
    down = '\n' * height
    
    spinner = spinner_gen()
    
    while mixer.music.get_busy():
        try:
            t = format_time(elapsed_time)
            print(f'{up}\r\033[41m\033[{width - len(t)}C{t}{down}\033[0m\r', end='')
            cursor.hide()

            time.sleep(1)
            elapsed_time += 1
        except KeyboardInterrupt:
            end()
            
    last_song_in_queue = height == 1
    if last_song_in_queue:
        end()
            
def format_time(duration):
    seconds = duration % 60
    minutes = floor(duration / 60) % 60
    hours = floor(minutes / 60)
    
    seconds_str = str(seconds).rjust(2, '0')
    
    if hours > 0:
        minutes_str = str(minutes).rjust(2, '0')
    else:
        minutes_str = str(minutes)
        
    hours_str = str(hours)
    
    time = ""
    
    if hours > 0:
        time = f'{hours_str}:{minutes_str}:{seconds_str}'
    else:
        time = f'{minutes_str}:{seconds_str}'
    
    return time

def get_playing_str(song):
    return f'{format_time(int(MP3(song).info.length)).ljust(7, " ")} ' +song.split('\\')[-1][0:-4]

def play_songs(songs, shuffle):    
    _songs = songs
    if shuffle:
        random.shuffle(_songs)
    
    after = '\033[48;5;235;2m'
    current = '\033[41m'
    before = '\033[48;5;240m'
    
    
    for song in _songs:
        print(f'{before}{get_playing_str(song).ljust(width, " ")}')
        
    for index, song in enumerate(_songs):
        
        height = len(_songs) - index
        up = '\033[A' * height
        down = '\n' * height
        print(f'\r{up}{current}{get_playing_str(song).ljust(width, " ")}{down}\r\033[0m', end='')
        
        play_song(song, height)
        
        print(f'\r{up}{after}{get_playing_str(song).ljust(width, " ")}\033[22m{down}\r', end='')

uv_folder_path = 'C:\\Users\\Teo\\Documents\\UV'

def main():
    os.system('title uv')
    mixer.init()
    
    clear()
    folder = select_folder()
    clear()
    songs = select_songs(folder)
    clear()
    shuffle = len(songs) > 1 and select_shuffle()
    clear()
    play_songs(songs, shuffle)
    clear()
    
    mixer.quit()

if __name__ == "__main__":
    main()