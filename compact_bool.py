"""
Written by Donald Tsang 2022 - https://github.com/rocketDonald/

This library provides a space-saving solution for storing 2D boolean array / matrix.

This solution takes the advantage of 2-fold rotational symmetric property of square,
such that only half the size is needed for storing such square matrix.

Space complexity:
    -   Split a n*n sized matrix into 4 domains ==> 1/4 space
    -   using ctypes.c_int8 to represent 16 different cases of bool value combination in 4 domains
        ==> 1 byte c_int8 representing 1 cell == representing 4 domains
    -   Recommended to use this library when the boolean matrix is large
Time complexity:
    -   The process for looking up values will still remain O(1)
    -   The process of changing values is slower than changing values in a normal matrix, but it still remains O(1)

Id for 4 Domains:
+-----+-----+
|  0  |  1  |
+-----+-----+
|  2  |  3  |
+-----+-----+

16 Different cases:
[ O = True | X = False]
Case 0:
+-----+-----+
|  X  |  X  |
+-----+-----+
|  X  |  X  |
+-----+-----+

Case 1:
+-----+-----+
|  O  |  X  |
+-----+-----+
|  X  |  X  |
+-----+-----+

Case 2:
+-----+-----+
|  X  |  O  |
+-----+-----+
|  X  |  X  |
+-----+-----+

Case 3:
+-----+-----+
|  X  |  X  |
+-----+-----+
|  O  |  X  |
+-----+-----+

Case 4:
+-----+-----+
|  X  |  X  |
+-----+-----+
|  X  |  O  |
+-----+-----+

Case 5:
+-----+-----+
|  O  |  O  |
+-----+-----+
|  X  |  X  |
+-----+-----+

Case 6:
+-----+-----+
|  O  |  X  |
+-----+-----+
|  O  |  X  |
+-----+-----+

Case 7:
+-----+-----+
|  O  |  X  |
+-----+-----+
|  X  |  O  |
+-----+-----+

Case 8:
+-----+-----+
|  X  |  O  |
+-----+-----+
|  O  |  X  |
+-----+-----+

Case 9:
+-----+-----+
|  X  |  O  |
+-----+-----+
|  X  |  O  |
+-----+-----+

Case 10:
+-----+-----+
|  X  |  X  |
+-----+-----+
|  O  |  O  |
+-----+-----+

Case 11:
+-----+-----+
|  O  |  O  |
+-----+-----+
|  O  |  X  |
+-----+-----+

Case 12:
+-----+-----+
|  O  |  O  |
+-----+-----+
|  X  |  O  |
+-----+-----+

Case 13:
+-----+-----+
|  O  |  X  |
+-----+-----+
|  O  |  O  |
+-----+-----+

Case 14:
+-----+-----+
|  X  |  O  |
+-----+-----+
|  O  |  O  |
+-----+-----+

Case 15:
+-----+-----+
|  O  |  O  |
+-----+-----+
|  O  |  O  |
+-----+-----+
"""
import sys
from ctypes import *
from math import ceil

"""
This class provides a compressed matrix for storing size*size boolean values
"""


class CompactBoolMatrix(object):
    def __init__(self, size):
        new_size = ceil(size / 2)

        # c_types structure factory
        class _MatStruct_32(Structure):
            _fields_ = [
                ("og_size", c_int32),
                ("new_size", c_int32),
                ("matrix", (c_int8 * new_size) * new_size)
            ]

        self.matrix = _MatStruct_32()
        self.matrix.og_size = size
        self.matrix.new_size = new_size

    """
    This function sets all the values in the matrix to False
    """

    def all_false(self):
        for i in range(self.matrix.new_size):
            for j in range(self.matrix.new_size):
                self.matrix.matrix[i][j] = 0

    """
    This function sets all the values in the matrix to True
    """

    def all_true(self):
        for i in range(self.matrix.new_size):
            for j in range(self.matrix.new_size):
                self.matrix.matrix[i][j] = 15

    """
    This function sets false to a cell. 
    Equals to the following syntax:
    bool_matrix[x][y] = False.
    """

    def set_false(self, x, y):
        domain = self.__get_domain(x, y)

        if domain == 0:
            val = self.__get_compact_val(x, y, domain)
            value_table = [0, 0, 2, 3,
                           4, 2, 3, 4,
                           8, 9, 10, 8,
                           9, 10, 14, 14]
            self.matrix.matrix[x][y] = value_table[val]
        elif domain == 1:
            val = self.__get_compact_val(x, y, domain)
            value_table = [0, 1, 0, 3,
                           4, 1, 6, 7,
                           3, 4, 10, 6,
                           7, 13, 10, 13]
            self.matrix.matrix[x - self.matrix.new_size][y] = value_table[val]
        elif domain == 2:
            val = self.__get_compact_val(x, y, domain)
            value_table = [0, 1, 2, 0,
                           4, 5, 1, 7,
                           2, 9, 4, 5,
                           12, 7, 9, 12]
            self.matrix.matrix[x][y - self.matrix.new_size] = value_table[val]
        else:
            val = self.__get_compact_val(x, y, domain)
            value_table = [0, 1, 2, 3,
                           0, 5, 6, 1,
                           8, 2, 3, 11,
                           5, 6, 8, 11]
            self.matrix.matrix[x - self.matrix.new_size][y - self.matrix.new_size] = value_table[val]

    """
    This function sets true to a cell. 
    Equals to the following syntax:
    bool_matrix[x][y] = True.
    """

    def set_true(self, x, y):
        domain = self.__get_domain(x, y)

        if domain == 0:
            val = self.__get_compact_val(x, y, domain)
            value_table = [1, 1, 5, 6,
                           7, 5, 6, 7,
                           11, 12, 13, 11,
                           12, 13, 15, 15]
            self.matrix.matrix[x][y] = value_table[val]
        elif domain == 1:
            val = self.__get_compact_val(x, y, domain)
            value_table = [2, 5, 2, 8,
                           9, 5, 11, 12,
                           8, 9, 14, 11,
                           12, 15, 14, 15]
            self.matrix.matrix[x - self.matrix.new_size][y] = value_table[val]
        elif domain == 2:
            val = self.__get_compact_val(x, y, domain)
            value_table = [3, 6, 8, 3,
                           10, 11, 6, 13,
                           8, 14, 10, 11,
                           15, 13, 14, 15]
            self.matrix.matrix[x][y - self.matrix.new_size] = value_table[val]
        else:
            val = self.__get_compact_val(x, y, domain)
            value_table = [4, 7, 9, 10,
                           4, 12, 13, 7,
                           14, 9, 10, 15,
                           12, 13, 14, 15]
            self.matrix.matrix[x - self.matrix.new_size][y - self.matrix.new_size] = value_table[val]


    """
    This function returns the boolean value of a cell
    Equals to the following syntax:
    a = bool_matrix[x][y]
    """
    def get(self, x, y):
        domain = self.__get_domain(x, y)
        if domain == 0:
            val = self.__get_compact_val(x, y, domain)
            truth_table = [False, True, False, False,
                           False, True, True, True,
                           False, False, False, True,
                           True, True, False, True]
            return truth_table[val]
        elif domain == 1:
            val = self.__get_compact_val(x, y, domain)
            truth_table = [False, False, True, False,
                           False, True, False, False,
                           True, True, False, True,
                           True, False, True, True]
            return truth_table[val]
        elif domain == 2:
            val = self.__get_compact_val(x, y, domain)
            truth_table = [False, False, False, True,
                           False, False, True, False,
                           True, False, True, True,
                           False, True, True, True]
            return truth_table[val]
        else:
            val = self.__get_compact_val(x, y, domain)
            truth_table = [False, False, False, False,
                           True, False, False, True,
                           False, True, True, False,
                           True, True, True, True]
            return truth_table[val]

    """
    This function sets the value of cell to the opposite boolean value
    Equals to the following syntax:
    bool_matrix[x][y] ? False : True
    """
    def switch(self, x, y):
        if self.get(x, y) is True:
            self.set_false(x, y)
        else:
            self.set_true(x, y)

    def __get_compact_val(self, x, y, domain):
        s = self.matrix.new_size

        if domain == 0:
            return self.matrix.matrix[x][y]
        elif domain == 1:
            return self.matrix.matrix[x - s][y]
        elif domain == 2:
            return self.matrix.matrix[x][y - s]
        else:
            return self.matrix.matrix[x - s][y - s]

    def __get_domain(self, x, y):
        s = self.matrix.new_size
        if x >= self.matrix.og_size or y >= self.matrix.og_size:
            raise OutOfBound

        if x < s and y < s:
            domain = 0
        elif x > s > y:
            domain = 1
        elif x < s < y:
            domain = 2
        else:
            domain = 3

        return domain

    def compact_to_normal(self):
        res = [[False for y in range(self.matrix.og_size)] for x in range(self.matrix.og_size)]

        for i in range(self.matrix.og_size):
            for j in range(self.matrix.og_size):
                res[i][j] = self.get(i, j)

        return res

    def __repr__(self):
        return "Compact Boolean Matrix Object with compressed size: " + str(self.matrix.new_size)

    def __str__(self):
        string = ''
        for i in range(self.matrix.og_size):
            for j in range(self.matrix.og_size):
                string += str(self.get(i, j)) + " "
            string += "\n"

        return string

    def __len__(self):
        return self.matrix.og_size * self.matrix.og_size

    def __eq__(self, other):
        if len(self) != len(other):
            return False

        for i in range(self.matrix.og_size):
            for j in range(self.matrix.og_size):
                if self.get(i, j) != other.get(i, j):
                    return False

        return True

    def __sizeof__(self):
        return sizeof(self.matrix)


class OutOfBound(Exception):
    pass


if __name__ == '__main__':
    # Example Code
    size = 5
    mat = CompactBoolMatrix(size)
    mat.all_false() # Init the matrix to all False
    mat.switch(2, 0)    # Switching the value from False to True
    mat.switch(2, 1)
    mat.switch(0, 2)
    mat.switch(1, 2)
    mat.switch(3, 2)
    mat.switch(4, 2)
    mat.switch(2, 2)
    mat.set_true(2, 3)
    mat.set_true(2, 4)  # Directly set the value to true
    print(mat)
    normal_mat = mat.compact_to_normal()
    print(normal_mat)

