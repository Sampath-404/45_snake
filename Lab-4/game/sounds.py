import array
import math
import pygame


class SoundManager:
    """Makes simple beep sounds in code (no audio files needed).

    If audio can't start on this computer, the game still runs silently.
    """

    def __init__(self):
        self.eat_sound = None
        self.game_over_sound = None
        try:
            pygame.mixer.quit()
            pygame.mixer.init(frequency=44100, size=-16, channels=1)
            self.eat_sound = self._make_sound([(880, 0.08), (1175, 0.08)])
            self.game_over_sound = self._make_sound([(440, 0.2), (330, 0.2), (220, 0.4)])
        except Exception:
            # No audio device or unsupported format: play without sound.
            self.eat_sound = None
            self.game_over_sound = None

    def _make_sound(self, notes):
        sample_rate, _, channels = pygame.mixer.get_init()
        volume = 0.3
        samples = array.array("h")
        for frequency, duration in notes:
            total = int(sample_rate * duration)
            for i in range(total):
                fade = 1.0 - i / total  # fade out so notes don't click
                value = int(32767 * volume * fade *
                            math.sin(2 * math.pi * frequency * i / sample_rate))
                for _ in range(channels):
                    samples.append(value)
        return pygame.mixer.Sound(buffer=samples.tobytes())

    def play_eat(self):
        if self.eat_sound:
            self.eat_sound.play()

    def play_game_over(self):
        if self.game_over_sound:
            self.game_over_sound.play()