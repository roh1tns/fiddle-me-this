from song import Song, SeekOutOfBoundsError
import random
import os
import threading
import pyglet

# Start pyglet event loop in a separate thread to enable looping
def start_pyglet_thread():
    pyglet.app.run()
    
pyglet_thread = threading.Thread(target=start_pyglet_thread, daemon=True)
pyglet_thread.start()
 
GREEN = '\033[92m'
RESET = '\033[0m'

available_commands = """
-----------------------Commands------------------
help - display the available commands
stop - stop the game
next - get the next track
seek mm:ss - seek to the timestamp mm:ss
guess <song name> - make a guess
surrender - give up the current song
pause - pause the song
resume - resume playback
-------------------------------------------------
"""

intro = f"""
    ███████╗██╗██████╗ ██████╗ ██╗     ███████╗    ███╗   ███╗███████╗    ████████╗██╗  ██╗██╗███████╗██╗
    ██╔════╝██║██╔══██╗██╔══██╗██║     ██╔════╝    ████╗ ████║██╔════╝    ╚══██╔══╝██║  ██║██║██╔════╝██║
    █████╗  ██║██║  ██║██║  ██║██║     █████╗      ██╔████╔██║█████╗         ██║   ███████║██║███████╗██║
    ██╔══╝  ██║██║  ██║██║  ██║██║     ██╔══╝      ██║╚██╔╝██║██╔══╝         ██║   ██╔══██║██║╚════██║╚═╝
    ██║     ██║██████╔╝██████╔╝███████╗███████╗    ██║ ╚═╝ ██║███████╗       ██║   ██║  ██║██║███████║██╗
    ╚═╝     ╚═╝╚═════╝ ╚═════╝ ╚══════╝╚══════╝    ╚═╝     ╚═╝╚══════╝       ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝
▂▃▄▅▆▇█▇▆▅▄▃▂ ▂▃▄▅▆▇█▇▆▅▄▃▂ ▂▃▄▅▆▇█▇▆▅▄▃▂ ▂▃▄▅▆▇█▇▆▅▄▃▂ ▂▃▄▅▆▇█▇▆▅▄▃▂ ▂▃▄▅▆▇█▇▆▅▄▃▂ ▂▃▄▅▆▇█▇▆▅▄▃▂ ▂▃▄▅▆▇█▇▆▅▄▃▂


-------------------------------------------How It Works---------------------------------------------------------
You will hear a song played, track by track, getting overlaid as you go, and you have to guess the song.
Each song will have at most 6 tracks - Bass, Drums, Guitar, Piano, Other and Vocals.
You will be given the release year and the length of the song in the beginning.
The song starts playing with just the bass track. If you are unable to guess the song, you can enter the
command 'next' to get the drums overlaid on top of the bass, and so on, until you run out of tracks.
You can seek to any part of the song using the 'seek' command.
You can make a guess using the 'guess' command.
You can give up the current song with the command 'surrender', and the song title and other details will be shown.

You may not hear a track as soon as you activate it because it is not playing in the current section of the song.
You can use the 'seek' command to seek to a part where it is playing.
----------------------------------------------------------------------------------------------------------------

{available_commands}
"""

print(intro)
songs = os.listdir("songs")

# Main Game Loop
while songs:
    song = random.choice(songs)
    song = Song(f"songs/{song}")
    songs.remove(song.get_title())
    input("Press 'Enter' to start!")
    print(song.get_starting_details())
    song.start_song()
    print(f"""------------------------------------------------
Current track: {song.get_current_track()}
------------------------------------------------""")
    # Song & commands loop
    while True:
        command = input("Your command: ").split()
        if not command:
            continue

        if command[0] == "stop":
            song.stop_song()
            break

        elif command[0] == "help":
            print(available_commands)

        elif command[0] == "next":
            try:
                song.next_track()
                print(f"""------------------------------------------------
Current track: {song.get_current_track()}
------------------------------------------------""")
            except IndexError:
                print("-> Error: This song has no more tracks.")

        elif command[0] == "seek":
            try:
                song.seek(command[1])
                print("-> Seek Successful!")
            except (IndexError, ValueError):
                print("-> Error: Invalid input format, please try again!")
            except SeekOutOfBoundsError:
                print(
                    "-> Error: The timestamp you gave is outside the song length, please try again!")

        elif command[0] == "guess":
            if song.evaluate_guess(" ".join(command[1:])):
                
                print(GREEN + "\nYOU GOT IT! LESGOOOOOO🥳🥳\n")
                print(song)
                print(RESET)
                song.stop_song()
                break
            else:
                print("-> Your guess is wrong, please try again :(")

        elif command[0] == "pause":
            song.stop_song()

        elif command[0] == "resume":
            song.resume()

        elif command[0] == "surrender":
            print(song)
            song.stop_song()
            break
        else:
            print("-> Error: Unrecognized command!")
    if songs:
        print("\n--------------------------------------------------------------------------------------------------------------\n")
        try_another = input(
            "Do you wish to try another song? (y/n):").strip().lower()
        if try_another == "y":
            continue
        else:
            break
