import pygame
import settings

class Player():
    def __init__(self, number):
        self.card_array = []
        self.number = number
        if number == 1:     # 玩家1
            self.image = pygame.image.load("images/player1.png")
        if number == 2:
            self.image = pygame.image.load("images/player2.png")
        if number == 3:
            pass
        self.rect = self.image.get_rect()
        self.font = pygame.font.Font('images/MIAO.TTF', 30)

    def update(self, turn, screen, settings):
        if turn == self.number:   # 如果是当前玩家的回合
            self.rect.x, self.rect.y = int(settings.screen_width * 0.01), int(settings.screen_height * 0.5)
            screen.blit(self.image, self.rect)
            card_x, card_y = settings.screen_width * 0.01, settings.screen_height * 0.8

            text = "当前玩家回合"
            text_render = self.font.render(text, True, (255, 255, 255))
            text_rect = text_render.get_rect()
            screen.blit(text_render, (self.rect.centerx, self.rect.centery+text_rect.bottom))

            for card in self.card_array:
                card.rect[0], card.rect[1] = card_x, card_y
                screen.blit(card.image, card.rect)
                card_x += card.rect.width - settings.hand_card_distance
        else:
            self.rect.x, self.rect.y = settings.screen_width * 0.01, settings.screen_height * 0.2
            screen.blit(self.image, self.rect)
            card_x, card_y = settings.screen_width * 0.01, settings.screen_height * 0.01
            for card in self.card_array:
                #以下两行二选一
                #看不到对手牌
                # screen.blit(card.card_back_image, (card_x, card_y))
                #看得到对手牌
                screen.blit(card.image, (card_x, card_y))
                card_x += card.rect.width - settings.hand_card_distance

    def receive_card(self, turn, cards):
        if turn == self.number:  # 如果是当前玩家的回合
            for card in cards:
                self.card_array.append(card)
                print(card.size, card.kind)
            # sorted(self.card_array,key = lambda x: x.kind )
    def win(self, screen, settings):
        winbg_image = pygame.image.load("images/winbg.png")
        winbg_image_rect = winbg_image.get_rect()
        winbg_image_rect.centerx = settings.screen_width / 2
        winbg_image_rect.centery = settings.screen_height / 2
        win_image = pygame.image.load("images/win.png")
        win_image_rect = win_image.get_rect()
        self.rect = self.image.get_rect()
        self.rect.centerx = settings.screen_width/2
        self.rect.centery = settings.screen_height/2
        screen.blit(winbg_image, winbg_image_rect)
        screen.blit(self.image, self.rect)
        win_image_rect.centerx, win_image_rect.centery = self.rect.centerx, win_image_rect.bottom
        screen.blit(win_image, win_image_rect)
        pygame.display.update()

        win_sound = pygame.mixer.Sound("images/win.wav")
        win_sound.play()