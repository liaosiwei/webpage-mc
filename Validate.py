#coding=utf-8

import sys
import os
from NanagMCE import NanagMCE

def lcs(a, b):
    lengths = [[0 for j in range(len(b)+1)] for i in range(len(a)+1)]
    # row 0 and column 0 are initialized to 0 already
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            if x == y:
                lengths[i+1][j+1] = lengths[i][j] + 1
            else:
                lengths[i+1][j+1] = \
                    max(lengths[i+1][j], lengths[i][j+1])
    # read the substring out from the matrix
    result = ""
    x, y = len(a), len(b)
    while x != 0 and y != 0:
        if lengths[x][y] == lengths[x-1][y]:
            x -= 1
        elif lengths[x][y] == lengths[x][y-1]:
            y -= 1
        else:
            assert a[x-1] == b[y-1]
            result = a[x-1] + result
            x -= 1
            y -= 1
    return result

def f1_score(str1, str2):
    def f1_inner(g, m, k):
        """g: word count of gold standard files
           m: word count of cleaned files
           k: common word count
        """
        k = k + 0.
        recall = k / g
        precision = k / m
        f1 = 2 * recall * precision / (recall + precision)
        return f1
    s1 = ''.join(str1.split())
    s2 = ''.join(str2.split())
    return f1_inner(len(s1), len(s2), len(lcs(s1, s2)))

def main(source_dir, gold_dir):
    sum = 0.0
    num = 0
    mc_extractor = NanagMCE()
    
    for root, dirs, files in os.walk(source_dir):
        for f in files:
            if f.endswith("html"):
                file_path = os.path.join(root, f)
                gold_file = os.path.join(gold_dir, f.rstrip('html') + 'txt')

                mc = mc_extractor.feed(file_path)
                try:
                    with open(gold_file) as f2:
                        str2 = f2.read()
                except Exception as e:
                    continue
                temp = f1_score(mc, str2)
                sum += temp
                num += 1
                print "%d: %f" % (num, temp)
    average = sum / num
    return average
        
    

if __name__ == '__main__':
    if len(sys.argv) == 3:
        print main(sys.argv[1], sys.argv[2])
    else:
        print "python %s source_dir gold_dir" % sys.argv[0]
