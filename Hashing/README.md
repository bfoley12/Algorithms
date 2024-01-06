Language: Python  
Language Version: 3.10.6 64-bit  
IDE: Visual Studio Code  
IDE Version: 1.77.1  

File notes:  
	&emsp;- The input files I used are labeled with "Input" along with their size  
	&emsp;- The output of the LabHashingInput.txt for each case is in a file labeled "Case#.txt" where the # relates to the case.  
Running instructions:  
	&emsp;From the command line, run Project.py using the following command:  
 
		python Project.py -m 120 -p 0 -b 1 -c linear -i LabHashingInput.txt -o Case1.txt
		python Project.py -h
  &emsp;&emsp;&emsp;- -h shows the help text detailing the arguments  
Input:  

	-m is the modulus
	-p is a flag for switching from division to my own hash
	-b is the bucket size
	-c is the collision scheme
		- must be one of: linear, quadratic, chaining
	-i is the input filename
	-o is the output filename
		- running without this argument prints to terminal
Results:   
	- a file named as specified by -o  
		- formatted as:  
  
		Input keys size: ##  
		Table size: ##  
		Input keys:  
		# # # # #  
		etc.  
		
		=====================
		Hash Table size: ##
		Bucket Size: ##
		Collision Scheme: ""
		Primary Collisions: ##
		Secondary Collisions: ##
		Number of comparisons: ##
		Number not inserted: ##
		Keys not inserted: []
		Load Factor: #.#
		
		============================= 

		Hash Table
		1 ----- ----- ----- ----- -----
		2 ... etc
