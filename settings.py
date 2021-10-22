from pygame import display


class Settings:
    def __init__(self):
        self.screen_width = 1800
        self.screen_height = 900

        display.set_caption("PiG TAiL--")
        self.fps = 90
        self.hand_card_distance = 70