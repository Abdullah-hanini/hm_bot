import numpy as np

def create_array(numbers):
    return np.array(numbers)

def array_stats(arr):
    mean = np.mean(arr)
    median = np.median(arr)
    std_dev = np.std(arr)
    return mean, median, std_dev

def reshape_array(arr, shape):
    return np.reshape(arr, shape)

def slice_array(arr, start, end, step):
    return arr[start:end:step]

def matrix_multiplication(matrix1, matrix2):
    return np.dot(matrix1, matrix2)

def transpose_matrix(matrix):
    return np.transpose(matrix)

def inverse_matrix(matrix):
    try:
        inv_matrix = np.linalg.inv(matrix)
        return inv_matrix
    except np.linalg.LinAlgError:
        print("Error: Matrix is not invertible.")
        return None

def solve_linear_equations(coefficients, constants):
    return np.linalg.solve(coefficients, constants)

