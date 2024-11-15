from abc import ABC, abstractmethod
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

class RegressorABC(ABC):
    @abstractmethod
    def fit(self, X, y):
        pass

    @abstractmethod
    def predict(self, X):
        pass

class KernelRegressor(RegressorABC):
    def __init__(self):
        self.X_train = None
        self.y_train = None

    def fit(self, X, y):
        self.X_train = np.asarray(X)
        self.y_train = np.asarray(y)

    def epanechnikov_kernel(self, u):
        return (3/4) * (1 - u**2) * (np.abs(u) <= 1)

    def predict(self, X):
        X = np.asarray(X)
        n_samples = X.shape[0]
        predictions = np.zeros(n_samples)

        for i, x in enumerate(X):
            # Compute distances from x to all points in the training set
            distances = np.abs(self.X_train - x)
            # Determine k for adaptive bandwidth
            k = np.argsort(distances)[1]  # choose the second closest point
            adaptive_bandwidth = distances[k]

            # Evaluate kernel weights
            weights = self.epanechnikov_kernel(distances / adaptive_bandwidth)
            weights /= np.sum(weights)  # Normalize weights

            # Compute the prediction
            predictions[i] = np.sum(weights * self.y_train)

        return predictions

class LeastSquaresRegressor(RegressorABC):
    def __init__(self):
        self.model = LinearRegression()

    def fit(self, X, y):
        self.model.fit(X.reshape(-1, 1), y)

    def predict(self, X):
        return self.model.predict(X.reshape(-1, 1))

# Пример использования
def main():
    # Сгенерируем данные
    np.random.seed(42)
    X_train = np.sort(np.random.rand(100))
    y_train = np.sin(2 * np.pi * X_train) + np.random.normal(0, 0.1, X_train.shape)

    # Создаем экземпляры регрессоров
    kernel_regressor = KernelRegressor()
    least_squares_regressor = LeastSquaresRegressor()

    # Обучаем регрессоры
    kernel_regressor.fit(X_train, y_train)
    least_squares_regressor.fit(X_train, y_train)

    # Подготавливаем данные для предсказания
    X_test = np.linspace(0, 1, 100)

    # Получаем предсказания
    y_kernel_pred = kernel_regressor.predict(X_test)
    y_ls_pred = least_squares_regressor.predict(X_test)

    # Визуализируем результаты
    plt.figure(figsize=(12, 6))
    plt.scatter(X_train, y_train, color='gray', label='Training Data')
    plt.plot(X_test, y_kernel_pred, color='blue', label='Kernel Regression', linewidth=2)
    plt.plot(X_test, y_ls_pred, color='red', label='Least Squares Regression', linewidth=2, linestyle='--')
    plt.title('Regression Comparison')
    plt.xlabel('X')
    plt.ylabel('y')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    main()