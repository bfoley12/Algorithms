Language: Python  
Language Version: 3.10.6 64-bit  
IDE: Visual Studio Code  
IDE Version: 1.77.1  
  
File notes:  
	&emsp;- The input files are "DynamicLab2Input.txt" (required) and "TestInput.txt"  
	&emsp;- The output files are "output.txt" (Aligned sequences, LCS, stats) and "summary.csv" (used for analysis of efficiency and other post testing analyses)  
Running instructions:  
	&emsp;From the command line, run Project.py using the following command:  
 
		python Project.py -m 1 -p -1 -g -2 -i DynamicLab2Input.txt -o output.txt  
		python Project.py -h  
&emsp;&emsp;&emsp;- -h shows the help text detailing the arguments  
Input:  

	-m, --match_score: the matching score (typically positive)  
	-p, --mismatch_penalty: the mismatch penalty (typically negative)  
	-g, --gap_penalty: the gap penalty (typically negative)  
	
 &emsp;* Note that there are no restrictions on the float range of all three scores/penalties, it is up to the user to decide the most insightful values  

	-i, --input: the input filename  
	-o, --output: the output filename  
	-h, --help: displays the help screen  
Results:  
	&emsp;- a .txt file that is formatted as follows:  
		&emsp;&emsp;S1 = AAAAA...  
		&emsp;&emsp;S2 = AAAAA...  
		&emsp;&emsp;Aligned S1: A--A...  
		&emsp;&emsp;Aligned S2: A-AA...  
		&emsp;&emsp;LCS: GGGGGGG...  
		&emsp;&emsp;Number of comparisons: ###  
		&emsp;&emsp;Average sequence length: ##.##  
		&emsp;&emsp;Number of comparisons / Average sequence length: ##.##  
ex.  
S2 =  GTCGTTCGGAATGCCGTTGCTCTGTAAA  
S1 = ACCGGTCGACTGCGCGGAAGCCGGCCGAA
Aligned S2: GTCCGTTCGGAA-GCCG--GC-C-G--AA
Aligned S1: GAC-GCGCGGAAAGCCGGGGCCCCGGGAA
LCS: GCGCGGAAGCCGGCCGAA
Number of comparisons: 1113
Average sequence length: 28.5
Number of comparisons / Average sequence length: 39.05263157894737
