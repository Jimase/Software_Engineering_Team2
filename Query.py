import tkinter as tk
import pygame_textinput
import GamePVP
from settings import Settings
import time
import Game
import GamePM,GamePM2
from GamePVP import *
from Game import in_rect

# # 初始化pygame
# pygame.init()
# # 初始化音效
# pygame.mixer.init()
# # 创建窗口设置
# settings = Settings()
# # 创建屏幕
# screen = pygame.display.set_mode((settings.screen_width, settings.screen_height))
# clock = pygame.time.Clock()
# # 设置按键重复事件
# pygame.key.set_repeat(200, 60)  # press every 50 ms after waiting 200 ms

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
def Query_Game(token, page_size, page_num):
    headers = {'Authorization': token}
    params = {"page_size": str(page_size), "page_num": str(page_num)}
    r = requests.get(url='http://172.17.173.97:9000/api/game/index', headers=headers, params=params)
    # print(r.text)
    user_dict = json.loads(r.text)
    for i in user_dict['data']['games']:
        print(i)
    return user_dict

def main():
    print("这里用于查询房间号、很抱歉没能实现可视化加入房间,需要您手动输一下")
    while True:
        print("这里用于查询房间号、很抱歉没能实现可视化加入房间,需要您手动输一下")
        username = input("麻烦输入以下你的账号")
        password = input("请输入你的密码")
        log_re = _login(username,password)
        if log_re['status'] != 200:
            print("输入错误,请重新输入,或检查网络连接")
        else:
            break

    num = 0
    while True:
        Query_Game(log_re['data']['token'],'10',num)
        mode = input("输入1下一页、输入2上一页、找到想加入的对局就复制粘贴回去开始游戏吧")
        if mode == '2':
            num -= 1
        else:
            num += 1

if __name__ == '__main__':
    main()