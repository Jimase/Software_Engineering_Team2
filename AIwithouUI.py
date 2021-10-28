# -*- coding: utf-8 -*-
# @Time : 2021/10/22 23:29
# @Author : Jimase
# @File : AIwithouUI.py
import requests
import json
import time
# 黑桃:S == 0
# 红桃:H == 1
# 梅花:C == 2
# 方块:D == 3

#
# num_org = [13, 13, 13, 13]
# num_show = [-1, [0, 0, 0, 0]]
# num_ai = [0, 0, 0, 0]
# num_p = [0, 0, 0, 0]


def __login(username, password):
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
    print("stu_msg：", log_msg)
    print("success loading")
    return log_msg
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
    # print(user_dict)
    return user_dict
def Do_card(token, uuid, type, str_card=''):
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
        'type': int(type),
        'card': str_card
    }
    payload = json.dumps(param)
    r = requests.put(url, headers=header, data=payload)
    user_dict = json.loads(r.text)
    # print(user_dict)
    return user_dict
    # {
    #     "code": 200,
    #     "data": {
    #         "last_code": "1 0 D10",
    #         "last_msg": "2P 从<牌库>翻开了一张 D10"
    #     },
    #     "msg": "操作成功"
    # }
class Card:
    '''
    ·········接口端： ======本地端：
    ♠ spade（黑桃，又名葵扇）        黑桃:S
    ♥ heart（红心，又名红桃）        红桃:H
    ♣ club（梅花，又名草花）         梅花:C
    ♦ diamond（方块，又名阶砖）      方块:D
    '''

    def __init__(self):
        self.color = ''
        self.size = ''

    def set_by_msg(self, msg):
        if type(msg) == str:
            self.color = msg[0]
            self.size = msg[1:]
        else:
            self.color = msg['data']['last_code'][4]
            self.size = msg['data']['last_code'][5:]

    def get_color(self):
        return self.color
    def get_size(self):
        return self.size

def color_to_num(str):
    if str == 'S' :
        return 0
    elif str == 'H':
        return 1
    elif str == 'C':
        return 2
    elif str == 'D':
        return 3
    else:
        return -1

def num_to_color(num):
    if num == 0:
        return 'S'
    elif num == 1:
        return 'H'
    elif num == 2:
        return 'C'
    elif num == 3:
        return 'D'
    else:
        print("见鬼了")
        return ''


def solusion(center_card,card_ai,card_people,ans):

    # ans[0] = '0'
    # return 0

    lc_show = 'U'       #中心展示的花色
    la = len(card_ai)
    lp = len(card_people)
    lc = len(center_card)
    if center_card[0] != '0':
        lc += 1
        lc_show = center_card[0].get_color()
    lo = 13*4 - la - lp - lc


    card_array =[ [13,13,13,13],
                  [0 ,0 ,0 ,0 ],
                  [0 ,0 ,0 ,0 ],
                  [0 ,0 ,0 ,0 ] ]

    for card in card_ai:
        card_array[2][color_to_num(card.get_color())] +=1
    for card in card_people:
        card_array[3][color_to_num(card.get_color())] +=1
    for card in center_card[1]:
        card_array[1][color_to_num(card.get_color())] +=1
    if center_card[0]!= '0':
        card_array[1][color_to_num(center_card[0].get_color())] += 1

    for i in range(3):
        card_array[0][i] = 13 - card_array[1][i] - card_array[2][i] - card_array[3][i]
    #没牌没啥好说的,就翻牌吧

    # print(card_array)
    if la == 0 :
        ans[0] = '0'
        ans[1] = ''
        return 0
    #必胜 随便我怎么拿牌

    elif la + 1 + (lo-1)*2 + lc < lp - lo + 1 :
        ans[0] = '0'
        ans[1] = ''
        return 0

    #必最佳操作
    elif lo == 1:            #对于最后一张牌
        last_num = 0
        for i in range(3):
            if card_array[i] == 1:
                last_num = i                                #知道最后一张牌的花色了

        if la < lp:                                         #牌比对手少、无进攻压力
            if color_to_num(lc_show) != last_num:           #翻掉算了
                ans[0] = '0'
                ans[1] = ''
                return 0

            elif color_to_num(lc_show) == last_num:           #颜色是一样的
                for card in card_ai :
                    if color_to_num(card.get_color()) != last_num:  #打一张不一样花色的就可以了
                        ans[0] = '1'
                        ans[1] = card.get_color()+card.get_size()
                        return 0
                ans[0] = '0'
                return 0

        elif la > lp:                                           #牌比对手多、我有进攻压力
            if color_to_num(lc_show) != last_num:
                for card in card_ai :
                    if card.get_color() == num_to_color(last_num):
                        ans[0] = '1'
                        ans[1] = card.get_color()+card.get_size()
                        return 0
                for card in card_ai :
                    if card.get_color() != num_to_color(lc_show):
                        ans[0] = '1'
                        ans[1] = card.get_color()+card.get_size()
                        return 0
                ans[0] = '0'
                return 0
            else:
                for card in card_ai:
                    if card.get_color() != num_to_color(last_num):
                        ans[0] = '1'
                        ans[1] = card.get_color()+card.get_size()
                        return 0
                ans[0] = '0'
                return 0

        elif la == lp:
            if color_to_num(lc_show) != last_num:
                for card in card_ai:
                    if card.get_color() == num_to_color(last_num):
                        ans[0] = '1'
                        ans[1] = card.get_color() + card.get_size()
                        return 0
                for card in card_ai:
                    if card.get_color()!=num_to_color(last_num):
                        ans[0] = '1'
                        ans[1] = card.get_color() + card.get_size()
                        return 0
            else:
                for card in card_ai:
                    if card.get_color()!=num_to_color(last_num):
                        ans[0] = '1'
                        ans[1] = card.get_color() + card.get_size()
                        return 0
                ans[0] = '0'
                ans[1] = ''
                return 0
        else:
            ans[0] = '0'
            ans[1] = ''
            return 0

    elif lo != 1:
        if la + lc - lo > lp +2*lo:
            for card in card_ai:
                if card.get_color() != lc_show:      #绝对不能吃
                    ans[0] = '1'
                    ans[1] = card.get_color() + card.get_size()
                    return 0

            ans[0] = '0'
            return 0
        elif la + lc - lo > lp:
            for card in card_ai:
                if card.get_color() != lc_show:      #绝对不能吃
                    ans[0] = '1'
                    ans[1] = card.get_color() + card.get_size()
                    return 0

            ans[0] = '0'
            return 0
        # if la > lc :
        #     if lp + lc - lo > la + lo*2:
        #         for card in card_ai:
        #             if card.get_color() == lc_show:  # 大胆吃
        #                 ans[0] = '1'
        #                 ans[1] = card.get_color() + card.get_size()
        #                 return 0

        elif la + lc <= lp + 2:
            for card in card_ai:
                if card.get_color() == lc_show:             #大胆吃
                    ans[0] = '1'
                    ans[1] = card.get_color() + card.get_size()
                    return 0

            ans[0] = '0'
            ans[1] = ' '
            return 0

                                         #la+lc>lp
        elif (la+lc) + lo*2 -1 >= lp - lo:          #拿了就输了
            for card in card_ai:
                if card.get_color() != lc_show:
                    ans[0] = '1'
                    ans[1] = card.get_color()+card.get_size()
                    return 0

            ans[0] = '0'
            ans[1] = ''
            return 0
        else :
            if la > lp :    # 大概率能让对手拿
                if lp + lc + 1 - lo > la - 1 + lo*2: #那就务必施压
                    for card in card_ai:
                        if card.get_color() != lc_show:
                            ans[0] = '1'
                            ans[1] = card.get_color() + card.get_size()
                            return 0

                    ans[0] = '0'
                    ans[1] = ''
                    return 0
                else :
                    for card in card_ai:
                        if card.get_color() != lc_show:
                            ans[0] = '1'
                            ans[1] = card.get_color() + card.get_size()
                            return 0

                    ans[0] = '0'
                    ans[1] = ''
                    return 0
            else:
                for card in card_ai:
                    if card.get_color() != lc_show:
                        ans[0] = '1'
                        ans[1] = card.get_color() + card.get_size()
                        return 0

                ans[0] = '0'
                ans[1] = ''
                return 0

    else:
        ans[0] = '0'
        ans[1] = ''
        return 520
def game(TOKEN, UUID):

    center_card = ['0', []]
    card_ai = []
    card_people = []
    wait = True
    your_first = True

    while wait:
        last_msg = Get_last(TOKEN, UUID)
        if last_msg['code'] == 200:
            your_first = last_msg['data']['your_turn']
            wait = False

    ai = 1  # 默认你是玩家1
    turn = 1
    if your_first == True:
        print("你是先手")
    else:
        print("你是后手")
        turn = 2
    ans = ['', '']

    while True:
        # time.sleep(10)
        cnt = 0
        print("ai:      ", end=' ')
        for card in card_ai:
            print(card.get_color() + card.get_size(), end=' ')
            cnt+=1

        print('')
        print("people:  ", end=' ')
        for card in card_people:
            print(card.get_color() + card.get_size(), end=' ')
            cnt+=1

        print()
        print("center   ", end=' ')
        for card in center_card[1]:
            print(card.get_color() + card.get_size(), end=' ')
            cnt += 1
        if center_card[0] != '0':
            print(center_card[0].get_color()+center_card[0].get_size())
            cnt+=1

        print(cnt)
        # input("断点")
        get_last = Get_last(TOKEN,UUID)
        if get_last['code'] == 400:
            print("游戏结束")
            input("任意键退出")
            return 0

        if turn == ai:
            ans[0] = ''
            ans[1] = ''

            solusion(center_card,card_ai,card_people,ans)

            if ans[0] == '0':
                # 如果选择了翻牌
                re_do_card = Do_card(TOKEN, UUID, '0')
                a = Card()
                a.set_by_msg(re_do_card)

                if center_card[0] == '0':  # 若中间没牌
                    center_card[0] = a
                elif a.get_color() != center_card[0].get_color():
                    center_card[1].append(center_card[0])
                    center_card[0] = a
                else:
                    center_card[1].append(a)
                    center_card[1].append(center_card[0])

                    card_ai.extend(center_card[1])

                    center_card = ['0', []]  # 清空

                turn += 1
                if turn > 2:
                    turn = 1
            elif ans[0] == '1':
                a = Card()
                a.set_by_msg(ans[1])
                Do_card(TOKEN, UUID, '1', a.get_color() + a.get_size())
                for card in card_ai:
                    if card.get_color() == a.get_color():
                        if card.get_size() == card.get_size():
                            card_ai.remove(card)
                            break

                if center_card[0] == '0':  # 若中间没牌
                    center_card[0] = a
                elif a.get_color() != center_card[0].get_color():
                    center_card[1].append(center_card[0])
                    center_card[0] = a
                else:
                    center_card[1].append(a)
                    center_card[1].append(center_card[0])
                    card_ai.extend(center_card[1])
                    center_card = ['0', []]  # 清空

                turn += 1
                if turn > 2:
                    turn = 1

        else:
            # 获取对手信息
            re_msg = Get_last(TOKEN, UUID)
            # 还没轮到我说明对手还没出
            if re_msg['data']['your_turn'] == False:
                # print("对手还没出牌，在等等")
                pass

                # 轮到我说明对手已经出牌了
            elif re_msg['data']['your_turn'] == True:
                if re_msg['data']['last_code'][2] == '0':
                    a = Card()
                    a.set_by_msg(re_msg)

                    if center_card[0] == '0':  # 若中间没牌
                        center_card[0] = a
                    elif a.get_color() != center_card[0].get_color():
                        center_card[1].append(center_card[0])
                        center_card[0] = a
                    else:
                        center_card[1].append(a)
                        center_card[1].append(center_card[0])

                        card_people.extend(center_card[1])

                        center_card = ['0', []]  # 清空

                    turn += 1
                    if turn > 2:
                        turn = 1

                elif re_msg['data']['last_code'][2] == '1':
                    a = Card()
                    a.set_by_msg(re_msg)

                    for card in card_people:
                        if card.get_color() == a.get_color() :
                            if card.get_size() == card.get_size():
                                card_people.remove(card)
                                break

                    if center_card[0] == '0':  # 若中间没牌
                        center_card[0] = a
                    elif a.get_color() != center_card[0].get_color():
                        center_card[1].append(center_card[0])
                        center_card[0] = a
                    else:
                        center_card[1].append(a)
                        center_card[1].append(center_card[0])

                        card_people.extend(center_card[1])

                        center_card = ['0', []]  # 清空

                    turn += 1
                    if turn > 2:
                        turn = 1
def main():
    print("这是AI参站系统,为了运行速度，我们放弃了UI可视化界面，如果需要请换一台电脑用左边的AIpy来观战")
    student_id = '031902515'
    password = '31415926swh'
    login_dict = __login(student_id, password)
    TOKEN = login_dict['data']['token']
    mode = input("加入还是创建对局？输入1：加入,输入2:创建")
    if mode == '1':
        UUID = input("请输入别人给你的房间的UUID")
        Join_Game(TOKEN, UUID)
        game(TOKEN, UUID)
    else:
        cre_msg = Create_Game(TOKEN, False)
        UUID = cre_msg['data']['uuid']
        print("把uuid复制给你的对手吧")
        game(TOKEN, UUID)

if __name__ == '__main__':
    main()


