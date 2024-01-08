from math import floor
import random
import time
import os
import sys
import json
from pygame import mixer
from mutagen.mp3 import MP3
import cursor

width = 120
uv_folder_path = 'C:\\Users\\Teo\\Documents\\UV'
playlists_path = 'C:\\Users\\Teo\\Desktop\\hac\\piton-stuf\\py-uv\\playlists.json'

class InvalidChoice(Exception):
    pass

class Home(Exception):
    pass

class RaiseInvalidChoice():
    def __enter__(self):
        pass
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type == ValueError:
            raise InvalidChoice()
        return False

class PromptPath:
    
    def __init__(self):
        self.prompts = []
        
    def add_prompt(self, prompt):
        self.prompts.append(prompt)
    
    def add_answer(self, answer):
        self.prompts[-1] += f' ({answer})'
    
    def reset_path(self):
        self.prompts = []
    
    def get_prompt_path(self):
        path = ''
        for i, prompt in enumerate(self.prompts):
            path += prompt
            if i != len(self.prompts) - 1:
                path += ' > '
        return path

promptPath = PromptPath()

# PLAYLISTS

def load_playlists(path):
    data = None
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def write_playlists(path, playlists):
    with open(path, 'w') as f:
        json.dump(playlists, f, indent=4)

def select_playlist(prompt=None):
    playlists = load_playlists(playlists_path)
    if len(playlists) == 0:
        _ = choose_free('no playlists', 'No playlists created.')
        raise Home()
    playlist_name = choose(prompt or "select playlist", list(playlists.keys()), add_answer=True)
    clear()
    playlist = playlists[playlist_name]
    return playlist, playlist_name

def new_playlist():
    name = choose_free('playlist name', 'Enter new playlist name:')
    clear()
    playlist = []
    songs = select_folder_and_songs()
    for song in songs:
        playlist.append(song)
    playlists = load_playlists(playlists_path)
    playlists[name] = playlist
    write_playlists(playlists_path, playlists)
    
def delete_playlist():
    playlists = load_playlists(playlists_path)
    _, name = select_playlist('delete playlist')
    del playlists[name]
    write_playlists(playlists_path, playlists)

def add_songs_to_playlists():
    playlist, name = select_playlist('add songs to playlist')
    songs = select_folder_and_songs()
    for song in songs:
        playlist.append(song)
    playlists = load_playlists(playlists_path)
    playlists[name] = playlist
    write_playlists(playlists_path, playlists)

def remove_songs_from_playlists():
    playlist, name = select_playlist('remove songs from playlist')
    _playlist = [song.split('\\')[-1][0:-4] for song in playlist]
    songs = choose("remove songs", playlist, multiple=True, fancy_menu=_playlist)
    clear()
    for song in songs:
        playlist.remove(song)
    playlists = load_playlists(playlists_path)
    playlists[name] = playlist
    write_playlists(playlists_path, playlists)

def play_playlist():
    playlist, _ = select_playlist('play playlist')
    clear()
    shuffle = len(playlist) > 1 and select_shuffle()
    clear()
    play_songs(playlist, shuffle)
    clear()

# SYSTEM STUFF

def home():
    promptPath.reset_path()
    raise Home()

def end():
    clear()
    print('\033[0m', end='')
    cursor.show()
    mixer.quit()
    sys.exit()
        
def clear():
    os.system('cls')

# CHOOSE

def print_prompt():
    print(f'\033[31;3;48;5;233m{promptPath.get_prompt_path().ljust(width, " ")}\033[0m')

def choose_free(prompt, prompt_fancy=None):
    
    promptPath.add_prompt(prompt)
    print_prompt()
    print(f'\033[37;48;5;235m{(prompt_fancy or prompt).ljust(width, " ")}')
    print(f'\033[31;48;5;233m{">>".ljust(width, " ")}\r\033[3C', end='')
    
    try:
        user = input()
    except KeyboardInterrupt:
        home()
    
    if user == 'home':
        home()
    
    if user == 'quit':
        end()
    
    promptPath.add_answer(user)
        
    return user

def resetLine():
    print(f"\033[A\r{' '*80}\r", end='')

def print_menu(menu):
    index_width = 5
    white_foreground = '\033[37m'
    is_even = lambda x: x % 2 == 0
    even_off = '\033[48;5;235;3m'
    odd_off = '\033[48;5;240;3m'
    reset_dim = '\033[23m'
    even = '\033[48;5;235m'
    odd = '\033[48;5;240m'
    reset = '\033[0m'
    for index, item in enumerate(menu):
        print(f'{white_foreground}{even_off if is_even(index) else odd_off}{str(index).ljust(index_width, " ")}{reset_dim}{even if is_even(index) else odd}{item.ljust(width - index_width, " ")}{reset}')

def choose_one(menu, choice):
    num = 0
    
    with RaiseInvalidChoice(): num = int(choice)
    
    if (num < 0 or num >= len(menu)):
        raise InvalidChoice()
    
    choice_item = menu[num]
    return choice_item

def expand_range(choice):
    bounds = choice.split('-')
    
    if len(bounds) != 2:
        raise InvalidChoice()
    
    _start = int(bounds[0])
    _end = int(bounds[1])
    swapped = False
    
    if _start > _end:
        swapped = True
        _temp = _start
        _start = _end
        _end = _temp
    
    nums = range(_start, _end+1, 1)
    if swapped:
        nums = reversed(nums)
    
    return nums

def expand_ranges(choices):
    _choices = []
    for choice in choices:
        if '-' in choice:            
            expanded_range = expand_range(choice)
            for num in expanded_range:
                _choices.append(num)
        else:
            _choices.append(choice)
    return _choices

def choose_multiple(menu, choice):
    choices = choice.split()
    choices_num = []
    
    choices = expand_ranges(choices)
    for num in choices:
        with RaiseInvalidChoice(): _num = int(num)
        
        if (_num < 0 or _num >= len(menu)):
            raise InvalidChoice()
        choices_num.append(_num)
    
    choice_items = [menu[num] for num in choices_num]
    return choice_items

def choose_loop(menu, multiple):
    choice = ""
    try:
        choice = input(f'\033[31;48;5;233m{">>".ljust(width, " ")}\r\033[3C')
    except KeyboardInterrupt:
        home()
        
    if choice == "":
        raise InvalidChoice()
    
    if choice == 'home':
        home()
    
    if choice == "quit":
        end()
        
    result = None

    if not multiple:
        result = choose_one(menu, choice)
    else:
        result = choose_multiple(menu, choice)
    
    return result

def choose(prompt, menu, multiple=False, fancy_menu=None, add_answer=False):
    if fancy_menu and len(menu) != len(fancy_menu):
        raise Exception

    promptPath.add_prompt(prompt)
    print_prompt()
    print_menu(fancy_menu or menu)
    
    while True:
        try:
            choice = choose_loop(menu, multiple)
            if add_answer:
                promptPath.add_answer(choice)
            return choice
        except InvalidChoice:
            resetLine()
            continue

# SONG PLAYING

def spinner_gen():
    while True:
        yield('⠙')
        yield('⠸')
        yield('⠴')
        yield('⠦')
        yield('⠇')
        yield('⠋')

def format_time(duration):
    seconds = duration % 60
    minutes = floor(duration / 60) % 60
    hours = floor(duration / 3600)
    
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

def get_duration(song):
    return int(MP3(song).info.length)

def get_playing_str(song):
    song_name = song.split("\\")[-1][0:-4]
    return f'{format_time(get_duration(song)).ljust(10, " ")}{song_name}'

def play_song(song, height, remaining_time):
    mixer.music.load(song)
    mixer.music.play()
    
    elapsed_time = 0
    up = '\033[A' * height
    down = '\n' * height
    
    while mixer.music.get_busy():
        try:
            elapsed_time_str = format_time(elapsed_time)
            remaining_time_str = format_time(remaining_time - elapsed_time)
            print(f'{up}\r\033[37;41m\033[{width - len(elapsed_time_str)}C{elapsed_time_str}\r{down}\033[0m\r\033[31;48;5;233m{remaining_time_str.ljust(width, " ")}\033[0m\r', end='')

            cursor.hide()
            time.sleep(1)
            elapsed_time += 1
        except KeyboardInterrupt:
            mixer.music.stop()
            cursor.show()
            home()
            
    last_song_in_queue = height == 1
    if last_song_in_queue:
        end()

def play_songs(songs, shuffle):    
    _songs = songs
    if shuffle:
        random.shuffle(_songs)
    
    white = '\033[37m'
    after = '\033[48;5;235;2m'
    current = '\033[41m'
    before = '\033[48;5;240m'
    
    for song in _songs:
        print(f'{white}{before}{get_playing_str(song).ljust(width, " ")}')
        
    for index, song in enumerate(_songs):
        
        height = len(_songs) - index
        up = '\033[A' * height
        down = '\n' * height
        print(f'\r{white}{up}{current}{get_playing_str(song).ljust(width, " ")}{down}\r\033[0m', end='')
        
        remaining_time = 0
        for i in range(index, len(_songs)):
            remaining_time += get_duration(_songs[i])
            
        play_song(song, height, remaining_time)
        
        print(f'\r{white}{up}{after}{get_playing_str(song).ljust(width, " ")}\033[22m{down}\r', end='')

# PROGRAM FLOW

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
    folder = choose("select folder", folder, fancy_menu=_folders, add_answer=False)
    return folder

def select_songs(folder):
    songs = get_files(folder)
    _songs = [song.split('\\')[-1][0:-4] for song in songs]
    vibes = choose("select songs", songs, multiple=True, fancy_menu=_songs, add_answer=False)
    return vibes

def select_folder_and_songs():
    folder = select_folder()
    clear()
    songs = select_songs(folder)
    clear()
    return songs

def select_shuffle():
    yes = "shuffle songs"
    no = "don't shuffle songs"
    choice = choose("select shuffle", [no, yes])
    if choice == yes:
        return True
    elif choice == no:
        return False
    
def play_uv_songs():
    songs = select_folder_and_songs()
    shuffle = len(songs) > 1 and select_shuffle()
    clear()
    play_songs(songs, shuffle)
    clear()

def edit_playlists():
    choice_new_playlist = 'new playlist'
    choice_delete_playlist = 'delete playlist'
    choice_add_songs_to_playlist = 'add songs to playlist'
    choice_remove_songs_from_playlist = 'remove songs from playlist'
    choice = choose("edit playlists", [
        choice_new_playlist,
        choice_delete_playlist,
        choice_add_songs_to_playlist,
        choice_remove_songs_from_playlist
    ])
    clear()
    if choice == choice_new_playlist:
        new_playlist()
    elif choice == choice_delete_playlist:
        delete_playlist()
    elif choice == choice_add_songs_to_playlist:
        add_songs_to_playlists()
    elif choice == choice_remove_songs_from_playlist:
        remove_songs_from_playlists()

def start_menu():
    clear()
    choice_play_songs = 'play uv songs'
    choice_play_playlist = 'play playlist'
    choice_edit_playlists = 'edit playlists'
    choice = choose("start menu", [choice_play_songs, choice_play_playlist, choice_edit_playlists])
    clear()
    if choice == choice_play_songs:
        play_uv_songs()
    elif choice == choice_play_playlist:
        play_playlist()
    elif choice == choice_edit_playlists:
        edit_playlists()

def main():
    os.system('title uv')
    mixer.init()
    
    clear()
    while True:
        promptPath.reset_path()
        try:
            start_menu()
        except Home:
            continue
    clear()
    
    mixer.quit()

if __name__ == "__main__":
    main()