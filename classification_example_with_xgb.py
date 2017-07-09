import pandas as pd
import xgboost as xgb
from sklearn import preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import LabelEncoder
import matplotlib
import matplotlib.pyplot as plt

num_round = 400 # number of rounds
data = pd.read_csv('/path/to/data.csv')
Y = df.pop('my response variable').astype(int)

param = {
    'booster': 'gbtree',
    'min_child_weight': 16,
    'gamma': 1,
    'objective' : 'multi:softmax',
    'eta': 0.05,
    'max_depth': 4,
    'silent': 0,
    'nthread': 4,
    'num_class': len(Y.unique()),
    'seed': 42,
    'lambda': 4,
    'alpha': 2,
    'subsample': 0.9
}

label_encoder = preprocessing.LabelEncoder()
label_encoder.fit(Y)
Y_num = label_encoder.transform(Y)

X_train, X_test, Y_train, Y_test = train_test_split(data, Y_num, test_size = 0.25, random_state=42, stratify=Y_num)

xg_train = xgb.DMatrix(X_train, label=Y_train)
xg_test = xgb.DMatrix(X_test, label=Y_test)
watchlist = [ (xg_train,'train'), (xg_test, 'test') ]

bst = xgb.train(param, xg_train, num_round, watchlist, early_stopping_rounds=80)
pred = bst.predict(xg_test)

cm = confusion_matrix(Y_test, pred)
print(cm)