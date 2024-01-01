from pygame import mixer
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
            continue

        if not multiple:
            choice_num = 0
            try:
                _num= int(choice)
                if (_num < 0 or _num >= len(menu)):
                    raise Exception
                choice_num = int(choice)
            except:
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

def play_songs(songs):
    for song in songs:
        play_mp3(song)

uv_folder_path = 'C:\\Users\\Teo\\Documents\\UV'

if __name__ == "__main__":
    mixer.init()
    
    folder = select_folder()
    songs = select_songs(folder)
    print(songs)
    play_songs(songs)
    
    mixer.quit()