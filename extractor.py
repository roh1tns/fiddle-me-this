import os
import sys
import json
import pyglet
from audio_separator.separator import Separator

input_file = sys.argv[1]

print("--- Please enter the song details for info.json ---")
title = input("Title: ")
artist = input("Artist: ")
album = input("Album: ")
while True:
    year_input = input("Release Year: ")
    try:
        year = int(year_input)
        break
    except ValueError:
        print("Please enter a valid integer for the year.")

output_folder = os.path.join("songs", title)

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

try:
    source_full = pyglet.media.load(input_file)
    duration = source_full.duration
    song_length = f"{int(duration // 60):02d}:{int(duration % 60):02d}"
except Exception as e:
    print(f"Warning: Could not infer song length automatically. Defaulting to 00:00. ({e})")
    song_length = "00:00"

separator = Separator(output_dir=output_folder)
separator.load_model('htdemucs_6s.yaml')

custom_names = {
    "Bass": "bass",
    "Drums": "drums",
    "Guitar": "guitar",
    "Piano": "piano",
    "Other": "other",
    "Vocals": "vocal"
}

output_files = separator.separate(input_file, custom_output_names=custom_names)

print(f"\nSeparation complete! Files saved in: {output_folder}")

included_tracks = {}

print("\n--- Audition Tracks ---")
print("You will now hear each extracted track.")
print("Commands during playback:")
print("  seek mm:ss  - Jump to a specific timestamp")
print("  stop        - Stop listening to the current track (or just press Enter)")

for file in output_files:
    track_name = os.path.splitext(file)[0]
    filepath = os.path.join(output_folder, file)

    print(f"\nPlaying '{track_name}'...")
    player = pyglet.media.Player()
    try:
        source = pyglet.media.load(filepath)
        player.queue(source)
        player.play()

        while True:
            cmd = input(
                f"[{track_name}] Command (seek/stop/Enter): ").strip().lower()
            if cmd == "" or cmd == "stop":
                break
            elif cmd.startswith("seek "):
                ts_str = cmd.split(" ", 1)[1].strip()
                try:
                    m, s = ts_str.split(":")
                    ts_seconds = int(m) * 60 + int(s)
                    if 0 <= ts_seconds <= source.duration:
                        player.seek(ts_seconds)
                    else:
                        print(f"-> Error: The timestamp you gave is outside the song length, please try again!")
                except ValueError:
                    print(" -> Error: Invalid format. Use 'mm:ss' or seconds (e.g. 'seek 01:15' or 'seek 75').")
            else:
                print("-> Unknown command. Press Enter to stop or type 'seek mm:ss' to jump.")

    except Exception as e:
        print(f"Could not play {file}: {e}")
    finally:
        player.pause()
        try:
            player.delete()
        except AttributeError:
            pass

    while True:
        include = input(
            f"Does the '{track_name}' track have audio? Include it? (y/n): ").strip().lower()
        if include in ['y', 'n']:
            break
        print("Please enter 'y' or 'n'.")

    if include == 'y':
        included_tracks[track_name] = filepath.replace("\\", "/")

ordered_tracks = {}

if not included_tracks:
    print("\nNo tracks were included. Creating empty tracklist.")
else:
    print("\n--- Playback Order ---")
    print(f"Included tracks: {', '.join(included_tracks.keys())}")
    while True:
        order_input = input(
            "Enter the tracks in your desired playback order, separated by commas: ")
        order_list = [t.strip() for t in order_input.split(',')]
        order_list = [t for t in order_list if t]

        if sorted(order_list) == sorted(included_tracks.keys()):
            for t in order_list:
                ordered_tracks[t] = included_tracks[t]
            break
        else:
            print(
                "-> Error: The tracks you entered do not match the included tracks. Please try again.")


info_dict = {
    "title": title,
    "artist": artist,
    "album": album,
    "year": year,
    "song_length": song_length,
    "tracks": ordered_tracks
}

info_path = os.path.join(output_folder, "info.json")
with open(info_path, "w", encoding="utf-8") as f:
    json.dump(info_dict, f, indent=2)

print(f"\nSuccessfully populated and saved '{info_path}'!")
