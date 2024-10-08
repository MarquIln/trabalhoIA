from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.tree import DecisionTreeClassifier
import numpy as np
from utils import encode_board, load_data, evaluate_model, print_evaluation_results

app = Flask(__name__)
CORS(app)

def train_model(X_train, y_train):
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    return model

train_file_path = 'datasets/dataSetTreino.csv'
validation_file_path = 'datasets/DataSetValidacao.csv'
test_file_path = 'datasets/dataSetTeste.csv'

X_train, y_train = load_data(train_file_path)
X_val, y_val = load_data(validation_file_path)
X_test, y_test = load_data(test_file_path)

decision_tree = train_model(X_train, y_train)

val_accuracy, val_precision, val_recall, val_f1 = evaluate_model(y_val, decision_tree.predict(X_val))
print_evaluation_results("Validação", val_accuracy, val_precision, val_recall, val_f1)

test_accuracy, test_precision, test_recall, test_f1 = evaluate_model(y_test, decision_tree.predict(X_test))
print_evaluation_results("Teste", test_accuracy, test_precision, test_recall, test_f1)

@app.route('/check_winner', methods=['POST'])
def predict_winner():
    data = request.json
    board = data.get('board', [])

    if len(board) != 9:
        return jsonify({'error': 'O tabuleiro deve conter 9 posições'}), 400

    if '' in board:
        result = 'Em andamento'
    else:
        encoded_board = np.array([encode_board(board)])
        prediction = decision_tree.predict(encoded_board)[0]

        if prediction == 1:
            result = 'X venceu'
        elif prediction == -1:
            result = 'O venceu'
        else:
            result = 'Empate'
    
    return jsonify({'winner': result})

if __name__ == '__main__':
    app.run(debug=True)
