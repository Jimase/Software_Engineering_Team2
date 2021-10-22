# -*- coding: utf-8 -*-
# @Time : 2021/10/8 10:42
# @Author : Hao
# @File : GamePVP.py
import time
import numpy as np
import random
from math import atan2, degrees
from Player import Player
import requests
import json
import sys
import pygame
# 创建游戏,接受唯一标识创建游戏者的token参数,返回该游戏的标识uuid，并跳出把uuid分享给你的好朋友吧
bg = pygame.image.load("images/bg3.png")
click_effect = pygame.image.load("cards_images/click.png")
click_effect_rect = click_effect.get_rect()
r = 330
def Create_Game(token, isprivate):  # isprivate表示该游戏是否隐私 Ture/False
    jsonT = {'private': isprivate}
    header = {'Authorization': token, 'Content-Type': 'application/json'}
    r = requests.post('http://172.17.173.97:9000/api/game', headers=header, json=jsonT)
    print("Create_Game_response:", r.text)
    user_dict = json.loads(r.text)
    uuid = user_dict['data']['uuid']
    print("success create game,uuid:", uuid)
    return user_dict
def Join_Game(token, uuid):
    header = {'Authorization': token, 'Content-Type': 'application/json'}
    r = requests.post(url='http://172.17.173.97:9000/api/game/' + uuid, headers=header)
    user_dict = json.loads(r.text)
    print(user_dict)
    return user_dict
def Query_Game(token, page_size, page_num):
    headers = {'Authorization': token}
    params = {"page_size": str(page_size), "page_num": str(page_num)}
    r = requests.get(url='http://172.17.173.97:9000/api/game/index', headers=headers, params=params)
    print(r.text)
    user_dict = json.loads(r.text)
    print(user_dict)
    return user_dict
def Get_last(token, uuid):
    '''
    :param token:
    :param uuid:
    :return:
    对局未开始返回报文：
    {
    “code”: 200,
    “data”: {
    “last_code”: “”,
    “last_msg”: “对局刚开始”,
    “your_turn”: true
    },
    “msg”: “操作成功”
    }
    人没齐返回报文：
    {
    “code”: 403,
    “data”: {
    “err_msg”: “人还没齐”
    },
    “msg”: “非法操作”
    }
    '''
    import requests
    import json
    url = 'http://172.17.173.97:9000/api/game/' + uuid + '/last'
    header = {'Authorization': token, 'Content-Type': 'application/json'}
    r = requests.get(url, headers=header)
    user_dict = json.loads(r.text)
    print(user_dict)
    return user_dict
def Do_card(token, uuid, type,str_card=''):
    '''
    :param token:
    :param uuid:
    :param type:
    :param str_card:
    :return: 操作返回的信息
    请求参数示例:
    {
    "type": 0
    }
    或
    {
      "type": 1,
      "card": "SQ"
    }
    '''
    import requests
    import json
    url = 'http://172.17.173.97:9000/api/game/' + uuid
    header = {'Authorization': token, 'Content-Type': "application/json"}
    param = {
        'type':int(type),
        'card':str_card
    }
    payload = json.dumps(param)
    r = requests.put(url, headers=header,data = payload)
    user_dict = json.loads(r.text)
    print(user_dict)
    return user_dict
    # {
    #     "code": 200,
    #     "data": {
    #         "last_code": "1 0 D10",
    #         "last_msg": "2P 从<牌库>翻开了一张 D10"
    #     },
    #     "msg": "操作成功"
    # }
def in_rect(pos, rect):
    """
    鼠标 是否在目标区域内 \n
    :param pos: 鼠标光标位置
    :param rect: 所要判断点击的区域框
    :return: 鼠标是否在区域内
    """
    x, y = pos
    rx, ry, rw, rh = rect
    if (rx <= x <= rx + rw) and (ry <= y <= ry + rh):
        return True
    return False
class Card:
    '''
    ·········接口端： ======本地端：
    ♠ spade（黑桃，又名葵扇）        黑桃:S ==== 2
    ♥ heart（红心，又名红桃）        红桃:H ==== 3
    ♣ club（梅花，又名草花）         梅花:C ==== 1
    ♦ diamond（方块，又名阶砖）      方块:D ==== 0
    '''

    def __init__(self, settings):
        # 表示卡牌均未知
        self.size, self.kind = (0, 0)
        self.msg = ''
        self.image = pygame.image.load("cards_images/" + str(self.size) + "_" + str(self.kind) + ".png")
        self.card_back_image = pygame.image.load("cards_images/back.png")
        self.rect = self.image.get_rect()
        self.rect.right = settings.screen_width * 0.9
        self.rect.top = settings.screen_height

        self.rect_canterx = self.rect.centerx
        self.rect_cantery = self.rect.centery
        self.rate = 0  # 最终rate
        self.current_rate = 0
        self.new_rect = self.rect  # 旋转之后的rect
        # print(self.size,self.kind)

    def set_by_msg(self, re_msg):
        # print("last_msg:",re_msg['data']['last_msg'])
        msg_list = (re_msg['data']['last_code'])
        # print("msg_list:",msg_list)
        # self.msg = msg_list[4:]
        # 设置大小
        if msg_list[5:] == '10':
            self.size = 10 - 1
        elif msg_list[5] == 'J':
            self.size = 11 - 1
        elif msg_list[5] == 'Q':
            self.size = 12 - 1
        elif msg_list[5] == 'K':
            self.size = 13 - 1
        else:
            self.size = int(msg_list[5:]) - 1
        # 设置花色
        if msg_list[4] == 'D':
            self.kind = 0
        elif msg_list[4] == 'C':
            self.kind = 1
        elif msg_list[4] == 'H':
            self.kind = 3
        else:  # msg_list[4] == 'S'
            self.kind = 2

        self.image = pygame.image.load("cards_images/" + str(self.size) + "_" + str(self.kind) + ".png")
        self.msg = msg_list[4:]

    def get_msg(self):
        print(self.msg)
        return self.msg
    # @staticmethod
    # def random_a_card(self, cards):
    #     size = np.random.randint(cards.shape[0])  # 从13张牌中挑一个
    #     kind = np.argmax(cards[size])  # 看此大小的牌 其四种类型是否还有，若没有再挑一张牌
    #     while cards[size][kind] == 0:
    #         cards = np.delete(cards, size, 0)  # 删除A的第二行
    #         size = np.random.randint(cards.shape[0])  # 从13张牌中挑一个
    #         kind = np.argmax(cards[size])
    #     cards[size][kind] = 0
    #     return size, kind
def cards_init(cards_array, settings):
    # 扑克牌就只有54张，从A、2~Q、K各4张，无大王、小王
    cards = np.ones((13, 4), dtype=int)  # 初始化 矩阵，全部取值为1

    for i in range(cards.shape[0] * cards.shape[1]):
        cards_array.append(Card(settings))
def show_cards(screen, cards_array, settings):
    """
    开始动画 \n
    修改 cards_array 中 card 坐标 \n
    :return:
    """
    card_box = [settings.screen_height * 0.1, settings.screen_height * 0.8]  # 上顶，下底
    card_card_distance = 12  # 牌与牌间距
    move_over = False
    while not move_over:
        # screen.fill((0, 0, 0))
        screen.blit(bg, (0, 0))
        for i in range(len(cards_array)):
            if i == 0:
                if cards_array[i].rect.y > card_box[0]:
                    cards_array[i].rect.y -= card_card_distance
                else:
                    move_over = True
            else:
                # 如果不是第一张牌，且y坐标大于前一张 且 y 坐标 大于
                if cards_array[i].rect.y >= cards_array[i - 1].rect.y + 2 * card_card_distance:
                    cards_array[i].rect.y -= card_card_distance
            screen.blit(cards_array[i].card_back_image, cards_array[i].rect)
        pygame.display.update()
        pygame.time.wait(5)
def show_insert(screen, settings, temp, cards_in_show, cards_array, player1, player2, turn):
    """
    显示插入动画， 调整新卡牌的坐标和角度， 并放入 围成圈的卡牌 中\n
    :param screen: 屏幕
    :param settings: 窗口设置
    :param temp: 临时卡牌存储
    :param cards_in_show: 围成圈的卡牌
    :param cards_array: 一开始存放着全部的卡牌
    :return: 无返回值
    """
    current_rate = 315
    change_rate = -36

    translation = True  # 先平移
    while translation:
        if temp[0].rect.x > settings.screen_width * 0.7:
            # screen.fill((0, 0, 0))
            screen.blit(bg, (0, 0))
            for card in cards_array:
                screen.blit(card.card_back_image, card.rect)
            for card in temp:
                card.rect.x -= 10
                screen.blit(card.card_back_image, card.rect)
            player1.update(turn, screen, settings)
            player2.update(turn, screen, settings)
            pygame.display.update()
        else:
            translation = False
    # 确定最终位置
    next_card_rate = (current_rate) % 360
    for card in cards_in_show:
        # 当前角度，对应圆的坐标， 作为card的最近路径点
        y = card.rect.centery - settings.screen_height / 2  # 获取 Y
        x = card.rect.centerx - settings.screen_width / 2  # 获取 X
        angle = atan2(y, x)  # 求反正切值
        card.current_rate = int(degrees(angle) % 360)  # 转换成角度
        card.rect_centerx = np.cos((360 - card.current_rate) * np.pi / 180) * r + settings.screen_width / 2
        card.rect_centery = np.sin((360 - card.current_rate) * np.pi / 180) * r + settings.screen_height / 2
        # 最终要旋转的角度
        card.rate = int(next_card_rate)
        next_card_rate += change_rate

    # 确定最终位置
    next_card_rate = (current_rate + change_rate * len(cards_in_show)) % 360
    for card in temp:
        # 当前角度，对应圆的坐标， 作为card的最近路径点
        y = card.rect.centery - settings.screen_height / 2  # 获取 Y
        x = card.rect.centerx - settings.screen_width / 2  # 获取 X
        angle = atan2(y, x)  # 求反正切值
        card.current_rate = int(degrees(angle) % 360)  # 转换成角度
        card.rect_centerx = np.cos((360 - card.current_rate) * np.pi / 180) * r + settings.screen_width / 2
        card.rect_centery = np.sin((360 - card.current_rate) * np.pi / 180) * r + settings.screen_height / 2
        # 最终要旋转的角度
        card.rate = int(next_card_rate)
        cards_in_show.append(card)
        next_card_rate += change_rate
    del temp


def speed(center1, biger, center2):
    max_speed = 6
    if biger:
        if center1 - center2 > 10:
            return int((center1 / center2) * max_speed)
        else:
            return int((center1 / center2) * 1)
    else:
        if center2 - center1 > 10:
            return int((center2 / center1) * max_speed)
        else:
            return int((center2 / center1) * 1)

def position_correct(cards_in_show, settings, screen):  # 针对cards_in_show矫正位置
    """
    卡牌到处飘的动画，调整坐标
    :param cards_in_show: 围成圈的卡牌
    :param settings: 窗口设置
    :param screen: 屏幕
    :return: 无返回值
    """
    for card in cards_in_show:
        if card.rect.centerx != card.rect_centerx:
            if card.rect.centerx > card.rect_centerx:
                card.rect.centerx -= speed(card.rect.centerx, 1, card.rect_centerx)
            else:
                card.rect.centerx += speed(card.rect.centerx, 0, card.rect_centerx)
        if card.rect.centery != card.rect_centery:
            if card.rect.centery > card.rect_centery:
                card.rect.centery -= speed(card.rect.centery, 1, card.rect_centery)
            else:
                card.rect.centery += speed(card.rect.centery, 0, card.rect_centery)
        if card.current_rate != card.rate:
            if card.current_rate > card.rate:
                card.current_rate -= 1
            else:
                card.current_rate += 1
            card.rect_centerx = int(np.cos((360 - card.current_rate) * np.pi / 180) * r + settings.screen_width / 2)
            card.rect_centery = int(np.sin((360 - card.current_rate) * np.pi / 180) * r + settings.screen_height / 2)
        new_card = pygame.transform.rotate(card.card_back_image, card.current_rate % 360)  # 绘制卡背
        card.new_rect = new_card.get_rect(center=card.rect.center)
        screen.blit(new_card, card.new_rect)


def game(screen, settings, TOKEN, UUID, player_id):
    """
    游戏主程序 \n
    :param screen: 屏幕
    :param settings: 窗口设置
    :return: 暂无返回值
    """
    # 游戏是否需要等待
    wait = True
    # 标记你是否是先手方
    you_first = True

    while wait:
        time.sleep(2)
        last_msg = Get_last(TOKEN, UUID)
        if last_msg['code'] == 200:
            you_first = last_msg['data']['your_turn']
            wait = False
    if player_id == 1:
        print("此人是游戏创建者")
    if player_id == 2:
        print("此人是游戏加入者")

    you = 1  # 默认你是玩家1
    if you_first == True:
        print("你是先手")
    else:
        print("你是后手")

    background_sound = pygame.mixer.Sound("images/background.mp3")
    background_sound.play()
    cards_array = []
    cards_init(cards_array, settings)
    print(len(cards_array))
    print("over")
    show_cards(screen, cards_array, settings)
    # 在场的牌，围成圈的牌
    cards_in_show = []
    max_nums = 10  # 在场牌的最大数量
    # 圈中间的牌
    center_card = [0, []]  # 最顶层的牌，目前积压的牌
    turn = 2  # 默认的先手玩家玩家
    if you_first == True:
        turn = 1
    player1 = Player(1)
    player2 = Player(2)
    font = pygame.font.Font('images/MIAO.TTF', 80)
    click_card_sound = pygame.mixer.Sound("images/cp.ogg")
    input("对局加载完成,准备好开始游戏了吗？")

    while True:
        # screen.fill((0, 0, 0))  # 屏幕填充纯黑色背景
        screen.blit(bg, (0, 0))  # 绘制背景图片
        # 获取事件
        events = pygame.event.get()
        for event in events:
            # 如果按键类型为 窗口右上角的八叉 或 ESC （目前ESC好像不管用）
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                # 程序推出
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and turn == you:
                # 选择翻牌
                for card in cards_in_show:
                    if in_rect(event.pos, card.new_rect):
                        # 选择了翻牌
                        re_do_card = Do_card(TOKEN, UUID, '0')
                        card.set_by_msg(re_do_card)
                        print("玩家", turn, "翻开了", card.get_msg())
                        card.rect.centerx, card.rect.centery = settings.screen_width / 2, settings.screen_height / 2
                        if not center_card[0]:  # 如果中间没牌
                            center_card[0] = card
                        elif card.kind != center_card[0].kind:
                            center_card[1].append(center_card[0])
                            center_card[0] = card
                        else:
                            center_card[1].append(card)
                            center_card[1].append(center_card[0])
                            player1.receive_card(turn, center_card[1])
                            player2.receive_card(turn, center_card[1])
                            center_card = [0, []]  # 重置
                        cards_in_show.remove(card)
                        click_card_sound.play()
                        turn += 1
                        if turn > 2:
                            turn = 1
                        break
                for card in player1.card_array:
                    if in_rect(event.pos, card.rect):
                        print(turn, "打出了", card.get_msg())
                        Do_card(TOKEN, UUID, '1', str_card=card.get_msg())
                        card.rect.centerx, card.rect.centery = settings.screen_width / 2, settings.screen_height / 2
                        if not center_card[0]:  # 如果中间没牌
                            center_card[0] = card
                            player1.card_array.remove(card)
                        elif card.kind != center_card[0].kind:
                            center_card[1].append(center_card[0])
                            center_card[0] = card
                            player1.card_array.remove(card)
                        else:
                            center_card[1].append(center_card[0])
                            player1.receive_card(turn, center_card[1])
                            player2.receive_card(turn, center_card[1])
                            center_card = [0, []]  # 重置
                        turn += 1
                        if turn > 2:
                            turn = 1
                        click_card_sound.play()
                        break
            elif turn != you:
                # 获取对手信息
                re_msg = Get_last(TOKEN, UUID)
                # 还没轮到我说明对手还没操作呢
                if re_msg['data']['your_turn'] == False:
                    print("对手还没出牌，在等等")
                    break
                # 轮到我了说明对手已经操作了
                elif re_msg['data']['your_turn'] == True:
                    if re_msg['data']['last_code'][2] == '0':  # 选择了翻牌
                        for card in cards_in_show:
                            card.set_by_msg(re_msg)
                            print(turn, "翻开了", card.get_msg())
                            card.rect.centerx, card.rect.centery = settings.screen_width / 2, settings.screen_height / 2

                            if not center_card[0]:  # 如果中间没牌
                                center_card[0] = card
                            elif card.kind != center_card[0].kind:
                                center_card[1].append(center_card[0])
                                center_card[0] = card
                            else:
                                center_card[1].append(card)
                                center_card[1].append(center_card[0])
                                player1.receive_card(turn, center_card[1])
                                player2.receive_card(turn, center_card[1])
                                center_card = [0, []]  # 重置

                            cards_in_show.remove(card)
                            click_card_sound.play()
                            turn += 1
                            if turn > 2:
                                turn = 1
                            break

                    elif re_msg['data']['last_code'][2] == '1':  # 选择了出牌
                        for card in player2.card_array:

                            if card.get_msg() == re_msg['data']['last_code'][4:]:
                                print(turn, "打出了了", card.get_msg())
                                card.rect.centerx, card.rect.centery = settings.screen_width / 2, settings.screen_height / 2
                                if not center_card[0]:  # 如果中间没牌
                                    center_card[0] = card
                                    player2.card_array.remove(card)
                                elif card.kind != center_card[0].kind:
                                    center_card[1].append(center_card[0])
                                    center_card[0] = card
                                    player2.card_array.remove(card)
                                else:
                                    center_card[1].append(center_card[0])
                                    player1.receive_card(turn, center_card[1])
                                    player2.receive_card(turn, center_card[1])
                                    center_card = [0, []]  # 重置
                                turn += 1
                                if turn > 2:
                                    turn = 1
                                click_card_sound.play()
                                break

        player1.card_array = sorted(player1.card_array, key=lambda x: x.kind)
        player2.card_array = sorted(player2.card_array, key=lambda x: x.kind)
        player1.update(turn, screen, settings)
        player2.update(turn, screen, settings)
        # 对于牌库中的每张卡牌
        for card in cards_array:
            screen.blit(card.card_back_image, card.rect)  # 将每张牌 以牌背 绘制到屏幕上
            # 这个没太大用，主要是让卡牌显示的好看些
            pygame.draw.line(screen, (100, 100, 100), (card.rect.left, card.rect.top), (card.rect.right, card.rect.top),
                             1)
        # 如果围成圈的卡牌 数量小于3， 添加新卡牌，添加数量为 最大值 - 当前数量
        if len(cards_in_show) <= 0:
            print("牌有点少，抽几张吧")
            temp = []
            for i in range(max_nums - len(cards_in_show)):
                # 如果牌库里还有牌
                if len(cards_array) != 0:
                    card = random.choice(cards_array)
                    temp.append(card)
                    cards_array.remove(card)
                else:
                    break
            # 如果 临时卡牌存储 里有卡牌
            if len(temp) != 0:
                # 显示插入动画，并调整新卡牌的坐标，和旋转角度
                show_insert(screen, settings, temp, cards_in_show, cards_array, player1, player2, turn)
            # 如果 围成圈的卡牌 数量为0
            if len(cards_in_show) <= 0:
                # 说明 场上无牌了，
                background_sound.stop()
                if len(player1.card_array) < len(player2.card_array):
                    print("player1 win")
                    player1.win(screen, settings)
                else:
                    print("player2 win")
                    player2.win(screen, settings)
                game_wait_close()

        mouse_pos = pygame.mouse.get_pos()
        for card in cards_in_show:
            if in_rect(mouse_pos, card.new_rect):
                new_click_effect = pygame.transform.rotate(click_effect, card.current_rate)  # 绘制卡背
                card.new_rect = click_effect.get_rect(center=card.new_rect.center)
                screen.blit(new_click_effect, card.new_rect)
                break

        if turn == 1:
            for card in player1.card_array:
                if in_rect(mouse_pos, card.rect):
                    screen.blit(click_effect, [n - 10 for n in card.rect])
                    break
        else:
            for card in player2.card_array:
                if in_rect(mouse_pos, card.rect):
                    screen.blit(click_effect, [n - 10 for n in card.rect])
                    break

        # 更新圈中间 的card
        if center_card[0]:
            screen.blit(center_card[0].image, center_card[0].rect)
            # ---------------------------------------
            if len(center_card[1]) != 0:
                text = "X" + str(len(center_card[1]) + 1)
                text_render = font.render(text, True, (0, 255, 0))
                text_rect = text_render.get_rect()
                screen.blit(text_render, (
                center_card[0].rect.right + text_rect.width / 2, center_card[0].rect.centery - text_rect.height / 2))
            # ---------------------------------------
        # 调整坐标
        position_correct(cards_in_show, settings, screen)
        # 更新画面
        pygame.display.update()
def game_wait_close():
    while True:
        for event in pygame.event.get():
            # 如果按键类型为 窗口右上角的八叉 或 ESC （目前ESC好像不管用）
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                # 程序推出
                pygame.quit()
                sys.exit()


if __name__ == '__main__':
    # 此处的代码为了方便该文件单独运行测试
    import pygame
    import settings

    settings = settings.Settings()
    pygame.init()
    screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
    # 创建
    TOKEN2 = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYzNDMwMTkxNCwiZXhwIjoxNjM1MTY1OTE0fQ.eyJpZCI6ODN9.YCqmbEJcD7rd1JxOM1Ugm_6HH-KE-xsCiCxwoFDRyq4VjdA130CUjVcOch4AWTexB68F2NYsfcuXnIJxgrFuSw'
    # 加入
    TOKEN1 = 'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYzNDI5ODQxNSwiZXhwIjoxNjM1MTYyNDE1fQ.eyJpZCI6NzV9.iFo-YSODfdMAXEOPhb18LOIYV4eZbYe1BNg4wHA9OSHMgf6NBoP9CGsoPwCMNyuWW30X7F1THtA6LWtI_8bF7A'
    UUID = 'orhl8bbikyokc9zz'
    mode = input("创建者(1) 还是加入者(2)")
    if mode == '1':
        game(screen, settings, TOKEN1, UUID, 1)
    else:
        Join_Game(TOKEN2, UUID)
        game(screen, settings, TOKEN2, UUID, 2)
