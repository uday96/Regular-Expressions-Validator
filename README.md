# **Regular Expression Validator** #

Validate if a given string matches a regular expresssion.

 - Checks for the validity of the Regular Expression using **Cocke-Younger-Kasami (CYK) Algorithm **
 - Constructs an equivalent **Non-Deterministic Finite Automaton (NFA)**
 - Check if the input strings are a part of the language defined by the given regular expression.

### Input: ###

First line of the input is a regular expression string R (0 < |R| < 100). Second line is an integer N (0 < N < 1000) represents total number of names following. N lines gives the names of the people. The name is a string S(0 < |S| < 100000).

The regular expression will be valid if it satisfies the following conditions
>1. The valid operations are concatenation(.), union(+) and closure(*).
>2. Each basic expression will be one of the form (a+b) or (a*) or (a.b).
>3. The final expression can be a recursive use of basic expressions.
Some examples of valid regular expressions ((a*).b) , (((a.b)+b)*) ,etc.

### Output: ###
If the Regular expression is not valid , output ”**Wrong Expression**”. Otherwise output N lines of ”**Yes**”
or ”**No**” each corresponding to whether the string matches or not.
