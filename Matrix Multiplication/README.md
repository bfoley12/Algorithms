Language: Python  
Language Version: 3.10.6 64-bit  
IDE: Visual Studio Code  
IDE Version: 1.75.1  
  
Running instructions:  
	&emsp;calling the 'run' function with the path to a list of properly formatted matrices  
	&emsp;- I.e. run("./examples.txt") will return the multiplications and runtimes of naive and
		Strassen multiplication for each matrix pair specified  
	&emsp;- Throws exceptions for:  
		&emsp;&emsp;- non-square matrices  
		&emsp;&emsp;- non-identical order of matrices  
	&emsp;- Matrices do not need to be in a power of two for Strassen's method  
  
Input:  
	&emsp;- The input I made is in test_examples.txt  
		&emsp;&emsp;- This corresponds to the answers in StrassenResults.txt and NaiveResults.txt  
	&emsp;- Required input is in LabStrassenInput.txt  
		&emsp;&emsp;- This corresponds to the answers in StrassenResults_Required.txt and 
			NaiveResults_Required.txt  
Results:   
	&emsp;- To view number of correct multiplications, open 'Num_Correct.txt'  
		&emsp;&emsp;- Format is # correct / number of problems  
	&emsp;- Runtime results  
		&emsp;&emsp;- runtimes.csv lists all runtimes of each method and size of input  
		&emsp;&emsp;- SummaryTable.csv lists representative cases  
	&emsp;- Summary:  
		&emsp;&emsp;- View either curves.png or normal_curves.png for a log_2 
			of runtimes, or raw runtimes, respectively  
	&emsp;- Matrix Multiplication answers:  
		&emsp;&emsp;- StrassenResults.txt and NaiveResults.txt show the answers to multiplications 
			in test_examples.txt, matched by index  
		&emsp;&emsp;- StrassenResults_Required.txt and NaiveResults_Required.txt show the answers 
			to multiplications in LabStrassenInput.txt, matched by index  
