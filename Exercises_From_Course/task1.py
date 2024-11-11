class Matrix:
    def __init__(self, rows, cols):
        if rows < 0 or cols < 0:
            raise ValueError("Error: Negative dimensions are not allowed.")
        
        self.matrix = []  

        for i in range(rows):
            current = []
            for j in range(cols):
                current.append(0)
            self.matrix.append(current)

    def __getitem__(self, index):
        if isinstance(index, tuple):
            row, col = index
            return self.matrix[row][col]
        else:
            return self.matrix[index]

    def __setitem__(self, index, value):
        if isinstance(index, tuple):
            row, col = index
            self.matrix[row][col] = value
        else:
            self.matrix[index] = value

    def __repr__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.matrix])

    def _slice(self, matrix, start, end):
        dimensions = len(start)

        if dimensions == 1:
            return matrix[start[0]:end[0]]

        result = []
        
        for i in range(start[0], end[0]):
            result.append(self._slice(matrix[i], start[1:], end[1:]))
        return result
