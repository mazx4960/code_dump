import numpy as np
import logging


class MatLab:
    def __init__(self):
        pass

    def rref(self, matrix):
        """
        Returns a copy of the original matrix in reduced row echelon form
        :param matrix: numpy array
        :return: numpy array
        """

        solved = matrix.tolist()
        rows, cols = solved.shape()

        # Arrange the rows so that they are sorted in terms of their leading entries
        def leading_non_zero(row):
            return next((index for index, value in enumerate(row) if value != 0), cols )

        solved.sort(key=leading_non_zero, reverse=False)
        solved = np.array(solved)

        return solved

    def get_basis(self):
        pass

    def get_dimension(self):
        pass

    def extend_basis(self):
        pass


def main():
    logging.basicConfig(format='[*] %(message)s', level=logging.DEBUG)
    a = np.array([[0, 0, 1], [0, 2, 0], [0, 0, 0]])
    print(MatLab().rref(a))


if __name__ == '__main__':
    main()
