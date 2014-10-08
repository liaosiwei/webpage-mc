#coding=utf-8

import sys

from BaseMce import BaseMCE
from HtmlParser import ParseText

class NanagMCE(BaseMCE):
    """main content extraction using Nanag algorithm"""
    def __init__(self):
        BaseMCE.__init__(self)
        self.pt = ParseText()
        self.debug = 0

    def clear(self):
        BaseMCE.clear(self)
        self.pt.reset()

    def preprocess(self):
        return self.html

    def parse_line(self, line):
        ascii_num = 0
        non_ascii_num = 0
        text = u''

        self.pt.feed(line)
        text = self.pt.get_text()
        self.pt.clear_data()
        non_ascii_num = len(text)
        ascii_num = len(line) - non_ascii_num
        if self.debug:
            print ("***********************************************")
            print "in: %s" % line
            print "out: %s" % text
            print ("%d: %d %s" % (ascii_num, non_ascii_num, text))
            print ("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=")
        return (ascii_num, non_ascii_num, text)

    def set_debug(self):
        self.debug = 1

    def feed(self, file_path):
        self.clear()
        self.set_gap(8)
        self.read_html(file_path)
        self.parse_html()
        self.smooth()
        self.choose_mc()
        return self.mc.encode('utf-8')

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = '/Users/Siwei/Documents/webpage content extraction/source/Hamshahri/100.html'
    mce = NanagMCE()
    # mce.set_debug()
    # mce.read_html(file_path)
    # mce.parse_html()
    # mce.smooth()
    # mce.choose_mc()
    # print mce.get_mc()
    # #mce.show_img()
    # mce.set_debug()
    print mce.feed(file_path)
