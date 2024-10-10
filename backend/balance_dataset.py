import pandas as pd
import os
from sklearn.model_selection import train_test_split

def normalize_dataset(df):
    mapping = {'x': 1, 'o': -1, 'b': 0}
    df.iloc[:, :-1] = df.iloc[:, :-1].applymap(mapping.get)
    df['class'] = df['class'].map({'positive': 1, 'negative': -1})
    return df

def divide_datasets(X, y):
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    return X_train, X_val, X_test, y_train, y_val, y_test

columns = ['top-left', 'top-middle', 'top-right', 'middle-left', 'middle-middle', 'middle-right', 
           'bottom-left', 'bottom-middle', 'bottom-right', 'class']

df = pd.read_csv('tic-tac-toe.data', header=None, names=columns)

df = normalize_dataset(df)

dfPositive = df[df['class'] == 1].sample(332)
dfNegative = df[df['class'] == -1]

dfBalanceado = pd.concat([dfPositive, dfNegative]).sample(frac=1).reset_index(drop=True)

dfBalanceado.columns = ['cell_1', 'cell_2', 'cell_3', 'cell_4', 'cell_5', 'cell_6', 'cell_7', 'cell_8', 'cell_9', 'result']

dfBalanceado = dfBalanceado.sort_values(by='result', ascending=False).reset_index(drop=True)

if not os.path.exists('datasets'):
    os.makedirs('datasets')

X = dfBalanceado.iloc[:, :-1]
y = dfBalanceado['result']
X_train, X_val, X_test, y_train, y_val, y_test = divide_datasets(X, y)

X_train['result'] = y_train
X_val['result'] = y_val
X_test['result'] = y_test

X_train.to_csv('datasets/train_dataset.csv', index=False)
X_val.to_csv('datasets/validation_dataset.csv', index=False)
X_test.to_csv('datasets/test_dataset.csv', index=False)
