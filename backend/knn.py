from flask import Flask, request, jsonify
from sklearn.neighbors import KNeighborsClassifier
from flask_cors import CORS
import os
import numpy as np
from utils import encode_board, load_data, evaluate_model, print_evaluation_results

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(os.path.abspath(__file__))
train_file_path = os.path.join(base_dir, 'datasets', 'dataSetTreino.csv')
validation_file_path = os.path.join(base_dir, 'datasets', 'DataSetValidacao.csv')
test_file_path = os.path.join(base_dir, 'datasets', 'dataSetTeste.csv')

X_train, y_train = load_data(train_file_path)
X_val, y_val = load_data(validation_file_path)
X_test, y_test = load_data(test_file_path)


knn = KNeighborsClassifier(n_neighbors=8)
knn.fit(X_train, y_train)

y_val_pred = knn.predict(X_val)
val_accuracy, val_precision, val_recall, val_f1 = evaluate_model(y_val, y_val_pred)
print_evaluation_results("Validação", val_accuracy, val_precision, val_recall, val_f1)

y_test_pred = knn.predict(X_test)
test_accuracy, test_precision, test_recall, test_f1 = evaluate_model(y_test, y_test_pred)
print_evaluation_results("Teste", test_accuracy, test_precision, test_recall, test_f1)

def check_tie(board):
    return all(cell != '' for cell in board)

@app.route('/check_winner', methods=['POST'])
def check_winner():
    data = request.json
    board = data.get('board', [])

    
    if len(board) != 9:
        return jsonify({'error': 'O tabuleiro deve conter 9 posições'}), 400


    if '' in board:
        result = 'Em andamento'
    else:
        encoded_board = np.array([encode_board(board)])
        prediction = knn.predict(encoded_board)[0]

        if prediction == 1:
            result = 'X venceu'
        elif prediction == -1:
            result = 'O venceu'
        else:
            result = 'Empate' if check_tie(board) else 'Em andamento'

    return jsonify({'winner': result})

if __name__ == '__main__':
    app.run(debug=True)
