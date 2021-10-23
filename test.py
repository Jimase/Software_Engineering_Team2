from AIwithouUI import *
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
if __name__ == '__main__':
    print("这是AI参站系统,为了运行速度，我们放弃了UI可视化界面，如果需要请换一台电脑用左边的AIpy来观战")
    student_id = '031902511'
    password = 'lllwww909090'
    login_dict = __login(student_id, password)
    TOKEN = login_dict['data']['token']
    mode = input("加入还是创建对局？1：加入,2:创建")
    if mode == '1':
        UUID = input("请输入别人给你的房间的UUID")
        Join_Game(TOKEN, UUID)
        game(TOKEN, UUID)
    else:
        cre_msg = Create_Game(TOKEN, True)
        UUID = cre_msg['data']['uuid']
        game(TOKEN, UUID)


