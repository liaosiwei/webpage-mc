#coding=utf-8

import sys
import os
import Validate

def main(source_dir, out_file):
    with open(out_file, 'w') as f:
        for root, dirs, files in os.walk(source_dir):
            for d in dirs:
                print ("processing %s" % d)
                fold_dir = os.path.join(root, d)
                gold_dir = fold_dir.replace('source', 'Golden Wiki')
                res = Validate.main(fold_dir, gold_dir)
                f.write("%s\t%f\n" % (d, res))

if __name__ == "__main__":
    if len(sys.argv) == 3:
        main(sys.argv[1], sys.argv[2])
    else:
        print "%s source_dir out_file" % sys.argv[0]
