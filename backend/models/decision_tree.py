from sklearn.tree import DecisionTreeClassifier
from utils import evaluate_model, print_evaluation_results

class DecisionTreeModel:
    def __init__(self):
        self.model = DecisionTreeClassifier(random_state=42)

    def train(self, X_train, y_train):
        self.model.fit(X_train, y_train)

    def predict(self, X):
        return self.model.predict(X)

    def evaluate(self, X_val, y_val):
        y_val_pred = self.predict(X_val)
        val_accuracy, val_precision, val_recall, val_f1 = evaluate_model(y_val, y_val_pred)
        print_evaluation_results("Validação", val_accuracy, val_precision, val_recall, val_f1)
