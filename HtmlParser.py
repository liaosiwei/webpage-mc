#coding=utf-8

import sys
import chardet
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
            if data:
                self.text_list.append(data)

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
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
    else:
        file_path = '/Users/Siwei/Documents/webpage content extraction/source/BBC Arabic/322.html'

    def read_html(file_path):
        with open(file_path, 'r') as f:
            temp_list = [x for x in f.readlines() if x.strip()]
            coding = chardet.detect(''.join(temp_list))
            html = [x.decode(coding["encoding"]).strip('\r\n').strip() for x in temp_list]
            return html
            
    page = read_html(file_path)

    for p in page:
        pt.feed(p)
        text = pt.get_text()
        if text:
            print text.encode('utf-8')
        pt.clear_data()
    
    # pt = ParseText()    
    # if len(sys.argv) == 2:
    #     print pt.parse_line(sys.argv[1])
    # else:
    #     print pt.parse_line('<div class="news-lead">اللهمّ وَفّقْنی فیهِ لِموافَقَةِ الأبْرارِ و جَنّبْنی فیهِ مُرافَقَهِ الأشْرارِ و آوِنی فیهِ بِرَحْمَتِکَ الى دارِالقَرارِ بالهِیّتَکِ یا إلَهَ العالَ</div>')
        
