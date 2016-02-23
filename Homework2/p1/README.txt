


Installed packages:
    *enchant
    *python-Levenshtein
    *roman

To install, run the pip3 install on the requirements.txt file as follows

pip3 install -r requirements.txt


Transformation Rules:
    *Professor names:
        - Assumption:  There's only 1 '.' or ',' in a professor's name
        - If the professor's name has a '.' in it, then take the part after the '.' and choose the last name in that part of the name.
            Eg: Abc D. Efg Hij ===>> Hij
        - If the professor's name has a ',' in it, then take the part before the ',' as the last name
        - If the professor's name has neither of the above mentioned symbols, choose the last appearing name in the sequence of the professor's full name as the professor's last name
            Eg: Abc Def Ghi ===>> Ghi

    *Course titles:
        - Replace all '&'s with the word 'and'
        - Remove all commas from the string
        - Replace '?'s with '.'
        - Replace ':'s and '-'s with a single whitespace
        - Replace all roman numerals with the corresponding number (works up to 9)
            Eg: Introduction to Roman Numerals part vii ===>> Introduction to Roman Numerals part 7
        - Replace instances of nD with n Dimensional.
            Eg: 7D Game Engines ===>> 7 Dimensional Game Engines
        - Standardize 'intro', 'intro.' to be 'Introduction'\
        - Attempts to clean spelling mistakes. If unable to find word in dictionary, add to dictionary and leave the word untouched