# Keywords-in-Context
A small keywords in context (KWIC) python implementation with sentence recognition.
Features
--------
* Summerize a larger text around keywords with a fixed amount of words before and after each keyword
* Summerize a larger text around keywords with a maximum amount of words before and after each keyword unless a new sentence beginns or ends.
* Ignore definied abbreviations which dont mark the beginning or end of a sentence.
* Works with strings containing multiple words as "keyword"
* Works with a list of several keywords

Usage
-----
Usage is simple, no additional modules are needed. 
Just copy the functions into your file or import the function keywords_in_context.

Example
-------
text.png
```python
KEYWORDS = ["Sed", "lorem ipsum", "quo", "recusandae", "doloribus"]

result_text = keywords_in_context(TEXT, KEYWORDS)
# Highlight Keywords
for k in KEYWORDS:
    result_text = find_and_replace(result_text, k, "\x1b[34m"+k+"\x1b[0m")
```
result.png

License
-------
MIT Licence see Licence.txt
