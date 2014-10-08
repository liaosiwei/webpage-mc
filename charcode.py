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
    text_str = u''
    for uchar in line:
        if parse_func(uchar):
            ascii_num += 1
        else:
            non_ascii_num += 1
            text_str += uchar
    return (ascii_num, non_ascii_num, text_str)

def parse_html(page, parse_func):
    """输入一个网页，输出每一行英文和非英文个数的元组列表"""
    data_list = []
    txt_list = []
    flag = 0
    for line in page:
        """将html中的css和script以及注释代码过滤掉"""
        sline = line.strip()
        if sline.startswith(u"<style") or sline.startswith(u"<script") or \
           sline.startswith(u"<!--"):
            flag = 1
        if flag == 1:
            if sline.endswith(u"</style>") or sline.endswith(u"</script>") or \
               sline.endswith(u"-->"):
                flag = 0
            continue
        res_tuple = parse_line(line, is_ascii)
        data_list.append(res_tuple[0:2])
        txt_list.append(res_tuple[2])
    return (data_list, txt_list)

def smooth(data_list):
    """对统计数据进行平滑处理"""
    def minus(d):
        return d[1] - d[0]
        
    smooth_data = [minus(data_list[0])]
    for i in range(1, len(data_list)-1):
        smooth_data.append(minus(data_list[i-1]) + minus(data_list[i]) + minus(data_list[i+1]))
    smooth_data.append(minus(data_list[-1]))
    return smooth_data

def main(file_path=""):
    res = None
    if not file_path:
        return res
    with open(file_path) as f:
        res = parse_html((x.decode('utf-8') for x in f.readlines()), is_ascii)
    return res

def test_show():
    data = main('/Users/Siwei/Documents/webpage content extraction/Source Wiki All Without WebDisk/Ahram/100.html')
    datalist = data[0]
    # ＃print data[1]              
    # r2lData = [y for x, y in datalist]
    # engData = [-x for x, y in datalist]
    # x = np.arange(1, len(r2lData) + 1)
    # yMax = max(r2lData) + 10
    # plt.xlim([0, len(x)+10])
    # plt.ylim([-yMax, yMax])
    # plt.plot(x, r2lData)
    # plt.plot(x, engData)
    x = np.arange(1, len(datalist) + 1)
    smoothdata = smooth(datalist)
    scale = max([y for _, y in datalist])
    plt.ylim([-scale, scale])
    for i in range(len(x)):
        if smoothdata[i] > 0:
            print ("%d: %s" % (i+1, data[1][i].encode('utf-8')))
            
    plt.bar(x, smoothdata)
    plt.show()

if __name__ == "__main__":
    test_show()
