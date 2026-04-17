import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        self.music_folder = music_folder
        self.tracks = [f for f in os.listdir(music_folder) if f.endswith(('.mp3', '.wav'))]
        self.current_track_index = 0
        self.is_paused = False

    def play(self):
        if not self.tracks: return
        track_path = os.path.join(self.music_folder, self.tracks[self.current_track_index])
        pygame.mixer.music.load(track_path)
        pygame.mixer.music.play()
        self.is_paused = False

    def pause_unpause(self):
        if self.is_paused:
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            pygame.mixer.music.pause()
            self.is_paused = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_paused = False

    def next_track(self):
        if not self.tracks: return
        self.current_track_index = (self.current_track_index + 1) % len(self.tracks)
        self.play()

    def prev_track(self):
        if not self.tracks: return
        self.current_track_index = (self.current_track_index - 1) % len(self.tracks)
        self.play()

    def get_current_track_name(self):
        if not self.tracks: return "No tracks found"
        if pygame.mixer.music.get_busy() or self.is_paused:
            return os.path.splitext(self.tracks[self.current_track_index])[0]
        return "Music Stopped"