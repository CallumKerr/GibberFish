# GibberFish
Extended and modified variant of the Fish programming language (https://esolangs.org/wiki/Fish)

GibberFish can be programmed and stored in either a symbolic format, or for smaller programs, a 5-bit format that makes use of multiple mappings to allow for a diverse array of commands in the limited space.

Just like Fish, execution is undertaken on a 2-dimensional, toroidal plane with the pointer starting in the top left and moving right, wrapping around whenever it passes out of the top, bottom, left, or right bounds of the program. GibberFish does however add the 5-bit map-based command system among other things to decrease program size compared to Fish, as well as additional commands and functionalities that Fish does not carry.

String literals are supported, but instead of being stored within the program they're concatenated and stored in the file header, either raw or compressed with one of two short-string compression schemes. Placeholder marks are then placed throughout the program and are replaced at runtime by the relevant symbols from the stored text.

# Requirements
Program was made and tested in Python 3.4.x and 3.5.x. No guarantees are made on working in other versions
In order to use short-string compression the pyShoco and pySMAZ modules must be installed. Programs utilizing short-string compression won't work without the relevant module for whichever compression style was used in the program

# Usage
GibberFish.py scriptfile [-h] (-e | -d) [-s <string>] [-n <number> [<number> ...]]

options:
-h	print usage help for GibberFish
-e	specify that scriptfile provided is 5-bit GibberFish encoded
-d	specify that scriptfile provided is symbolic GibberFish Encoded
-s	follow by string to add string to initial stack one character at a time
-n	follow by space seperated ints or floats to add them to initial stack (done after -s if used)