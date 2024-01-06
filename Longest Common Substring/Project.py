import getopt, sys, csv
from Cell import Cell

def initialize(A_len, B_len):
    """Initializes an A_len x B_len matrix with empty Cells
    
    Args:
      A_len (int): the length of the first sequence
      B_len (int): the length of the second sequence
      
   Returns:
      mat (Cell matrix): the A_len x B_len matrix with empty Cells
   """
    mat = [[Cell(value = 0) if i == 0 or j == 0 else Cell() \
            for i in range(B_len + 1)] for j in range(A_len + 1)]
    return mat

def get_max(i, j, seq_a, seq_b, mat, match_value, mismatch_penalty, \
            gap_penalty):
   """Creates the cell with the maximum possible value based on upper, left,
      and upper-left Cells
      
      Args:
         i (int): the row coordinate of the matrix we are considering
         j (int): the column coordinate of the matrix we are considering
         seq_a (string): the first string we are aligning
         seq_b (string): the secodn string we are aligning
         mat (Cell matrix): the dynamic programming matrix
         match_value (float): the value we add when bases match
         mismatch_penalty (float): the value we add (typically negative) when
            bases mismatch, but is the best outcome
         gap_penalty (float): the value we add (typically negative) when  
            inserting a gap
         
      Returns:
         cell (Cell): the Cell with an updated value, labeled with where we 
            obtained the value from (above, left, diagonal)
         num_comparisons (int): the number of comparisons performed (used for
            stats)
   """
   value = 0
   num_comparisons = 0
   if seq_a[i-1] == seq_b[j-1]:
      num_comparisons += 1
      value = match_value
   else:
      value = mismatch_penalty

   diagonal = mat[i-1][j-1].get_value() + value
   above = mat[i-1][j].get_value() + gap_penalty
   left = mat[i][j-1].get_value() + gap_penalty

   # Max gives bias to gaps in the "above" string when above == left
   # Also will not introduce a gap if diagonal == above or diagonal == left
   max_value = max(diagonal, above, left)

   cell = Cell(value = max_value)
   if max_value == diagonal:
      num_comparisons += 1
      cell.set_previous("diagonal")
   elif max_value == above:
      num_comparisons += 2
      cell.set_previous("above")
   else:
      cell.set_previous("left")
   return cell, num_comparisons

def backtrace(seq_a, seq_b, mat):
   """Performs the backtracing step to align two sequences
   
   Args:
      seq_a (string): the first sequence we want to align
      seq_b (string): the second sequence we want to align
      mat (float matrix): the dynamic programming matrix
      
   Returns:
      the aligned first sequence
      the aligned second sequence
      num_comparisons (int): the number of comparisons made (used for stats)
   """
   aligned_seq_a = ""
   aligned_seq_b = ""
   num_comparisons = 0
   i = len(seq_a)
   j = len(seq_b)
   while i > 0 and j > 0:
      previous = mat[i][j].get_previous()
      if previous == "diagonal":
         num_comparisons += 1
         aligned_seq_a += seq_a[i-1]
         aligned_seq_b += seq_b[j-1]
         i -= 1
         j -= 1
      elif previous == "above":
         num_comparisons += 2
         aligned_seq_a += "-"
         aligned_seq_b += seq_b[j-1]
         i -= 1
      else:
         aligned_seq_a += seq_a[i-1]
         aligned_seq_b += "-"
         j -= 1
   return aligned_seq_a[::-1], aligned_seq_b[::-1], num_comparisons

def get_LCS(aligned_seq_a, aligned_seq_b):
   """Finds the longest common substring
   
   Args:
      aligned_seq_a (string): the aligned first string
      aligned_seq_b (string): the aligned second string
      
   Returns:
      lcs (string): the longest common substring
      num_comparisons (int): the number of comparisons made (used for stats)
   """
   lcs = ""
   num_comparisons = 0
   for i in range(len(aligned_seq_a)):
      num_comparisons += 1
      if aligned_seq_a[i] == aligned_seq_b[i] and aligned_seq_a != "-":
         num_comparisons += 1
         lcs += aligned_seq_a[i]
   
   return lcs, num_comparisons
   
def get_trace_mat(mat):
   """Formats the matrix to show the path of backtrace
   
   Args:
      mat (float matrix): the dynamic programming matrix
   
   Returns:
      trace_mat (string matrix): the backtrace path matrix in string
         representation
   """
   trace_mat = [["0" for j in range(len(mat[0]))] for i in range(len(mat))]
   for i in range(len(mat)):
      for j in range(len(mat[0])):
         match mat[i][j].get_previous():
            case "diagonal":
               trace_mat[i][j] = "\\"
            case "above":
               trace_mat[i][j] = "^"
            case "left":
               trace_mat[i][j] = "<"
   return trace_mat

def trace_output(trace_mat):
   """Formats the trace matrix into a print-friendly string
   
   Args:
      trace_mat (string matrix): the output of get_trace_mat
   
   Returns:
      ret (string): the formatted string of trace_mat
   """
   ret = ""
   for i in range(len(trace_mat)):
      for j in range(len(trace_mat[0])):
         ret += trace_mat[i][j] + " "
      ret += "\n"
   return ret

def read_file(filename):
   """Reads in a text file
   
   Reads in a text file containing sequences to compare
   
   Args:
      filename (string): the name of the file to be read
   
   Returns:
      labels (string list): the names of the sequences to compare
      sequences (string list): the sequences to compare
   """
   file = open(filename, "r")
   labels = []
   sequences = []
   for line in file:
      line = line.rsplit("=", 1)
      line = [x.strip(' ') for x in line]
      labels.append(line[0])
      sequences.append(line[1].strip())
   file.close()
   return labels, sequences

def write_output(filename, output):
   """Writes to a text file
   
   Helper function to write output

   Args:
      filename (string): the file to write to (overwrites the file)
      output (string list): the list of string to be written to the file
   """
   with open(filename, 'w') as f:
      f.write(output)

argument_list = sys.argv[1:]
options = "hm:p:g:i:o:"
long_options = ["help", "match_score", "mismatch_penalty", "gap_penalty", \
                "input", "output"]

# parse command line arguments
try:
   arguments, values = getopt.getopt(argument_list, options, long_options)
   output_filename = ""
   help_string = "-h, --help: displays this help menu\n\
   -m, --match_score: the score of a match\n\
   -p, --mismatch_penalty: the penalty to apply on a mismatch\n\
   -g, --gap_penalty: the penalty to apply on a gap\n\
   -i, --input: the input filename \n\
   -o, --output: the filename of the output file. Running without this prints\
      output to terminal"
   for current_argument, current_value in arguments:
      if current_argument in ("-h", "--help"):
         print(help_string)
         exit()
      elif current_argument in ("-m", "--match_score"):
         match_value = current_value
      elif current_argument in ("-p", "--mismatch_penalty"):
         mismatch_penalty = current_value
      elif current_argument in ("-g", "--gap_penalty"):
         gap_penalty = current_value
      elif current_argument in ("-i", "--input"):
         input_filename = current_value
      elif current_argument in ("-o", "--output"):
         output_filename = current_value
except getopt.error as err:
   print(str(err))

# Input exception handling
if match_value.lstrip("-").isnumeric():
   match_value = float(match_value)
else:
   raise Exception("Match value must be numeric")
if mismatch_penalty.lstrip("-").isnumeric():
   mismatch_penalty = float(mismatch_penalty)
else:
   raise Exception("Mismatch penalty must be numeric")
if gap_penalty.lstrip("-").isnumeric():
   gap_penalty = float(gap_penalty)
else:
   raise Exception("Gap penalty must be numeric")

# File extension formatting
if output_filename[-4:] != ".txt":
   raise Exception("Please specify the output file with the extension '.txt'")
if input_filename[-4:] != ".txt":
   raise Exception("Please specify the input file with the extension '.txt'")

# read in sequences
labels, sequences = read_file(input_filename)
output = ""
csv_rows = []
# Pairwise comparison of each sequence
for i in range(len(sequences)):
   for j in range(i):
      seq_a = sequences[i]
      seq_b = sequences[j]
      a_len = len(seq_a)
      b_len = len(seq_b)
      num_comparisons = 0
      # Create the empty dynamic programming matrix
      mat = initialize(a_len, b_len)
      
      # Populate each cell in the matrix
      for n in range(1, a_len + 1):
         for m in range(1, b_len + 1):
            mat[n][m], comparisons = get_max(n, m, seq_a, seq_b, mat, match_value, \
                                mismatch_penalty, gap_penalty)
            num_comparisons += comparisons

      # Create aligned sequences through backtracing
      aligned_seq_a, aligned_seq_b, comparisons = backtrace(seq_a, seq_b, mat)
      num_comparisons += comparisons

      # Find LCS
      lcs, comparisons = get_LCS(aligned_seq_a, aligned_seq_b)
      num_comparisons += comparisons

      # Format outputs
      output += labels[i] + " =  " + seq_a + "\n"\
                  + labels[j] + " = " + seq_b + "\n"\
                  + "Aligned " + labels[i] +": " + aligned_seq_a + "\n"\
                  + "Aligned " + labels[j] +": " + aligned_seq_b + "\n"\
                  + "LCS: " + lcs + "\n"\
                  + "Number of comparisons: " + str(num_comparisons) + "\n"\
                  + "Average sequence length: " + \
                     str((len(seq_a) + len(seq_b))/2) + "\n"\
                  + "Number of comparisons / Average sequence length: " + \
                  str(num_comparisons/((len(seq_a) + len(seq_b))/2)) + "\n\n"
      
      # Prep CSV output
      csv_rows.append([num_comparisons, len(seq_a) * len(seq_b), (len(seq_a) + len(seq_b))/2, \
                       num_comparisons/((len(seq_a) + len(seq_b))/2), lcs])

# Write stats to CSV
with open('summary.csv', 'w', newline="", encoding='UTF8') as f:
    writer = csv.writer(f)

    # write the header
    writer.writerow(["num_comparisons", "num_bases", "avg_seq_len", "comp_per_seq_len", "LCS"])

    # write the data
    for row in csv_rows:
      writer.writerow(row)
# Write aligned sequences, LCS, and stats to .txt
write_output(output_filename, output)