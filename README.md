# CROSSPULL.py
Python Code that pulls metadata for every publication in Crossref that lists a specific institution in it's author affiliations. This metadata is exported as a csv file 

## CROSSPULL.py for those without programming experience

The crosspull program can be used by those unfamilar with python or programing. Four key steps need to be followed:
  1. [Download Python 3](https://www.python.org/downloads/)
  2. Copy and paste the program code to a [text editor](https://en.wikipedia.org/wiki/Text_editor) (e.g. Notepad) and make sure it is saved as a ".py" program (e.g. APICDOI.py)
  3. Open and edit (e.g. Right click and select "Open with") the firstline of the code in the text editor to add your email. (e.g. email = "ryan@email.com")
  4. Open and run the code with the Python intrepreter (i.e. IDLE)
  
Your email is required so that Crossref can keep an idea how their API is being used and can contact you if any overuse or problems. This is a standard practice with most free and public APIs these days.

## How to Use

Crossref doesn't currently have a phrase search option, so searching for 'University of Guelph' will pull every item that mentions even one of "Guelph", "University" and "Of".

This code is a way around that. It'll ask you for your insitution's full name (e.g. University of Waterloo) and then the distingushing keyword from your insitutions name (e.g. Waterloo). Then it will search for the keyword in Crossref's author affiliations, collect all the items, and then filter out all of those that don't mention the full name of your insitution.

(Note: 'Physics Department, University of Waterloo' would get captured by this filter and included in the final export)

## Issues

- This code only finds via author affiliations, not editor or funder affiliations
- A lot of publishers currently don't provide author affiliations to crossref but more and more are every year
