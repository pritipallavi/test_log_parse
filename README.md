#Log Parser by Priti Pallavi

This tool is used to post-process word vectors to incorporate knowledge from semantic lexicons. As shown in Faruqui et al, 2015 these word vectors are generally better in performance on semantic tasks than the original word vectors. This tool can be used for word vectors obtained from any vector training model.

###Requirements

Python 3.6
###Data you need

Input log text file containing following elements:
1. Action
2. Address
3. Line Number
4. Function Name

###Running the program

python log_parser.py -i input.txt -o output.json
