import sys
import copy
import random
# import pprint
from collections import Counter

def load_data(filename):
    f = open(filename, "r")
    data = []
    for line in f:
        tmp = line.split()
        if len(tmp) != 0:
            data.append(tmp)
    return data
    
def gini_index(data):
    # calculate gini of one value
    total = data[1][0]
    values = data[1][1].values()
    res = 1.0
    for v in values:
        res -= (1.0 * v/total)**2
    return res
    
def best_gini_index(data, attr):
    # create a table [index, value] => [cnt, cnt of each outcome]
    table = {}
    for i in data:
        for j in i[1:]:
            if j not in table:
                table[j] = [1,{i[0]:1}]
            else:
                table[j][0] += 1
                if i[0] not in table[j][1]:
                    table[j][1][i[0]] = 1
                else:
                    table[j][1][i[0]] += 1

    counter = [(i.split(":"), j) for i,j in table.items()]
    
    # loop over each attribute, select the one with min gini index    
    min_gini = sys.maxint
    best_split = -1
    for i in attr:
        gini = 0.0
        for j in [m for m in counter if m[0][0] == i]:
            gini += 1.0 * j[1][0]/len(data) * gini_index(j)
        if gini < min_gini:
            min_gini = gini
            best_split = i
      
    # get the pssible outcome of the best split point      
    outcome = []
    for i in counter:
        if i[0][0] == best_split:
            outcome.append(i[0][1])          
    return best_split, list(set(outcome))
    
def build_tree(data, attr):
    node = {}
    
    # if all tuple are in the same class, return
    if len(set([i[0] for i in data])) == 1:
        node["leaf"] = data[0][0]
        return node
        
    # if attribute list empty, return majority class
    if len(attr) == 0:
        node["leaf"] = Counter([i[0] for i in data]).most_common(1)[0][0]
        return node
    
    # find best splitting criterion and delete the attribute
    best_split, outcome = best_gini_index(data, attr)
    tmp_attr = copy.deepcopy(attr)
    tmp_attr.remove(best_split)
    
    # loop over outcome, grow the tree
    for i in outcome:
        d = [j for j in data if j[int(best_split)] == best_split+":"+i]
        # print d
        if len(d) == 0:
            node["leaf"] = Counter([i[0] for i in data]).most_common(1)[0][0]
        else:
            node[best_split+":"+i] = build_tree(d, tmp_attr)
    return node

def train_decision_tree(data):
    attr = [i.split(":")[0] for i in data[0][1:]]
    tree = build_tree(data, attr)
    # pprint.pprint(tree)
    return tree

def test_decision_tree(data, tree):
    cur = tree
    labels = []
    candidate = list(set([i[0] for i in data]))
    output = {}
    for i in data:
        while True:
            if "leaf" in cur:
                labels.append(cur["leaf"])
                break
            union = set(i[1:]) & set(cur.keys())
            if len(union) == 0 and len(cur) != 0:
                cur = cur[random.choice(cur.keys())]
                # cur = cur[max(cur.items(), key = lambda x: len(x[1]))[0]]
            else:
                cur = cur[list(union)[0]]
        cur = tree
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
    tree = train_decision_tree(load_data(train_file))
    test_decision_tree(load_data(test_file), tree)
    
if __name__ == "__main__":
    main(sys.argv)