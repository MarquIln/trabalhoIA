import pandas as pd
from sklearn.model_selection import train_test_split

def normalize_dataset(df):
  
    return df 

def divide_datasets(X, y):
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.2, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42)
    return X_train, X_val, X_test, y_train, y_val, y_test

columns = ['top-left', 'top-middle', 'top-right', 'middle-left', 'middle-middle', 'middle-right', 
           'bottom-left', 'bottom-middle', 'bottom-right', 'class']

df = pd.read_csv('tic-tac-toe.data', header=None, names=columns)

print("distribuição original:")
print(df['class'].value_counts())

dfPositive = df[df['class'] == 'positive'].sample(332)
dfNegative = df[df['class'] == 'negative']

dfBalanceado = pd.concat([dfPositive, dfNegative]).sample(frac=1).reset_index(drop=True)

print("distribuição balanceada:")
print(dfBalanceado['class'].value_counts())

dfBalanceado.to_csv('dataset_balanceado.csv', index=False)
