import time
from math import ceil, log
import csv
"""
   This program serves to show the difference in runtimes between
      Naive Matrix Multiplication and Strassen's Algorithm for
      Matrix Multiplication.
   It is controlled by the 'run' function, which takes a path
      to an example file, formatted as:
      2 (order of square matrix)
      1 2 (matrix 1 line 1)
       3 4 (matrix 1 line 2)
      1 2 (matrix 2 line 1)
      3 4 (matrix 2 line 2)
      (empty line)
      2 (order of next square matrix)
   Run calls 'get_results' which times and calculates the naive
      and Strassen multiplication and reports them back.
"""

def naive_mult(a, b):
   ''' Naive matrix multiplication
    
   Runs in O(n^3) time. Not advisable to use in production
    
   Args:
      a (array): square matrix of length N
      b (array): square matrix of length N
        
   Returns:
      C (array): square matrix of length N resulting from a x b
   '''
   n = len(a)
   c = [[0] * n for _ in range(n)]
   for i in range(n):
      for j in range(n):
         for k in range(n):
               c[i][j] = c[i][j] + a[i][k] * b[k][j]
   return c

def subtract(a, b):
   ''' Subtracts two matrices 
    
   Args:
      a (matrix): an nxn array to subtract from
      b (matrix): an nxn array to subtract with
    
   Returns:
      (matrix): the matrix resulting from a - b
   '''
   return [[a[i][j] - b[i][j] for j in range(len(a))]
         for i in range(len(a))]

def add(a, b):
   ''' Adds two matrices 
    
   Args:
      a (matrix): an nxn array to add to
      b (matrix): an nxn array to add with
    
   Returns:
      (matrix): the matrix resulting from a + b'''
   return [[a[i][j] + b[i][j] for j in range(len(a))]
         for i in range(len(a))]

def strassen(a, b):
   ''' Strassen matrix multiplication
    
   Runs in O(n^(lg7)) time.
   Note on "m-block": I struggled to find an error in the method.
      2x2 multiplication worked but not 4x4. I thought it was
      something with the book definition, since I followed it.
      I checked the Strassen'S algorithm Wiki page, where they
      define S as M, so I changed that notation and did not 
      change it back to the book's. 
    
   Args:
      a (array): square matrix of length N
      a (array): square matrix of length N
        
   Returns:
      C (array): square matrix of length N resulting from a x b
   '''

   n = len(a)

   # Base case: if single elements, multiply and return
   if n == 1:
      return [[a[0][0] * b[0][0]]]
    
   # List comprehensions defining quadrants of a and b
   a11 = [[a[i][j] for j in range(n//2)] for i in range(n//2)]
   a12 = [[a[i][j] for j in range(n//2, n)] for i in range(n//2)]
   a21 = [[a[i][j] for j in range(n//2)] for i in range(n//2, n)]
   a22 = [[a[i][j] for j in range(n//2, n)] for i in range(n//2, n)]

   b11 = [[b[i][j] for j in range(n//2)] for i in range(n//2)]
   b12 = [[b[i][j] for j in range(n//2, n)] for i in range(n//2)]
   b21 = [[b[i][j] for j in range(n//2)] for i in range(n//2, n)]
   b22 = [[b[i][j] for j in range(n//2, n)] for i in range(n//2, n)]

   # m's used to simplify c statements
   # See function header for information
   m1 = strassen(add(a11, a22), add(b11, b22))
   m2 = strassen(add(a21, a22), b11)
   m3 = strassen(a11, subtract(b12, b22))
   m4 = strassen(a22, subtract(b21, b11))
   m5 = strassen(add(a11, a12), b22)
   m6 = strassen(subtract(a21, a11), add(b11, b12))
   m7 = strassen(subtract(a12, a22), add(b21, b22))
    
   # Constructing resulting matrix quadrants
   c11 = add(subtract(add(m1, m4), m5), m7)
   c12 = add(m3, m5)
   c21 = add(m2, m4)
   c22 = subtract(add(add(m1, m3), m6), m2)

   res = [[0] * n for _ in range(n)]

   # Merge c quadrants into single matrix
   for i in range(n//2):
      for j in range(n//2):
         res[i][j] = c11[i][j]
         res[i][j + n//2] = c12[i][j]
         res[i + n//2][j] = c21[i][j]
         res[i + n//2][j + n//2] = c22[i][j]
    
   return res

def get_results(a, b):
   """ Calculates results and time for matrix multiplication
    
   Multiplies a and b using naive and Strassen's matrix multiplication
    
   Args:
      a (array): square matrix of length N
      a (array): square matrix of length N
        
   Returns:
      naive_res (matrix): array that has been multiplied by the naive method
      strassen_res (matrix): array that has been multiplied by the Strassen 
      method naive_runtime (float): runtimes for naive_res result
      strassen_runtime (float): runtime for strassen_res result
   """
   n = 2**(int(ceil(log(len(a), 2))))
    
   # Prepare arrays in case a and b are not powers of 2
   strassen_a = [[0 for _ in range(n)] for _ in range(n)]
   strassen_b = [[0 for _ in range(n)] for _ in range(n)]

   # Copy a and b over to respective variables
   # New variables are padded with 0s to get to power of 2
   for i in range(len(a)):
      for j in range(len(a)):
         strassen_a[i][j] = a[i][j]
         strassen_b[i][j] = b[i][j]

   # Time naive_mult with 'begin' and 'middle' timepoints
   begin = time.perf_counter()
   naive_res = naive_mult(a, b)
   middle = time.perf_counter()

   naive_runtime = middle - begin
    
    
   strassen_res = strassen(strassen_a, strassen_b)

   # If we added 0s to pad up to power of 2, remove them, otherwise do 
   #   nothing
   if n != len(a):
      strassen_final = [[0 for _ in range(len(a))] for _ in range(len(a))]
      for i in range(len(a)):
         for j in range(len(a)):
            strassen_final[i][j] = strassen_res[i][j]
   else:
      strassen_final = strassen_res

   # Time strassen with 'middle' and 'end' timepoints
   strassen_runtime = time.perf_counter() - middle

   return (naive_res, strassen_final, naive_runtime, strassen_runtime)

def run(path):
   """ Driver function
    
   Controls the running of this program.
    
   Args:
      path (string): the path to the input file
    
   Returns:
      naive_res (list): list of arrays that have been multiplied by the 
         naive method
      strassen_res (list): list of arrays that have been multiplied by the 
         Strassen method
      naive_runtime (list): list of runtimes for naive_res results
      strassen_runtime (list): list of runtimes for strassen_res results
   """

   # Open file and define return lists
   file = open(path, 'r')
   naive_res = []
   strassen_res = []
   naive_runtime = []
   strassen_runtime = []
   sizes = []

   while True:    
      # Get next line from file
      line = file.readline().strip()
      # If empty, exit loop
      if not line:
         break
      sizes.append(line)
      # If we don't exit, must cast string to int
      line = int(line)

      a = []
      b = []

        
      # Read through next lines, creating parameter arrays
      for i in range(line):
         a.append([int(num) for num in file.readline().strip().split()])
      for i in range(line):
         b.append([int(num) for num in file.readline().strip().split()])

      # Check for valid shape (square)
      if not (all (len (row) == len (a) for row in a) or 
         all (len (row) == len (a) for row in a)):
         raise Exception("A and B must be square matrices")
      
      # Check for identical order
      if not len(a) == len(b):
         raise Exception("A and B must be identically ordered")
      
      w, x, y, z = get_results(a, b)
      naive_res.append(w)
      strassen_res.append(x)
      naive_runtime.append(y)
      strassen_runtime.append(z)

        

      # Read line to skip empty line between examples
      file.readline()
   file.close()
    
   return (naive_res, strassen_res, naive_runtime, strassen_runtime, sizes)

def print_matrices(a, file_name):
   """ Pretty prints matrices
   
   Prints matrix a into file specified by file_name in the same way our
   input is given to us. The index of the array corresponds to the index
   of the input
   
   Args:
      a (list): the list matrix to be printed
      file_name (string): the name of the file, extension required
   """
   with open(file_name, 'w') as f:
        for i, matrix in enumerate(a):
            for row in matrix:
                f.write(' '.join(str(elem) for elem in row) + '\n')
            if i != len(a) - 1:
                f.write('\n')

def identical(a, b):
   for i in range(len(a)):
      for j in range(len(a)):
         if a[i][j] != b[i][j]:
            return 0
   return 1
#file_name = "./LabStrassenInput.txt"
#file_name = "./test_examples.txt"
#file_name = "./wrong_example.txt"
#naive_res, strassen_res, naive_runtime, strassen_runtime, sizes = run(file_name)
#count = 0
#for i in range(len(naive_res)):
#   count += identical(naive_res[i], strassen_res[i])
#with open("Num_Correct.txt", 'w') as f:
#   f.write(str(count) + "/" + str(len(naive_res)))
# print_matrices(naive_res, "NaiveResults_Required.txt")
# print_matrices(strassen_res, "StrassenResults_Required.txt")
