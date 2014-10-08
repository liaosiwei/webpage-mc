#coding=utf-8

import sys
import matplotlib.pyplot as plt
import chardet
#import numpy as np

class BaseMCE(object):
    """A base class for main content extraction"""
    def __init__(self):
        self.html = []
        self.data = []
        self.text = []
        self.smooth_data = []
        self.gap = 8
        self.mc = ""

    def clear(self):
        self.html = []
        self.data = []
        self.text = []
        self.smooth_data = []
        self.gap = 8
        self.mc = u""

    def set_gap(self, gap):
        self.gap = gap

    def get_gap(self):
        return self.gap
    
    def read_html(self, file_path):
        with open(file_path) as f:
            temp_list = f.readlines()
            coding = chardet.detect(''.join(temp_list))
            self.html = [x.decode(coding["encoding"]) for x in temp_list]
            
    def is_ascii(self, uchar):
        if uchar <= u'\u007a':
            return True
        else:
            return False

    def is_htmltag(self, uchar):
        if (uchar >= u'\u0061' and uchar <= u'\u007a') or \
           (uchar == u'\u002f') or \
           (uchar == u'\u003c') or \
           (uchar == u'\u003e'):
            return True
        else:
            return False
    

    def preprocess(self):
        """将html中的css和script以及注释代码过滤掉"""
        flag = 0
        for sline in self.html:
            if sline.startswith(u"<style") or sline.startswith(u"<script") or \
               sline.startswith(u"<!--"):
                flag = 1
            if flag == 1:
                if sline.endswith(u"</style>") or sline.endswith(u"</script>") or \
                   sline.endswith(u"-->"):
                    flag = 0
                continue
            if sline.strip():
                yield sline

    def parse_line(self, line):
        """输入一行字符串，输出英文字符集的个数和非英文字符集的个数"""
        ascii_num = 0
        non_ascii_num = 0
        text_str = u''
        for uchar in line:
            if self.is_htmltag(uchar):
                ascii_num += 1
            else:
                non_ascii_num += 1
                text_str += uchar
        return (ascii_num, non_ascii_num, text_str)


    def parse_html(self):
        for line in self.preprocess():
            res = self.parse_line(line)
            self.data.append(res[0:2])
            self.text.append(res[2])
    
    def smooth(self):
        """对统计数据进行平滑处理"""
        def minus(d):
            return d[1] - d[0]
            
        self.smooth_data.append(minus(self.data[0]))
        for i in range(1, len(self.data)-1):
            self.smooth_data.append(minus(self.data[i-1]) + minus(self.data[i]) + 
                               minus(self.data[i+1]))
        self.smooth_data.append(minus(self.data[-1]))

    def choose_mc(self):
        """确定所选取的main content的范围"""
        max_index = -1
        max_value = 0

        length = len(self.smooth_data)
        for i in range(length):
            if self.smooth_data[i] > max_value:
                max_value = self.smooth_data[i]
                max_index = i
        if max_value == 0:
            return self.mc

        self.mc += self.text[max_index] + '\n'
        k = 1
        index = max_index
        while k <= self.gap:
            if (index - k) >= 0:
                if self.smooth_data[index-k] > 0:
                    self.mc = self.text[index-k] + '\n' + self.mc
                    index = index - k;
                    k = 1
                else:
                    k += 1
            else:
                break
        k = 1
        index = max_index
        while k <= self.gap:
            if (index + k) < length:
                if self.smooth_data[index+k] > 0:
                    self.mc += self.text[index+k] + '\n'
                    index += k
                    k = 1
                else:
                    k += 1
            else:
                break
        return self.mc

    def show_img(self):
        x = range(1, len(self.data)+1)
        scale = max([y for y in self.smooth_data]) + 20
        plt.ylim([-scale, scale])
        plt.bar(x, self.smooth_data)
        plt.show()
    
    def debug_text(self):
        for i in range(len(self.text)):
            if self.smooth_data[i] > 0:
                print ("%d: %s" % (i+1, data[1][i].encode('utf-8')))

    def get_mc(self):
        return self.mc.encode('utf-8')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = '/Users/Siwei/Documents/webpage content extraction/source/BBC Arabic/100.html'
    mce = BaseMCE()
    mce.read_html(file_path)
    mce.parse_html()
    mce.smooth()
    mce.choose_mc()
    print mce.get_mc()

