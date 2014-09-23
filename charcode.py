#coding=utf-8

import sys
import numpy as np
import matplotlib.pyplot as plt

def is_chinese(uchar):
    """判断一个unicode是否是汉字"""
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def is_alphabet(uchar):
    """判断一个unicode是否是英文字母"""
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

def is_ascii(uchar):
    if uchar <= u'\u007a':
        return True
    else:
        return False

def parse_line(line, parse_func):
    """输入一行字符串，输出英文字符集的个数和非英文字符集的个数"""
    ascii_num = 0
    non_ascii_num = 0
    for uchar in line:
        if parse_func(uchar):
            ascii_num += 1
        else:
            non_ascii_num += 1
    return (ascii_num, non_ascii_num)

def parse_html(page, parse_func):
    """输入一个网页，输出每一行英文和非英文个数的元组列表"""
    data_list = []
    txt_list = []
    flag = 0
    for line in page:
        """将html中的css和script代码过滤掉"""
        sline = line.strip()
        if sline.startswith(u"<style") or sline.startswith(u"<script") or \
           sline.startswith(u"<!--"):
            flag = 1
        if flag == 1:
            if sline.endswith(u"</style>") or sline.endswith(u"</script>") or \
               sline.endswith(u"-->"):
                flag = 0
            continue
        data_list.append(parse_line(line, is_ascii))
    return data_list

def main(file_path=""):
    res = None
    if not file_path:
        return res
    with open(file_path) as f:
        res = parse_html((x.decode('utf-8') for x in f.readlines()), is_ascii)
    return res

def test_show():
    datalist = main('/Users/Siwei/Documents/webpage content extraction/Source Wiki All Without WebDisk/Ahram/101.html')
    r2lData = [y for x, y in datalist]
    engData = [-x for x, y in datalist]
    x = np.arange(1, len(r2lData) + 1)
    yMax = max(r2lData) + 10
    plt.xlim([0, len(x)+10])
    plt.ylim([-yMax, yMax])
    plt.plot(x, r2lData)
    plt.plot(x, engData)
    plt.show()

if __name__ == "__main__":
    test_show()
