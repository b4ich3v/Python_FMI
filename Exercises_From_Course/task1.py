class NDimMatrix:
    def __init__(self, dimensions):
        if any(dim < 0 for dim in dimensions):
            raise ValueError("Error: Negative dimensions are not allowed.")
        
        self.dimensions = dimensions
        self.matrix = self._initialize_matrix(dimensions)

    def _initialize_matrix(self, dimensions):
        if len(dimensions) == 1:
            return [0] * dimensions[0]
        
        matrix = []
        for _ in range(dimensions[0]):
            matrix.append(self._initialize_matrix(dimensions[1:]))
        return matrix

    def __getitem__(self, index):
        if isinstance(index, tuple):
            return self._get_recursive(self.matrix, index)
        else:
            raise TypeError("Index must be a tuple.")

    def _get_recursive(self, matrix, index):
        if len(index) == 1:
            return matrix[index[0]]
        else:
            return self._get_recursive(matrix[index[0]], index[1:])
    
    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            self._set_recursive(self.matrix, index, value)
        else:
            raise TypeError("Index must be a tuple.")

    def _set_recursive(self, matrix, index, value):
        if len(index) == 1:
            matrix[index[0]] = value
        else:
            self._set_recursive(matrix[index[0]], index[1:], value)

    def __repr__(self):
        return self._repr_recursive(self.matrix)

    def _repr_recursive(self, matrix):
        if isinstance(matrix[0], list):
            return '[' + ',\n '.join(self._repr_recursive(m) for m in matrix) + ']'
        else:
            return ' '.join(map(str, matrix))
    
    def _slice(self, matrix, start, end):
        if len(start) == 1:
            return matrix[start[0]:end[0]]
        
        result = []
        for i in range(start[0], end[0]):
            result.append(self._slice(matrix[i], start[1:], end[1:]))
        return result

    def slice(self, start, end):
        if len(start) != len(end):
            raise ValueError("Start and end indices must have the same length.")
        return self._slice(self.matrix, start, end)

