#coding=utf-8

import sys
from HTMLParser import HTMLParser

class ParseText(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.ignore_flag = 1
        self.text_list = []

    def handle_starttag(self, tag, attrs):
        if tag == 'script' or tag == 'style':
            self.ignore_flag = 0
    
    def handle_endtag(self, tag):
        if tag == 'script' or tag == 'style':
            self.ignore_flag = 1
        
    def handle_data(self, data):
        if self.ignore_flag:
            if data.strip():
                self.text_list.append(data.strip())

    def clear_data(self):
        self.text_list = []

    def show_text(self):
        print '\n'.join(self.text_list)

    def get_text(self):
        return ' '.join(self.text_list)
    
    def parse_line(self, line):
        self.feed(line)
        return self.get_text()

if __name__ == "__main__":
    pt = ParseText()

    with open('/Users/Siwei/Documents/webpage content extraction/source/Hamshahri/100.html') as f:
        page = [x.decode('utf-8') for x in f.readlines()]

    for p in page:
        pt.feed(p)
        print pt.get_text()
        pt.clear_data()
    
    # pt = ParseText()    
    # if len(sys.argv) == 2:
    #     print pt.parse_line(sys.argv[1])
    # else:
    #     print pt.parse_line('<div class="news-lead">اللهمّ وَفّقْنی فیهِ لِموافَقَةِ الأبْرارِ و جَنّبْنی فیهِ مُرافَقَهِ الأشْرارِ و آوِنی فیهِ بِرَحْمَتِکَ الى دارِالقَرارِ بالهِیّتَکِ یا إلَهَ العالَ</div>')
        
