from sklearn import tree
from sklearn.ensemble import RandomForestClassifier
import DecisionTree as DT
import RandomForest as RF

def load_data(filename):
    f = open(filename, "r")
    data = []
    label = []
    for line in f:
        tmp = line.split()
        if len(tmp) != 0:
            label.append(tmp[0])
            data.append([i.split(":")[1] for i in tmp[1:]])
    return data, label

def DT_check(f1, f2):
    x1, y1 = load_data(f1)
    clf = tree.DecisionTreeClassifier()
    clf = clf.fit(x1, y1)
    x2, y2 = load_data(f2)
    print clf.score(x2, y2)
    
def RF_check(f1, f2):
    x1, y1 = load_data(f1)
    clf = RandomForestClassifier(n_estimators=32, max_features=0.75)
    clf = clf.fit(x1, y1)
    x2, y2 = load_data(f2)
    print clf.score(x2, y2)

def evaluate(data, name):
    print "\n",name,":"
    l = len(data)
    correct = 0.0
    total = 0.0
    for i in range(l):
        for j in range(l):
            if i == j:
                correct += float(data[i][j])
            total += float(data[i][j])
    print "accuracy: ", correct/total,"\n"
    for i in range(l):
        tp = float(data[i][i])
        tp_fn = sum([float(j) for j in data[i]])
        tp_fp = sum([float(j[i]) for j in data])
        if tp_fn == 0:
            print "sensitivity/recall", i+1, ": NAN"
        else:
            print "sensitivity/recall", i+1, ":", 1.0 * tp/tp_fn
        print "specificity", i+1, ":", (total-tp_fn-tp_fp+tp)/(total-tp_fn)
        if tp_fp == 0:
            print "precision", i+1, ": NAN"
        else:
            print "precision", i+1, ":", 1.0 * tp/tp_fp
        print "F1 score", i+1, ":", 2*tp/(tp_fn+tp_fp)
        print "F0.5 score", i+1, ":", 1.25*tp/(1.25*tp+0.25*(tp_fn-tp)+tp_fp-tp)
        print "F2 score", i+1, ":", 5*tp/(5*tp+4*(tp_fn-tp)+tp_fp-tp),"\n"
    print    

def main():
    print "\nDecision tree:"
    DT_check("balance-scale.train", "balance-scale.test")
    DT_check("nursery.data.train", "nursery.data.test")
    DT_check("led.train.new", "led.test.new")
    DT_check("poker.train", "poker.test")
    
    print "\nRandom Forest:"
    RF_check("balance-scale.train", "balance-scale.test")
    RF_check("nursery.data.train", "nursery.data.test")
    RF_check("led.train.new", "led.test.new")
    RF_check("poker.train", "poker.test")
    
    print    
    tree1 = DT.train_decision_tree(DT.load_data("balance-scale.train"))
    res1 = DT.test_decision_tree(DT.load_data("balance-scale.test"), tree1)
    evaluate(res1, "DT balance-scale")
    
    tree2 = DT.train_decision_tree(DT.load_data("nursery.data.train"))
    res2 = DT.test_decision_tree(DT.load_data("nursery.data.test"), tree2)
    evaluate(res2, "DT nursery")
    
    tree3 = DT.train_decision_tree(DT.load_data("led.train.new"))
    res3 = DT.test_decision_tree(DT.load_data("led.test.new"), tree3)
    evaluate(res3, "DT led")
    
    tree4 = DT.train_decision_tree(DT.load_data("poker.train"))
    res4 = DT.test_decision_tree(DT.load_data("poker.test"), tree4) 
    evaluate(res4, "DT poker")
    
    forest1 = RF.train_random_forest(DT.load_data("balance-scale.train"))
    res5 = RF.test_random_forest(DT.load_data("balance-scale.test"), forest1)
    evaluate(res5, "RF balance-scale")
    
    forest2 = RF.train_random_forest(DT.load_data("nursery.data.train"))
    res6 = RF.test_random_forest(DT.load_data("nursery.data.test"), forest2)
    evaluate(res6, "RF nursery")
    
    forest3 = RF.train_random_forest(DT.load_data("led.train.new"))
    res7 = RF.test_random_forest(DT.load_data("led.test.new"), forest3)
    evaluate(res7, "RF led")
    
    forest4 = RF.train_random_forest(DT.load_data("poker.train"))
    res8 = RF.test_random_forest(DT.load_data("poker.test"), forest4)
    evaluate(res8, "RF poker")

if __name__ == "__main__":
    main()