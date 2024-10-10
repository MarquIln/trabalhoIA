from sklearn.neural_network import MLPClassifier
import numpy as np
from utils import evaluate_model, print_evaluation_results
# Modelo Multi-Layer Perceptron (MLP)
class MLPModel:
    def __init__(self, hidden_layer_sizes=(5,), max_iter=600):
        self.model = MLPClassifier(hidden_layer_sizes=hidden_layer_sizes, max_iter=max_iter)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X_val, y_val):
        y_val_pred = self.predict(X_val)
        val_accuracy, val_precision, val_recall, val_f1 = evaluate_model(y_val, y_val_pred)
        print_evaluation_results("Validação", val_accuracy, val_precision, val_recall, val_f1)
