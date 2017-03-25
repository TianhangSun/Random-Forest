import sys
import math
import random
# import pprint
import DecisionTree as DT
from collections import Counter

def train_random_forest(data):
    attr = [i.split(":")[0] for i in data[0][1:]]
    forest = []
    for i in range(32):
        tmp_data = random.sample(data, int(math.ceil(len(data) * 0.25)))
        tmp_attr = random.sample(attr, int(math.ceil(len(attr) * 0.75)))
        forest.append(DT.build_tree(tmp_data, tmp_attr))
    return forest
    
def test_random_forest(data, forest):
    labels = []
    candidate = list(set([i[0] for i in data]))
    output = {}
    for i in data:
        tmp_labels = []
        for t in forest:
            cur = t
            while True:
                if "leaf" in cur:
                    tmp_labels.append(cur["leaf"])
                    break
                union = set(i[1:]) & set(cur.keys())
                if len(union) == 0 and len(cur) != 0:
                    cur = cur[cur.keys()[0]]
                else:
                    cur = cur[list(union)[0]]
            cur = t
        labels.append(Counter(tmp_labels).most_common(1)[0][0])
        if i[0] not in output:
            output[i[0]] = {labels[-1]:1}
        else:
            if labels[-1] not in output[i[0]]:
                output[i[0]][labels[-1]] = 1
            else:
                output[i[0]][labels[-1]] += 1
        
    ret = []
    for i in sorted(candidate):
        tmp = []
        for j in sorted(candidate):
            if i in output and j in output[i]:
                print output[i][j],
                tmp.append(output[i][j])
            else:
                print "0",
                tmp.append("0")
        ret.append(tmp)
        print
        
    return ret

def main(argv):
    if len(argv) != 3:
        print "incorrect input format"
        return
    
    train_file = argv[1]
    test_file = argv[2]
    forest = train_random_forest(DT.load_data(train_file))
    test_random_forest(DT.load_data(test_file), forest)    

if __name__ == "__main__":
    main(sys.argv)