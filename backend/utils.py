import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

def encode_board(board):
    return [1 if cell == 'X' else -1 if cell == 'O' else 0 for cell in board]

def load_data(file_path, sep=','):
    try:
        data = pd.read_csv(file_path, sep=sep)
    except FileNotFoundError:
        raise Exception(f"Arquivo não encontrado: {file_path}")
    except pd.errors.EmptyDataError:
        raise Exception(f"O arquivo está vazio: {file_path}")
    except Exception as e:
        raise Exception(f"Erro ao carregar o arquivo: {str(e)}")

    X = data.iloc[:, :-1].values
    y = data.iloc[:, -1].values
    return X, y


def evaluate_model(y_true, y_pred):
    accuracy = accuracy_score(y_true, y_pred)
    precision = precision_score(y_true, y_pred, average='weighted')
    recall = recall_score(y_true, y_pred, average='weighted')
    f1 = f1_score(y_true, y_pred, average='weighted')
    return accuracy, precision, recall, f1

def print_evaluation_results(phase, accuracy, precision, recall, f1):
    print(f"Resultados de {phase}:")
    print(f"Acurácia: {accuracy}")
    print(f"Precisão: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-Measure: {f1}")
