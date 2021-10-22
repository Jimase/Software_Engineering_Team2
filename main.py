import tkinter as tk
import pygame_textinput
import GamePVP
from settings import Settings
import time
import Game
import GamePM,GamePM2
from GamePVP import *
from Game import in_rect

# 初始化pygame
pygame.init()
# 初始化音效
pygame.mixer.init()
# 创建窗口设置
settings = Settings()
# 创建屏幕
screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
clock = pygame.time.Clock()
# 设置按键重复事件
pygame.key.set_repeat(200, 60)  # press every 50 ms after waiting 200 ms

def _login(username,password):
    """
    登录模块 \n
    :return: 登陆成功 / 登陆失败
    """
    data1 = {'student_id': username, 'password': password}
    r1 = requests.post('http://172.17.173.97:8080/api/user/login', data=data1)
    user_dict1 = json.loads(r1.text)
    user_dict = user_dict1
    print("user_dict:", user_dict)
    log_msg = user_dict1
    print("stu_msg：",log_msg)
    print("success loading")
    return log_msg
def login():
    """
    登陆页面 \n
    :return: 学生信息
    """
    #最终返回的信息
    login_menu = pygame.image.load('images/login.png')
    # 账号，密码输入域
    font = pygame.font.SysFont("宋体", 55)
    username = pygame_textinput.TextInputVisualizer(antialias=True, font_object=font)

    username_area = [1120, 250]                 # 整个输入区域
    username_input_position = [1145, 280]       # 输入光标所在位置 25,25

    password = pygame_textinput.TextInputVisualizer(antialias=True, font_object=font,)
    password_area = [1120, 410]
    password_input_position = [1145, 440]

    username.font_color = (0, 85, 180)
    password.font_color = (0, 85, 180)
    # 设置账号密码的初始值，如果不需要，请删除
    username.value = '031902515'
    password.value = '31415926swh'

    login_button_area = [1120, 1145, 560, 650]  # x1, x2, y1, y2
    # 输入框 聚焦时/有文字时 高亮
    lightning_image = pygame.image.load("images/lightning.png")
    lightning_rect = lightning_image.get_rect()

    curse_focus = ""
    old_time = time.time()
    click_login_button = False

    while True:
        username.font_color = [(c - 3) % 255 for c in username.font_color]
        password.font_color = [(c + 3) % 255 for c in password.font_color]
        new_time = time.time()
        screen.blit(login_menu, (0, 0))
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 鼠标点击事件
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # 判断鼠标点击区域
                # 先判断y坐标，然后判断x坐标
                if in_rect(event.pos, (username_area[0], username_area[1], lightning_rect.width, lightning_rect.height)):
                    # 如果点了 用户名的输入区域
                    curse_focus = "username"
                elif in_rect(event.pos, (password_area[0], password_area[1], lightning_rect.width, lightning_rect.height)):
                    # 如果点了 密码的输入区域
                    curse_focus = "password"
                elif in_rect(event.pos, (login_button_area[0], login_button_area[2], lightning_rect.width, lightning_rect.height)):
                    # 如果点了登录按钮
                    click_login_button = True
            # 回车 或 点击登录按钮
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN) or click_login_button:
                click_login_button = False
                print("正在登录...")
                stu_msg = _login(username.value,password.value)
                if stu_msg['message'] == 'Success':
                    print("登陆成功！")
                    return stu_msg
                else:
                    print("登陆失败")
                    return 0

        # 如果当前焦点为 用户名输入域
        if curse_focus == "username":
            username.update(events)
            # 使用户可以在文段末输入TAB换行
            if username.value != "":
                if username.value[-1] == "	":
                    username.value = username.value[:-1]
                    if new_time - old_time > 0.5:
                        curse_focus = "password"
                        # password.cursor_pos = len(password.value)
                        old_time = new_time
            password.cursor_color = (255, 255, 255)
            username.cursor_color = (0, 0, 0)
        # 如果输入框聚焦或者有文字，则背景高亮
        if curse_focus == "username" or username.value != "":
            screen.blit(lightning_image, username_area)
        # 如果当前焦点为 密码输入域
        if curse_focus == "password":
            password.update(events)
            # 使用户可以在文段末输入TAB换行
            if password.value != "":
                if password.value[-1] == "	":
                    password.value = password.value[:-1]
                    if new_time - old_time > 0.5:
                        curse_focus = "username"
                        # username.cursor_pos = len(username.value)
                        old_time = new_time
            username.cursor_color = (255, 255, 255)
            password.cursor_color = (0, 0, 0)
        # 如果输入框聚焦或者有文字，则背景高亮
        if curse_focus == "password" or password.value != "":
            screen.blit(lightning_image, password_area)
        # 绘制输入框
        screen.blit(username.surface, username_input_position)
        screen.blit(password.surface, password_input_position)
        # 限制fps
        clock.tick(settings.fps)
        # 画面更新
        pygame.display.update()
def start():
    """
    模式选择页面 人人，人机，联网 \n
    :return: 所选模式
    """
    # 载入音效
    button = pygame.mixer.Sound("images/button.wav")
    # 载入图片
    start_menu = pygame.image.load('images/start.png')
    # 最终模式选择
    last_choice_mode = 0  # 1.人人 2.人机 3.联机
    # 当前模式选择
    current_choice_mode = 0
    while True:
        # 绘制背景图片
        screen.blit(start_menu, (0, 0))
        # 检测事件
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 检测鼠标移动
            elif event.type == pygame.MOUSEMOTION:
                # 判断鼠标所处位置  x:630 y:270, 450, 630  x2:1180 y2:360
                if in_rect(event.pos, (630, 270, 550, 90)):
                    current_choice_mode = 1     # 人人
                if in_rect(event.pos, (630, 450, 550, 90)):
                    current_choice_mode = 2     # 人机
                if in_rect(event.pos, (630, 630, 550, 90)):
                    current_choice_mode = 3     # 联网
                if current_choice_mode != last_choice_mode:
                    last_choice_mode = current_choice_mode
                    button.play()   # 播放音效
            # 如果鼠标按下
            if event.type == pygame.MOUSEBUTTONDOWN:  # (490 + 420, 210/350/490 + 70)
                # 只要最终模式不为空
                if last_choice_mode != 0:
                    return last_choice_mode

        clock.tick(settings.fps)
        pygame.display.update()
def pvp_start():
    """
    模式选择页面 创建 加入 返回\n
    :return: 所选模式
    """
    # 载入音效
    button = pygame.mixer.Sound("images/button.wav")
    # 载入图片
    start_menu_pvp = pygame.image.load('images/start_pvp.png')

    last_choice_mode = 0  # 1.创建游戏 2.加入游戏 3.返回菜单
    # 当前模式选择
    current_choice_mode = 0

    while True:
        # 绘制背景图片
        screen.blit(start_menu_pvp, (0, 0))
        # 检测事件
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 检测鼠标移动
            elif event.type == pygame.MOUSEMOTION:
                # 判断鼠标所处位置  x:630 y:270, 450, 630  x2:1180 y2:360
                if in_rect(event.pos, (630, 270, 550, 90)):
                    current_choice_mode = 1     # 创建游戏
                if in_rect(event.pos, (630, 450, 550, 90)):
                    current_choice_mode = 2     # 加入游戏
                if in_rect(event.pos, (630, 630, 550, 90)):
                    current_choice_mode = 3     # 返回菜单
                if current_choice_mode != last_choice_mode:
                    last_choice_mode = current_choice_mode
                    button.play()   # 播放音效
            # 如果鼠标按下
            if event.type == pygame.MOUSEBUTTONDOWN:  # (490 + 420, 210/350/490 + 70)
                # 只要最终模式不为空
                if last_choice_mode != 0:
                    return last_choice_mode
        clock.tick(settings.fps)
        pygame.display.update()

def pm_start():
    """
    模式选择页面 创建 加入 返回\n
    :return: 所选模式
    """
    # 载入音效
    button = pygame.mixer.Sound("images/button.wav")
    # 载入图片
    start_menu_pm = pygame.image.load('images/start_pm.png')

    last_choice_mode = 0  # 1.创建游戏 2.加入游戏 3.返回菜单
    # 当前模式选择
    current_choice_mode = 0

    while True:
        # 绘制背景图片
        screen.blit(start_menu_pm, (0, 0))
        # 检测事件
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 检测鼠标移动
            elif event.type == pygame.MOUSEMOTION:
                # 判断鼠标所处位置  x:630 y:270, 450, 630  x2:1180 y2:360
                if in_rect(event.pos, (630, 270, 550, 90)):
                    current_choice_mode = 1     # 标准
                if in_rect(event.pos, (630, 450, 550, 90)):
                    current_choice_mode = 2     # 困难
                if in_rect(event.pos, (630, 630, 550, 90)):
                    current_choice_mode = 3     # 返回菜单
                if current_choice_mode != last_choice_mode:
                    last_choice_mode = current_choice_mode
                    button.play()   # 播放音效
            # 如果鼠标按下
            if event.type == pygame.MOUSEBUTTONDOWN:  # (490 + 420, 210/350/490 + 70)
                # 只要最终模式不为空
                if last_choice_mode != 0:
                    return last_choice_mode
        clock.tick(settings.fps)
        pygame.display.update()

def Create_start():
    """
    模式选择页面 创建 加入 返回\n
    :return: 所选模式
    """
    # 载入音效
    button = pygame.mixer.Sound("images/button.wav")
    # 载入图片
    start_menu_pvp = pygame.image.load('images/start_Create.png')

    last_choice_mode = 0  # 1.私人对局 2.公开对局 3.返回菜单
    # 当前模式选择
    current_choice_mode = 0

    while True:
        # 绘制背景图片
        screen.blit(start_menu_pvp, (0, 0))
        # 检测事件
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            # 检测鼠标移动
            elif event.type == pygame.MOUSEMOTION:
                # 判断鼠标所处位置  x:630 y:270, 450, 630  x2:1180 y2:360
                if in_rect(event.pos, (630, 270, 550, 90)):
                    current_choice_mode = 1     # 私人对局
                if in_rect(event.pos, (630, 450, 550, 90)):
                    current_choice_mode = 2     # 公开对局
                if in_rect(event.pos, (630, 630, 550, 90)):
                    current_choice_mode = 3     # 返回菜单
                if current_choice_mode != last_choice_mode:
                    last_choice_mode = current_choice_mode
                    button.play()   # 播放音效
            # 如果鼠标按下
            if event.type == pygame.MOUSEBUTTONDOWN:  # (490 + 420, 210/350/490 + 70)
                # 只要最终模式不为空
                if last_choice_mode != 0:
                    return last_choice_mode
        clock.tick(settings.fps)
        pygame.display.update()

def begin_ui(login_re_msg):
    flag = True
    while flag:
        mode = start()                      # 模式选择页面
        if mode == 1:                       # 人人对战
            Game.game(screen, settings)
        elif mode == 2:                       # 人机模式
            mode == pm_start()
            if mode == 1:
                GamePM.game(screen, settings)
            if mode == 2:
                GamePM2.game(screen,settings)
            if mode == 3:
                continue
        elif mode == 3:                       # 在线模式
            mode = pvp_start()              # 创建还是加入对局？
            if(mode == 1):                  #创建对局
                mode = Create_start()
                if mode == 1:                                       #私人对局
                    create_game_re_msg = Create_Game(login_re_msg['data']['token'],True)
                    UUID = create_game_re_msg['data']['uuid']
                    print("把你的uuid分享给好友吧！")
                    GamePVP.game(screen,settings,login_re_msg['data']['token'],UUID,2)
                    flag = False
                elif mode == 2:                                       #公开对局
                    create_game_re_msg = Create_Game(login_re_msg['data']['token'],False)
                    UUID = create_game_re_msg['data']['uuid']
                    print("把你的uuid分享给好友吧！")
                    GamePVP.game(screen,settings,login_re_msg['data']['token'],UUID,2)
                    flag = False                                    #返回
                elif mode == 3:
                   continue
            elif(mode == 2):                  #加入对局
                UUID = input("麻烦输入下好友给你的uuid：")
                GamePVP.game(screen,settings,login_re_msg['data']['token'],UUID,2)
            elif(mode == 3):
                continue       #返回


        # 查询游戏
        # Query_Game(login_re_msg['data']['token'],10,1)
        # 创建游戏，返回该游戏的标识uuid，并且输出"请把你的uuid分享给朋友们吧"
        # uuid = Create_Game(login_re_msg['data']['token'])
        # uuid =''
        # #加入游戏
        # Join_Game(login_re_msg['data']['token'] , uuid )

def main():
    login_re_msg = login()    # 登录页面
    print("token:",login_re_msg['data']['token'])
    begin_ui(login_re_msg)

if __name__ == '__main__':
    main()
    # login2()
