from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
from utils import encode_board, load_data
from models.decision_tree import DecisionTreeModel
from models.knn import KNNModel
from models.mlp import MLPModel
# Aplicação em Flask
app = Flask(__name__)
CORS(app, resources={r"/check_winner": {"origins": "*"}})


base_dir = os.path.dirname(os.path.abspath(__file__))
train_file_path = os.path.join(base_dir, 'datasets', 'dataSetTreino.csv')
validation_file_path = os.path.join(base_dir, 'datasets', 'DataSetValidacao.csv')
test_file_path = os.path.join(base_dir, 'datasets', 'dataSetTeste.csv')

X_train, y_train = load_data(train_file_path)
X_val, y_val = load_data(validation_file_path)
X_test, y_test = load_data(test_file_path)

decision_tree_model = DecisionTreeModel()
decision_tree_model.train(X_train, y_train)
decision_tree_model.evaluate(X_val, y_val)

knn_model = KNNModel(n_neighbors=8)
knn_model.train(X_train, y_train)
knn_model.evaluate(X_val, y_val)

mlp_model = MLPModel(hidden_layer_sizes=(5,), max_iter=600)
mlp_model.train(X_train, y_train)
mlp_model.evaluate(X_val, y_val)

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
        prediction = decision_tree_model.predict(encoded_board)[0]

        if prediction == 1:
            result = 'X venceu'
        elif prediction == -1:
            result = 'O venceu'
        else:
            result = 'Empate'

    return jsonify({'winner': result, 'game_status': result})


if __name__ == '__main__':
    app.run(debug=True)
