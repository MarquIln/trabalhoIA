from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
from utils import load_data
from models.decision_tree import DecisionTreeModel
from models.knn import KNNModel
from models.mlp import MLPModel

app = Flask(__name__)
CORS(app, resources={r"/check_winner": {"origins": "http://localhost:3000"}})

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

@app.route('/check_winner', methods=['POST', 'OPTIONS'])
def check_winner():
    if request.method == 'OPTIONS':
        return jsonify({'status': 'ok'}), 200

    data = request.json
    board = data.get('board', [])

    print(f"Received board: {board}") # debug board

    if len(board) != 9:
        return jsonify({'error': 'O tabuleiro deve conter 9 posições'}), 400

    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)            
    ]

    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != "":
            return jsonify({'winner': board[a], 'game_status': 'Terminado'})

    if "" in board:
        return jsonify({'winner': '', 'game_status': 'Em andamento'})
    else:
        return jsonify({'winner': 'Empate', 'game_status': 'Terminado'})

if __name__ == '__main__':
    app.run(debug=True)
