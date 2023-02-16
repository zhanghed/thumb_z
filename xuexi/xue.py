import os
import time
from config import CON
from utils import click, read, img_ocr, shape, answer_red, ctrlcv, choice

"""主函数"""
print('启动')
os.system(CON['start'])  # 模拟器
click(**CON['app'])  # app
print('文章')
click(**CON['review_1'])  # 点击要闻
s = shape(**CON['review_2'])  # 获取列表
read(s, 6)  # 读文章
print('视频')
click(**CON['video_1'])  # 点击百灵
click(**CON['video_2'])  # 点击竖
click(**CON['video_3'])  # 开始播放
time.sleep(720)  # 等时间
click(**CON['video_4'])  # 退出
print('每日答题')
click(**CON['answer_1'])  # 点击我的
click(**CON['answer_2'])  # 我要答题
click(**CON['answer_3'])  # 每日答题
for i in range(5):
    click(shape(**CON['answer_4'])[0])  # 获取提示按钮位置  点击查看提示  只有一个
    an = answer_red(**CON['answer_5'])  # 识别答案
    print(an)
    click(**CON['answer_6'])  # 点击关闭提示
    ju = shape(**CON['answer_7'])  # 获取填空题形状集合 判断题型
    if ju:  # 填空题
        an = ["".join(an)]  # 合并字符串（防止有跨区域答案）
        ctrlcv(ju[0], *an)  # 输入答案
    else:  # 选择题
        op = shape(**CON['answer_8'])  # 获取选项集合
        op.sort()  # 排序
        arr = img_ocr(dot=(48, op[0][1] - 30, 560, op[-1][1] + 30))  # 识别文字 各选项
        print(arr)
        for i in choice(an, arr):  # 匹配
            click(op[i])  # 点他
    click(**CON['answer_9'])  # 点他
print('')
