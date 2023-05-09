# rm_duplicates.py

## Usage

This is a command line tool written in Python 3.x that identifies and prints or deletes file duplicates in a provided directory and its subdirectories. The tool considers files to be duplicates if the contents of the files are exactly the same. The tool is not limited by things like file path, file name or file extension. E.g. if you accidentaly renamed and changed extension of any of your files and as a consequence 'book.pdf' now has the same content as 'song.mp3' the tool will detect that these two are duplicates. The tool is compatible with any OS with Python3.X installed, and can be used by executing the `./rm_duplicates.py` file.

If you know how to run any script file on your system you are good to go. Just make sure you have Python3.x installed, point 'rm_duplicates.py' file's shebang line to your Python and execute `./rm_duplicates.py`, it will print you help. Skip the rest in this document just read DISCLAIMER at the end of it.

## How to run command line scripts

Here is a reminder on how to run scripts using a command line.
- To run any script your command line shell must know what interpreter (Python in this case) to use and where it's located. The interpreter must know where to locate the script file itself. You might also need to provide command line arguments for a script. You would type the following on your systems shell command line:

	`interpreter script [arguments]`

, where interpreter is a path to interpreter and it's name, a script is a path and a name of your script, followed by optional command line arguments.
- There are some conventions and techniques to make script invocation shorter.
	- If a path to the interpreter and/or the script is know to the system i.e. it is in system PATH then there is no need to specify the path on command line when invoking the script.
	- If the script itself points to the correct interpreter then there is no need to type interpreter on the command line. A script can have so called shebang line, the very first line of a script starting with '#!' and followed by a path to the interpreter used to execute the script. To make a script executable it is not enough to have shebang line. The script has to be marked as executable, on UNIX like systems (Linux, macOS etc.) use chmod command to do so. E.g. `chmod 755 rm_duplicates.py`.

To summarize, make sure you have Python3.x installed, amend first line of rm_duplicates.py so that it points to Python on your system, make it executable running `chmod 755 rm_duplicates.py` (this step is not required if you use Windows) and run the script by typing `./rm_duplicates.py`. If you run it without any command line arguments It will print info how to use it.

Examples:

`./rm_duplicates.py -p /home/viktor/Documents` Prints duplicates found in specified directory.

`./rm_duplicates.py /home/viktor/Documents -p` Does the same thing. Argument order doesn't matter.

`./rm_duplicates.py -d /home/viktor/Documents` Removes duplicates from specified directory.

`./rm_duplicates.py` Prints help.

I recommend to print a list of duplicates to a file using shell redirection and inspect the list before deleting duplicates.
	`./rm_duplicates.py /home/viktor/Documents -p >duplicates_list.txt`

Feel free to extend or amend the script to your needs. For example if there are duplicates, i.e. multiple files having exactly the same content, then the shortest file name (path + name) is kept and the rest deleted. You might want to change the logic of selection of files to keep, you might want to apply different selection logic for different types of files, you might want to change print out format so that it can be piped to other tools expecting specific input structure, etc.

## DISCLAIMER

This open source project is provided "as is" and without warranties of any kind, either expressed or implied. The author of this project disclaim any liability for any direct, indirect, incidental, special, exemplary, or consequential damages that may result from the use or misuse of this project. Users of this project are solely responsible for their use of the project and any consequences that may arise from that use. By using this project, you acknowledge that you have read this disclaimer and agree to its terms.
