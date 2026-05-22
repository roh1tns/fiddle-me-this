import json
import pyglet


class SeekOutOfBoundsError(Exception):
    """Exception raised when the seek value exceeds the song length"""
    pass


class Song:
    """Class to load and play the song tracks."""
    
    def __init__(self, path: str):
        with open(f"{path}/info.json", 'r') as f:
            song_info = json.load(f)

        self.title: str = song_info["title"]
        self.artist = song_info["artist"]
        self.album = song_info["album"]
        self.year = song_info["year"]
        self.length_str: str = song_info["song_length"]
        l = self.length_str.split(":")
        self.length = int(l[0]) * 60 + int(l[1])
        self.tracks = {x: pyglet.media.load(
            song_info["tracks"][x], streaming=False) for x in song_info["tracks"]}
        self.players = {x: pyglet.media.Player() for x in self.tracks}
        self.playback_order = list(self.tracks.keys())
        self.current_track = 0

    def start_song(self):

        for (track, player) in self.players.items():
            player.queue(self.tracks[track])
            player.volume = 0.0
            player.loop = True
        self.players[self.playback_order[self.current_track]].volume = 1.0

        for (_, player) in self.players.items():
            player.play()

    def seek(self, timestamp: str):
        m, s = timestamp.split(":")
        ts = int(m) * 60 + int(s)
        if ts > self.length or ts < 0:
            raise SeekOutOfBoundsError
        for _, player in self.players.items():
            player.seek(ts)

    def next_track(self):
        self.current_track += 1
        self.players[self.playback_order[self.current_track]].volume = 1.0

    def evaluate_guess(self, guess: str):
        if guess.lower().strip() == self.title.lower().strip():
            return True
        return False
    
    def stop_song(self):
        for _, player in self.players.items():
            player.pause()
    
    def resume(self):
        for _, player in self.players.items():
            player.play()

    def get_current_track(self):
        return self.playback_order[self.current_track]
    
    def get_title(self):
        return self.title
    
    def get_starting_details(self):
        return f"""-------------------------------------
Release Year    :   {self.year}
Song Length     :   {self.length_str}
-------------------------------------
"""
    
    def __str__(self):
        return f"""----------Song Details----------
Title           :   {self.title}
Artist          :   {self.artist}
Album           :   {self.album}
Release Year    :   {self.year}
--------------------------------
"""
