import time
import pyautogui
import pyperclip
import cv2
import numpy as np
import aircv as ac
import Levenshtein
from PIL import ImageGrab
from aip import AipOcr

pyautogui.PAUSE = 3


def node_color(color_test):
    """
    颜色检查
    :param color_test:((被检查),(预期颜色))
    :return:
    """
    while True:
        time.sleep(3)
        c = (color_test[0][0], color_test[0][1], color_test[0][0] + 1, color_test[0][1] + 1)
        img = ImageGrab.grab(c)
        if img.getcolors()[0][1] == color_test[1]:
            return True


def img_ocr(url='./img/temp.png', dot=None):
    """
    识别文字
    :param url: 图像路径
    :return:
    """
    if dot:
        ImageGrab.grab(dot).save(url)  # 截图 选项
    APP_ID = 'xxxx'
    API_KEY = 'xxxx'
    SECRET_KEY = 'xxxx'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    with open(url, "rb") as f:
        message = client.basicGeneral(f.read())
        return [i['words'] for i in message['words_result']]


def click(dot, color_test=None):
    """
    点击目标点
    :param dot:(点击位置)
    :param color_test:((被检查点范围),(预期颜色))
    :return:
    """

    def p():
        pyautogui.moveTo(*dot, 2)
        pyautogui.click()
        pyautogui.moveRel(0, 2)

    p() if color_test and node_color(color_test) else p()


def drag(star, end, color_test=None):
    """
    鼠标按住拖动
    :param star:(开始位置)
    :param end:(结束位置)
    :param color_test:((被检查范围),(预期颜色值))
    :return:
    """

    def p():
        time.sleep(3)
        pyautogui.moveTo(*star, 2)
        pyautogui.dragTo(*end, 2)

    p() if color_test and node_color(color_test) else p()


def shape(url, color_test=None):
    """
    查找图形
    :param url:被查找的图形（小图）
    :param color_test:((被检查范围),(预期颜色值))
    :return:
    """

    def p():
        u = './img/temp.png'
        img = ImageGrab.grab((0, 0, 763, 1393)).save(u)  # 截取原始图形
        src = cv2.imread(u)  # 加载
        img = cv2.cvtColor(src, cv2.COLOR_RGB2GRAY)  # 转灰度
        cv2.imwrite(u, img, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])  # 存
        im = (ac.imread(u), ac.imread(url), 0.8)  # 原始图像，查找图像，相似度
        arr = ac.find_all_template(*im)  # 查找
        return [(i['result'][0], i['result'][1]) for i in arr]  # 坐标集合

    return p() if color_test and node_color(color_test) else p()


def read(s, n=None):
    """
    读文章列表
    :param s:列表
    :param n:次数
    :return:
    """
    x = 0
    for i in s:
        dot = [int(i[0]), int(i[1]), int(i[0]) + 1, int(i[1]) + 1]  # 拼坐标点 一个像素
        img = ImageGrab.grab(dot).getcolors()[0][1]  # 取颜色
        pyautogui.moveTo(*i, 2)
        pyautogui.click()
        x += 1
        if x and x >= n: return  # 计数判断
        if node_color((dot, img)):  # 颜色检查 博发放完毕
            continue


def answer_red(dot, color_test=None):
    """
    识别红色答案
    :param dot:截图范围
    :param color_test:((被检查范围),(预期颜色值))
    :return:
    """

    def p():
        u = './img/temp.png'
        img = ImageGrab.grab(dot).save(u)  # 截图
        src = cv2.imread(u)  # 加载
        hsv = cv2.cvtColor(src, cv2.COLOR_BGR2HSV)  # 颜色模式转换
        low_hsv = np.array([0, 43, 46])  # 下限 红
        high_hsv = np.array([10, 255, 255])  # 上限 红
        mask = cv2.inRange(hsv, lowerb=low_hsv, upperb=high_hsv)  # 取图
        cv2.imwrite(u, mask, [int(cv2.IMWRITE_PNG_COMPRESSION), 3])  # 存
        return img_ocr(u)  # 识别

    return p() if color_test and node_color(color_test) else p()


def choice(an, arr):
    """
    匹配答案与选项
    :param an: 答案
    :param arr: 选项
    :return:
    """
    s = []
    for i in an:  # 答案
        un = []
        for ii in arr:  # 选项
            un.append(Levenshtein.ratio(i, ii))  # 字符串匹配成程度
        a = set(un)
        if len(a) == 1:
            s = [i for i in range(0, len(un))]
        else:
            s.append(un.index(max(un)))  # 找出匹配程度最高的索引
    return s


def ctrlcv(dot, w):
    """
    模拟输入
    :param dot:目标坐标
    :param w:内容
    :return:
    """
    pyperclip.copy(w)
    click(dot)
    pyautogui.hotkey('ctrl', 'v')
