[![ci](https://github.com/jonbiemond/BCIT-Flex/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jonbiemond/BCIT-Flex/actions/workflows/ci.yml)
# BCIT Flex
Webscrape BCIT available courses, quickly view course offerings and write the information to a text file

Please feel free to report any issues, bugs or suggestions. Pull requests are welcome.

The information is
+ Code
+ Name
+ Prerequisites
+ Credits
+ URL
+ Offerings
  + Instructor
  + Price
  + Duration
  + Meeting Times
  + Status
  + Rate My Professor URLs

## Installation
+ Clone the repository
+ Install the requirements `poetry install`

## Usage
1. Run `python interface.py`
2. Enter and load a subject.

![An example of the GUI, showing a small window with an input box titled "Subject" with the text "MATH" inputted,
  to the right of the input box is a button titled "Load", on the next row is an empty drop down menu titled "Subject",
  beneath that a line of text that reads "Loading MATH courses..."  
  and then a row of buttons; "Save" and "Cancel".](https://i.ibb.co/N6zynYK/BCIT-Course-Finder-Load-Subject.png "BCIT Course Finder")

3. Select a course from the drop-down menu. The number in brackets represents the number of offerings for that course.

![An example of the GUI, similar to the previous step. 
But now showing a full drop down menu titled "Course" with the text 2011 (2) selected.](https://i.ibb.co/xg4nWRP/BCIT-Course-Finder-Choose-Course.png "BCIT Course Finder")

4. Course offerings pop up in a new window.

![A popup window showing the course offerings for MATH 2011.](https://i.ibb.co/ZM0c5xh/BCIT-Course-Finder-Pop-Up.png "BCIT Course Finder")

5. Click "Save" to save the course offerings to a text file.

## Supports
+ Displaying all course offerings for specific course
+ Saving all courses to a text file for a specific subject

## TODO
+ Filter by prerequisites
+ ~~Individual Course Offerings~~
+ ~~Rate My Professors~~
+ WebAssembly
+ ~~GUI~~
+ Return RMP rating

## Contributors
- Sam - [0x53616D75656C](https://github.com/0x53616D75656C)
- Jonathan - [jonbiemond](https://github.com/jonbiemond)
