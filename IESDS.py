from random import randrange as rand

_min = -5
_max = 7+1

row_constraints = [2,6]
# col_constraints = [2,6]

class Entry:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'

class PayoffMatrix:
    def __init__(self, rows, cols, entry, i, j):
        self.m = [[None for ii in range(cols)] for jj in range(rows)]
        self.m[i][j] = entry
        self.rows, self.cols = rows, cols
        self.moves = [entry]

    def row(self, i):
        return self.m[i]

    def col(self, j):
        return [self.m[i][j] for i in range(self.rows)]

    def __str__(self):
        rowstr = ''
        for i in range(self.rows):
            for j in range(self.cols):
                if self.m[i][j] == None:
                    rowstr += ' ' + '  .   '
                else:
                    rowstr += ' ' + str(self.m[i][j])
            rowstr += '\n'
        return rowstr

    def nonempty(self, vector):
        for i in range(len(vector)):
            if vector[i]!= None:
                return True
        return False

    def rand_from_list(self, nums):
        return nums[rand(len(nums))]

    def grow_by_row(self):
        nonempty_rows = [i for i in range(self.rows) if self.nonempty(self.m[i])]
        empty_rows = [i for i in range(self.rows) if i not in nonempty_rows]
        dominating_index = self.rand_from_list(nonempty_rows)
        dominated_index = self.rand_from_list(empty_rows)

        for j in range(self.cols):
            if self.m[dominating_index][j] != None:
                if _min >= self.m[dominating_index][j].x:
                    p1 = self.m[dominating_index][j].x-1
                else:
                    p1 = rand(_min, self.m[dominating_index][j].x)
                p2 = rand(_min+1, _max)
                self.m[dominated_index][j] = Entry(p1, p2)

        self.moves.append( ['row', dominated_index, dominating_index] )
        return dominated_index

    def grow_by_col(self):
        nonempty_cols = [j for j in range(self.cols) if self.nonempty(self.col(j))]
        empty_cols = [j for j in range(self.cols) if j not in nonempty_cols]
        dominating_index = self.rand_from_list(nonempty_cols)
        dominated_index = self.rand_from_list(empty_cols)

        for i in range(self.rows):
            if self.m[i][dominating_index] != None:
                if _min >= self.m[i][dominating_index].y:
                    p2 = self.m[i][dominating_index].y-1
                else:
                    p2 = rand(_min, self.m[i][dominating_index].y)
                p1 = rand(_min+1, _max)
                self.m[i][dominated_index] = Entry(p1, p2)

        self.moves.append( ['col', dominated_index, dominating_index])
        return dominated_index

    def build_matrix(self):
        empty_rows = [i for i in range(self.rows) if not self.nonempty(self.m[i])]
        empty_cols = [j for j in range(self.cols) if not self.nonempty(self.col(j))]
        rows = len(empty_rows)
        cols = len(empty_cols)

        while rows + cols > 0:
            r = rand(rows + cols)
            if r < rows:
                i = self.grow_by_row()
                empty_rows.pop( empty_rows.index(i) )
            else:
                j = self.grow_by_col()
                empty_cols.pop( empty_cols.index(j) )
            rows = len(empty_rows)
            cols = len(empty_cols)

    def print_solution(self):
        s = []
        for m in self.moves[:0:-1]:
            if m[0] == 'row':
                s.append( 'Eliminate row ' + str(m[1]+1) + ', since it is dominated by row ' + str(m[2]+1) + '.'  )
            else:
                s.append( 'Eliminate column ' + str(m[1]+1) + ', since it is dominated by column ' + str(m[2]+1) + '.'  )
        s.append('We arrive at the optimal outcome ' + str(self.moves[0]))
        return s

    def generate_table_latex(self):
        string = r"""\begin{table}[]
\centering
\begin{tabular}{"""
        string += "|l" * self.cols + "|}\n\hline"
        for row in self.m:
            for entry in row[:-1]:
                string += str(entry.x) + ',' + str(entry.y) + ' & '
            string += str(row[-1].x) + ',' + str(row[-1].y) + r"\\ \hline" + "\n"
        string += r"\end{tabular}" + "\n" + r"\end{table}"
        return string

    def generate_solution_latex(self):
        s = []
        s.append(r'\subsubsection*{Steps}')
        s.append(r'\begin{enumerate}')
        for m in self.moves[:0:-1]:
            if m[0] == 'row':
                s.append( '\item Eliminate row $' + str(m[1]+1) + '$, since it is dominated by row $' + str(m[2]+1) + '$.'  )
            else:
                s.append( '\item Eliminate column $' + str(m[1]+1) + '$, since it is dominated by column $' + str(m[2]+1) + '$.'  )
        s.append(r'\end{enumerate}')
        s.append('We arrive at the optimal outcome $' + str(self.moves[0]) + '$.')
        return ('\n').join(s)

    def generate_latex_snippet(self):

        s = self.generate_table_latex() + self.generate_solution_latex()
        return s

m = []
for i in range(1):
    rows = rand(row_constraints[0], row_constraints[1])
    cols = rand(max(2, rows-1), min(5, rows+1))
    # rows = cols = 10
    I = rand(rows)
    J = rand(cols)
    m.append( PayoffMatrix(rows, cols, Entry(rand(_min, _max), rand(_min, _max)), I, J) )
    m[i].build_matrix()
    m[i].solution()
    # print m[i].rows, 'x', m[i].cols, ':', m[i].moves[0]

print '\nBult', i+1, 'problems.'
problems = ''
solutions = ''
header = '\documentclass{article} \n \\begin{document}'
footer = '\end{document}'

problems += header
solutions += header

for x in m:
    problems += x.generate_table_latex() + '\n\n'
    solutions += x.generate_latex_snippet() + '\n\\newpage\n'
problems += footer
solutions += footer

with open('problems.tex', 'wb') as file:
    file.write(problems)
with open('solutions.tex', 'wb') as file:
    file.write(solutions)

print 'Generated LaTeX for problem and solution documents.\n'
