Language: Python
Language Version: 3.10.6 64-bit
IDE: Visual Studio Code
IDE Version: 1.75.1

Running instructions: calling the 'run' function with the path to a list of properly formatted matrices
	- I.e. run("./examples.txt") will return the multiplications and runtimes of naive and
		Strassen multiplication for each matrix pair specified
	- Throws exceptions for:
		- non-square matrices
		- non-identical order of matrices
	- Matrices do not need to be in a power of two for Strassen's method

Input:
	- The input I made is in test_examples.txt
		- This corresponds to the answers in StrassenResults.txt and NaiveResults.txt
	- Required input is in LabStrassenInput.txt
		- This corresponds to the answers in StrassenResults_Required.txt and 
			NaiveResults_Required.txt
Results: 
	- To view number of correct multiplications, open 'Num_Correct.txt'
		- Format is # correct / number of problems
	- Runtime results
		- runtimes.csv lists all runtimes of each method and size of input
		- SummaryTable.csv lists representative cases
	- Summary:
		- View either curves.png or normal_curves.png for a log_2 
			of runtimes, or raw runtimes, respectively
	- Matrix Multiplication answers:
		- StrassenResults.txt and NaiveResults.txt show the answers to multiplications
			in test_examples.txt, matched by index
		- StrassenResults_Required.txt and NaiveResults_Required.txt show the answers
			to multiplications in LabStrassenInput.txt, matched by index