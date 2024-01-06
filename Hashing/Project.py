import getopt, sys
"""
This program is used to assess various hashing strategies.

It can be run from the command line by providing arguments:
-p, --personal_hash: a flag for whether my personal hash (described below) 
                     should be used
-o, --output: the filename of the output file
-m, --modulus: the modulus you wish to use
-b, --bucket_size: the bucket size you wish to use
-c, --collision_scheme: the collision scheme (linear, quadratic, or chaining)
-i, --input: the input filename

The personal hash funtion that I elected to use is multiplication and is 
derived as follows:
h(k) = floor(M(kA mod 1))
where M is the size of the hash table (120), k is the key value, and A is a 
constant, 0<A<1, which I chose to be 0.623. 
"""
def hash(input, modulus, bucket_size, collision_scheme, personal_hash):
   """ Hash table calculation
   
   Depending on the arguments provided, calculates the hash table of input 
      keys

   Args:
      input (int list): a list of the keys to be hashed
      modulus (int): the modulus to perform hashing with
      bucket_size (int): the bucket size of the hash table
      collision_scheme (string): the collision resolution method to use, must
         be one of: linear, quadratic, chaining
      personal_hash (boolean): flag to use personal_hash (1) or not (0)

   Returns:
      table: the resulting hash table
      primary_collsions (int): number of primary collisions (used for stats)
      secondary_collisions (int): number of secondary collisions (used for
         stats)
      num_comparisons (int): number of comparisons performed (used for stats)
      not_inserted (int list): list of keys not inserted (used for stats)
   """
   # Creates empty table of buckets properly sized according to static table
   #  size of 120
   table = [ [list() for j in range(bucket_size)] \
            for i in range(int(120/bucket_size)) ]
   primary_collisions = 0
   secondary_collisions = 0
   not_inserted = list()
   num_comparisons = 0

   # For every key we have, we compute the hash
   for key in input:
      # perform personal hash if flag is set
      if personal_hash:
         index = int(len(table) * ((key * .623) % 1))
      else:
         index = key % modulus
      # if the key hashes to an empty spot first, store it
      loc = has_space(table[index])
      if loc != -1 or collision_scheme == "chaining":
         table[index][loc].append(key)
      # otherwise, handle the collision and store it there
      else:
         index, sc, nc = handle_collision(table, key, modulus, \
                                          collision_scheme, personal_hash)
         # if we cannot store it, keep track of it
         if index == -1:
            not_inserted.append(key)
         else:
            loc = has_space(table[index])
            table[index][loc].append(key)
         primary_collisions += 1
         secondary_collisions += sc
         num_comparisons += nc
         

   return table, primary_collisions, secondary_collisions, num_comparisons, \
      not_inserted

def handle_collision(table, key, modulus, collision_scheme, personal_hash):
   """Handles collisions of hash table
   
   Handles the collisions that occur when creating the hash table, with
   varying methods, depending on the arguments provided
   
   Args:
      table (int list): the table we are hashing into
      key (int): the key that had the collision
      modulus (int): the modulus we are hashing with
      collision_scheme (string): the collision resolution method to use, must
         be one of: linear, quadratic, chaining
      personal_hash (boolean): flag to use personal_hash (1) or not (0)
   
   Returns:
      i (int): the index we can hash the given key into, safely
      primary_collsions (int): number of primary collisions (used for stats)
      secondary_collisions (int): number of secondary collisions (used for
         stats)"""
   index = 1
   counter = 0
   secondary_collision = 0
   num_comparisons = 1

   # select proper collision method, as specified
   match collision_scheme:
      case "linear":
         # we still use the personal hash if asked, but the updates happen as 
         #  specified by collision_scheme
         if personal_hash:
            i = int(len(table) * ((key * .623) % 1))
         else:
            i = (key + index) % modulus
         # continue until we find a space
         while has_space(table[i]) == -1:
            secondary_collision = 1
            num_comparisons += 1
            index += 1
            counter += 1
            
            # if we have tried every spot, return unsuccessful attempt
            if counter >= len(table):
               return -1, 1, num_comparisons
            
            # update key as specified
            if personal_hash:
               i = int(len(table) * ((key * .623) % 1))
            else:
               i = (key + index) % modulus
      case "quadratic":
         c1 = 1
         c2 = 2
         if personal_hash:
            i = int(len(table) * ((key * .623) % 1))
         else:
            i = int((key + c1 * index + c2 * index**2) % modulus)
         # continue until we find a space
         while has_space(table[i]) == -1:
            secondary_collision = 1
            num_comparisons += 1
            index += 1
            counter += 1

            # if we tried every possible spot, return unsuccessful attempt
            if counter >= len(table):
               return -1, 1, num_comparisons
            
            # update key as specified
            if personal_hash:
               i = int(len(table) * ((key * .623) % 1))
            else:
               i = int((key + c1 * index + c2 * index**2) % modulus)
      case "chaining":
         # since we can chain, we return the same index
         index = 0
   return i, secondary_collision, num_comparisons

def has_space(arr):
   """Checks whether there is space in a bucket
   
   Helper method that checks for space in a given bucket
   
   Args:
      arr (array): the bucket we are checking for an open space
      
   Returns:
      i (int): the first index we can safely insert at, -1 if everything is 
         full
   """
   i = 0
   for a in arr:
      if a == []:
         return i
      i += 1
   return -1

def pretty_print(table, bucket_size, collision_scheme):
   """Formats hash table for printing
   
   Formats the hash table in proper format for inspecting
   
   Args:
      table (int array): the table to be printed
      bucket_size (int): the number of elements allowed in each bucket
      collision_scheme (string): the collision resolution method to use, must
         be one of: linear, quadratic, chaining
         
   Returns:
      table_string (string): the properly formatted table for printing
   """
   table_string = ""
   counter = 0
   row_num = 1
   # print each bucket
   for bucket in table:
      if counter == 0:
         table_string += str(row_num) + " "
      for elem in bucket:
         # if there is an element present, print it
         if elem:
            # handle chaining
            if collision_scheme == "chaining":
               for e in elem:
                  table_string += str(e).zfill(5) + "->"
               table_string = table_string[:-2]
            else:
               table_string += str(elem[0]).zfill(5)
         # if no element, add filler
         else:
            table_string += "-----"
         table_string += " "
      counter += 1
      # handle new lines based on bucket size
      if bucket_size == 1 and counter == 5:
         table_string += "\n"
         counter = 0
         row_num += 1
      elif bucket_size != 1:
         table_string += "\n"
         row_num += 1
         counter = 0
   return table_string

def stats_string(table, bucket_size, collision_scheme, primary_collisions, \
                 secondary_collisions, num_comparisons, not_inserted):
   """Formats the stats we collected for printing
   
   Args:
      table (int array): the table to be printed
      bucket_size (int): the number of elements allowed in each bucket
      collision_scheme (string): the collision resolution method to use, must
         be one of: linear, quadratic, chaining
      primary_collsions (int): number of primary collisions (used for stats)
      secondary_collisions (int): number of secondary collisions (used for
         stats)
      num_comparisons (int): number of comparisons performed (used for stats)
      not_inserted (int list): list of keys not inserted (used for stats)
      
   Returns:
      stats_string (string): the properly formatted statistical information
   """
   stats_string = "Hash Table size: 120 \n"
   stats_string += "Bucket Size: " + str(bucket_size) + "\n"
   stats_string += "Collision Scheme: " + collision_scheme + "\n"
   stats_string += "Primary Collisions: " + str(primary_collisions) + "\n"
   stats_string += "Secondary Collisions: " + str(secondary_collisions) + "\n"
   stats_string += "Number of comparisions: " + str(num_comparisons) + "\n"
   stats_string += "Number not inserted: " + str(len(not_inserted)) + "\n"
   stats_string += "Keys not inserted: " + str(not_inserted) + "\n"
   num_items = 0
   # calculate load
   for bucket in table:
      for elem in bucket:
         if len(elem) > 1:
            for e in elem:
               num_items += 1
         elif len(elem) == 1:
            num_items += 1
   load_factor = num_items / 120

   stats_string += "Load Factor: " + str(load_factor) + "\n\n"
   stats_string += "============================= \n\n"
   stats_string += "Hash Table\n"

   return stats_string

def input_string(input):
   """Formats input keys for printing in output file
   
   Args:
      input (int list): list of keys from input
   
   Returns:
      input_string (string): input keys formatted for printing
   """
   input_string = "Input keys size: " + str(len(input)) + "\n"
   input_string += "Table size: 120\n"
   input_string += "Input keys: \n"
   counter = 1
   for i in input:
      input_string += str(i) + " "
      if counter == 5:
         counter = 0
         input_string += "\n"
      counter += 1
   input_string += "\n=====================\n"
   return input_string

def read_file(filename):
   """Reads in a text file
   
   Reads in a text file containing keys to be hashed
   
   Args:
      filename (string): the name of the file to be read
   
   Returns:
      arr (int list): the keys to be hashed
   """
   file = open(filename, "r")
   arr = []
   for line in file:
      line = line.strip()
      if line.isdigit():
         arr.append(int(line))
   file.close()
   return arr

def write_file(filename, string):
   """Writes to a text file
   
   Helper function to write output

   Args:
      filename (string): the file to write to (overwrites the file)
      string (string): the string to be written to the file
   """
   with open(filename, 'w') as f:
      f.write(string)

argument_list = sys.argv[1:]
options = "hp:m:b:c:i:o:"
long_options = ["help", "personal_hash", "output", "modulus", "bucket_size",\
                "collision_scheme", "input"]

# parse command line arguments
try:
   arguments, values = getopt.getopt(argument_list, options, long_options)
   output_filename = ""
   help_string = "-p, --personal_hash: a flag for whether my personal hash \
should be used \n\
-o, --output: the filename of the output file. Running without this prints\
 output to terminal \n\
-m, --modulus: the modulus you wish to use \n\
-b, --bucket_size: the bucket size you wish to use\n\
-c, --collision_scheme: the collision scheme \
(linear, quadratic, or chaining)\n\
-i, --input: the input filename"
   for current_argument, current_value in arguments:
      if current_argument in ("-h", "--help"):
         print(help_string)
         exit()
      elif current_argument in ("-p", "--personal_hash"):
         personal_hash = int(current_value)
      elif current_argument in ("-o", "--output"):
         output_filename = current_value
      elif current_argument in ("-m", "--modulus"):
         modulus = int(current_value)
      elif current_argument in ("-b", "--bucket_size"):
         bucket_size = int(current_value)
      elif current_argument in ("-c", "--collision_scheme"):
         collision_scheme = current_value
      elif current_argument in ("-i", "--input"):
         input_filename = current_value
except getopt.error as err:
   print(str(err))

# Exception handling
if collision_scheme not in ("linear", "quadratic", "chaining"):
   raise Exception("collision_scheme must be one of: linear, quadratic, \
                   chaining")
if not isinstance(modulus, int) or modulus == 0:
   raise Exception("modulus must be an integer not equal to 0")
if not isinstance(bucket_size, int) or bucket_size < 1 or bucket_size > 120:
   raise Exception("bucket_size must be an integer 1 <= bucket_size <= 120")
if modulus > 120/bucket_size:
   raise Exception("modulus must be < 120/bucket_size")

# File extension formatting
if output_filename[-4:] != ".txt":
   output_filename += ".txt"
if input_filename[-4:] != ".txt":
   input_filename += ".txt"


input = read_file(input_filename)
table, primary_collisions, secondary_collisions, num_comparisons, \
   not_inserted = hash(input, modulus, bucket_size, collision_scheme, \
                       personal_hash)
output_string = input_string(input) + stats_string(table, bucket_size, \
               collision_scheme, primary_collisions, secondary_collisions, \
                  num_comparisons, not_inserted) +\
               pretty_print(table, bucket_size, collision_scheme)

if output_filename != ".txt":
   write_file(output_filename, output_string)
else:
   print(output_string)