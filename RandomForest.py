from collections import Counter
import numpy as np, pandas as pd, sys
from DecisionTrees import DecisionTree

def cl(y):
    counter = Counter(y)
    most_common = counter.most_common(1)[0][0]
    return most_common

def boot(X, y):
    n_samples = X.shape[0]
    idxs = np.random.choice(n_samples, n_samples, replace=True)
    return X[idxs], y[idxs]


class RandomForest:
    def __init__(self, n_trees=10, s_split=2, max_depth=100, n_feats=None):
        self.n_trees = n_trees
        self.s_split = s_split
        self.max_depth = max_depth
        self.n_feats = n_feats
        self.trees = []

    def fit(self, X_arr, y_arr):
        self.trees = []
        for _ in range(self.n_trees):
            tree = DecisionTree(
                s_split=self.s_split,
                max_depth=self.max_depth,
                n_feats=self.n_feats,
            )
            X_samp, y_samp = boot(X_arr, y_arr)
            tree.fit(X_samp, y_samp)
            self.trees.append(tree)

    def predict(self, X):
        tree_preds = np.array([tree.predict(X) for tree in self.trees])
        tree_preds = np.swapaxes(tree_preds, 0, 1)
        y_pred = [cl(tree_pred) for tree_pred in tree_preds]
        return np.array(y_pred)

if __name__ == "__main__":
    from sklearn.model_selection import train_test_split, KFold
    from sklearn.metrics import accuracy_score

    #Reading dataset
    dataset = sys.argv[1]

    def accuracy(y_true, y_pred):
        accuracy = np.sum(y_true == y_pred) / len(y_true)
        return accuracy

    acc = []
    if dataset == 'breast_cancer':
        #Preprocessing dataset
        cancer_dataset = pd.read_csv("./data/breast-cancer-wisconsin.data", names=["id","diagnosis","radius","texture","perimeter","area","smoothness","compactness","concavity","concave points","decision"])
        cancer_dataset["smoothness"].replace(["?"], ['0'], inplace = True)
        cancer_dataset['smoothness'] = cancer_dataset['smoothness'].astype(int)
        average = cancer_dataset["smoothness"].mean()
        cancer_dataset["smoothness"].replace(["?"], [average], inplace = True)

        cancer_dataset['diagnosis'] = cancer_dataset['diagnosis'].astype(int)
        cancer_dataset['radius'] = cancer_dataset['radius'].astype(int)
        cancer_dataset['texture'] = cancer_dataset['texture'].astype(int)
        cancer_dataset['perimeter'] = cancer_dataset['perimeter'].astype(int)
        cancer_dataset['area'] = cancer_dataset['area'].astype(int)
        cancer_dataset['smoothness'] = cancer_dataset['smoothness'].astype(int)
        cancer_dataset['compactness'] = cancer_dataset['compactness'].astype(int)
        cancer_dataset['concavity'] = cancer_dataset['concavity'].astype(int)
        cancer_dataset['concave points'] = cancer_dataset['concave points'].astype(int)
        cancer_dataset['decision'] = cancer_dataset['decision'].astype(int)

        for i in range(10):
            #Shuffle the dataset
            cancer_dataset = cancer_dataset.sample(frac=1)
            
            model = RandomForest(n_trees=20, max_depth=10)
            X = cancer_dataset.drop(["id","decision"], axis = 1)
            y = cancer_dataset.decision
            X = X.to_numpy()
            y = y.to_numpy()

            #5-fold cross validation
            kf = KFold(n_splits=5)
            for train_index , test_index in kf.split(X):
                X_train , X_test = X[train_index,:],X[test_index,:]
                y_train , y_test = y[train_index] , y[test_index]
        
                model.fit(X_train,y_train)
                pred_values = model.predict(X_test)
        
                acc.append(accuracy_score(pred_values , y_test))

    elif dataset == 'car':
        #Preprocessing dataset
        car_dataset = pd.read_csv("./data/car.data", names=["buying", "maint", "doors", "persons", "lug_boot", "safety", "decision"])
        car_dataset["buying"].replace(["vhigh", "high", "med", "low"], [3, 2, 1, 0], inplace = True)
        car_dataset["maint"].replace(["vhigh", "high", "med", "low"], [3, 2, 1, 0], inplace = True)
        car_dataset["doors"].replace(["5more"], [5], inplace = True)
        car_dataset["persons"].replace(["more"], [4], inplace = True)
        car_dataset["lug_boot"].replace(["small", "med", "big"], [0, 1, 2], inplace = True)
        car_dataset["safety"].replace(["low", "med", "high"], [0, 1, 2], inplace = True)
        car_dataset["decision"].replace(["unacc", "acc", "good", "vgood"], [1, 0, 2, 3], inplace = True)
            
        car_dataset['buying'] = car_dataset['buying'].astype(int)
        car_dataset['maint'] = car_dataset['maint'].astype(int)
        car_dataset['doors'] = car_dataset['doors'].astype(int)
        car_dataset['persons'] = car_dataset['persons'].astype(int)
        car_dataset['lug_boot'] = car_dataset['lug_boot'].astype(int)
        car_dataset['safety'] = car_dataset['safety'].astype(int)
        car_dataset['decision'] = car_dataset['decision'].astype(int)

        for i in range(10):
            #Shuffle the dataset
            car_dataset = car_dataset.sample(frac=1)
            
            X = car_dataset.drop(["decision"], axis = 1)
            y = car_dataset.decision
            X = X.to_numpy()
            y = y.to_numpy()

            #5-fold cross validation
            kf = KFold(n_splits=5)
            for train_index , test_index in kf.split(X):
                X_train , X_test = X[train_index,:],X[test_index,:]
                y_train , y_test = y[train_index] , y[test_index]
                model = RandomForest(n_trees=20, max_depth=10)
                model.fit(X_train,y_train)
                pred_values = model.predict(X_test)
        
                acc.append(accuracy_score(pred_values , y_test))
    
    elif dataset == 'ecoli':
        #Preprocessing dataset
        ecoli_dataset = pd.read_csv("./data/ecoli.data", names=["sequence names", "mcg", "gvh", "lip", "chg",
                                "aac", "alm1", "alm2", "decision"], delim_whitespace=True)    
        ecoli_dataset["decision"].replace(["cp","im","imU","imS","imL","om","omL","pp"], [0,1,2,3,4,5,6,7], inplace = True)

        ecoli_dataset['mcg'] = ecoli_dataset['mcg'].astype(float)
        ecoli_dataset['gvh'] = ecoli_dataset['gvh'].astype(float)
        ecoli_dataset['lip'] = ecoli_dataset['lip'].astype(float)
        ecoli_dataset['chg'] = ecoli_dataset['chg'].astype(float)
        ecoli_dataset['aac'] = ecoli_dataset['aac'].astype(float)
        ecoli_dataset['alm1'] = ecoli_dataset['alm1'].astype(float)
        ecoli_dataset['alm2'] = ecoli_dataset['alm2'].astype(float)
        ecoli_dataset['decision'] = ecoli_dataset['decision'].astype(int)
        
        for i in range(10):
            #Shuffle the dataset
            ecoli_dataset = ecoli_dataset.sample(frac=1)

            X = ecoli_dataset.drop(["sequence names","decision"], axis=1).to_numpy()
            y = ecoli_dataset.decision.to_numpy()

            #5-fold cross validation
            kf = KFold(n_splits=5)
            for train_index, test_index in kf.split(X):
                X_train, X_test = X[train_index, :], X[test_index, :]
                y_train, y_test = y[train_index], y[test_index]

                model = RandomForest(n_trees=20, max_depth=10)
                model.fit(X_train,y_train)
                pred_values = model.predict(X_test)
        
                acc.append(accuracy_score(pred_values , y_test))


    elif dataset == 'letter':
        #Preprocessing dataset
        letter_dataset = pd.read_csv('./data/letter-recognition.data', names=["lettr", "x-box", "y-box", "width", "high", "onpix", "x-bar", "y-bar", "x2bar", "y2bar", "xybar", "x2ybr", "xy2br", "x-ege", "xegvy", "y-ege", "yegvx"])
        ObjectColumns = letter_dataset.select_dtypes(include=np.object).columns.tolist()
        letter_dataset['lettr'] = [ord(item)-64 for item in letter_dataset['lettr']]

        for i in range(10):
            #Shuffle the dataset
            letter_dataset = letter_dataset.sample(frac=1)
            
            model = RandomForest(n_trees=20, max_depth=10)
            X = letter_dataset.drop(["lettr"], axis = 1)
            y = letter_dataset.lettr
            X = X.to_numpy()
            y = y.to_numpy()

            #5-fold cross validation
            kf = KFold(n_splits=5)
            for train_index , test_index in kf.split(X):
                X_train , X_test = X[train_index,:],X[test_index,:]
                y_train , y_test = y[train_index] , y[test_index]
        
                model.fit(X_train,y_train)
                pred_values = model.predict(X_test)
        
                acc.append(accuracy_score(pred_values , y_test))

    
    elif dataset == 'mushroom':
        #Preprocessing dataset
        mushroom_dataset = pd.read_csv("./data/mushroom.data", names=["decision", "cap-shape", "cap-surface", "cap-color", "bruises", "odor",  "gill-attachment", 
    "gill-spacing", "gill-size", "gill-color", "stalk-shape", "stalk-root", "stalk-surface-above-ring", "stalk-surface-below-ring", 
    "stalk-color-above-ring", "stalk-color-below-ring", "veil-type", "veil-color", "ring-number", "ring-type", "spore-print-color", 
    "population", "habitat"])

        mushroom_dataset.replace(['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z'],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25],inplace = True)
        
        mushroom_dataset["stalk-root"].replace(["?"], ['0'], inplace = True)
        mushroom_dataset["stalk-root"] = mushroom_dataset['stalk-root'].astype(int)
        average = mushroom_dataset["stalk-root"].mean()
        mushroom_dataset["stalk-root"].replace(["?"], [average], inplace = True)

        mushroom_dataset["decision"] = mushroom_dataset['decision'].astype(int)
        mushroom_dataset["cap-shape"] = mushroom_dataset['cap-shape'].astype(int)
        mushroom_dataset["cap-surface"] = mushroom_dataset['cap-surface'].astype(int)
        mushroom_dataset["cap-color"] = mushroom_dataset['cap-color'].astype(int)
        mushroom_dataset["bruises"] = mushroom_dataset['bruises'].astype(int)
        mushroom_dataset["odor"] = mushroom_dataset['odor'].astype(int)
        mushroom_dataset["gill-attachment"] = mushroom_dataset['gill-attachment'].astype(int)
        mushroom_dataset["gill-spacing"] = mushroom_dataset['gill-spacing'].astype(int)
        mushroom_dataset["gill-size"] = mushroom_dataset['gill-size'].astype(int)
        mushroom_dataset["gill-color"] = mushroom_dataset['gill-color'].astype(int)
        mushroom_dataset["stalk-shape"] = mushroom_dataset['stalk-shape'].astype(int)
        mushroom_dataset["stalk-surface-above-ring"] = mushroom_dataset['stalk-surface-above-ring'].astype(int)
        mushroom_dataset["stalk-surface-below-ring"] = mushroom_dataset['stalk-surface-below-ring'].astype(int)
        mushroom_dataset["stalk-color-above-ring"] = mushroom_dataset['stalk-color-above-ring'].astype(int)
        mushroom_dataset["stalk-color-below-ring"] = mushroom_dataset['stalk-color-below-ring'].astype(int)
        mushroom_dataset["veil-type"] = mushroom_dataset['veil-type'].astype(int)
        mushroom_dataset["veil-color"] = mushroom_dataset['veil-color'].astype(int)
        mushroom_dataset["ring-number"] = mushroom_dataset['ring-number'].astype(int)
        mushroom_dataset["ring-type"] = mushroom_dataset['ring-type'].astype(int)
        mushroom_dataset["spore-print-color"] = mushroom_dataset['spore-print-color'].astype(int)
        mushroom_dataset["population"] = mushroom_dataset['population'].astype(int)
        mushroom_dataset["habitat"] = mushroom_dataset['habitat'].astype(int)

        for i in range(10):
            #Shuffle the dataset
            mushroom_dataset = mushroom_dataset.sample(frac=1)
            
            model = RandomForest(trees=20, max_depth=10)
            X = mushroom_dataset.drop(["decision"], axis = 1)
            y = mushroom_dataset.decision
            X = X.to_numpy()
            y = y.to_numpy()

            #5-fold cross validation
            kf = KFold(n_splits=5)
            for train_index , test_index in kf.split(X):
                X_train , X_test = X[train_index,:],X[test_index,:]
                y_train , y_test = y[train_index] , y[test_index]
        
                model.fit(X_train,y_train)
                pred_values = model.predict(X_test)
        
                acc.append(accuracy_score(pred_values , y_test))

    std = np.std(acc)

    print('Random Forest classification accuracy %.3f%%' % ((sum(acc)/float(len(acc)))*100))
    print("Random Forest classification standard deviation", std)