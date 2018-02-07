# easyplate
Bioscience Plate Reader parser for quicker data analysis.

## About
Bioscience Plate Readers often produce data in file formats that makes analysis take longer due to cumbersome data processing steps prior to analysis.

This tool converts BMG Plate Reader raw data in to CSV, for quicker analysis.

### Features
- Parses data from **BMG Labtech Fluostar Optima** machines
- Handles runs with files split over multiple days
- Handles runs with files split with one timepoint per file
- Allows filtering data via date range
- Outputs to CSV

### Platform Support & Downloads
Stand-alone executables compiled with [pyinstaller](https://github.com/pyinstaller/pyinstaller) are available for Windows and Debian-based operating systems.

**See the [releases](../../releases) page for downloads!**

### Usage
Place the executable in a directory that contains only the .DAT files you wish to parse.

You will be prompted to select the .DAT files you wish to import, with the option to import all .DAT files in the current directory.

You will be prompted to filter out data from the files imported by giving  start and end dates.

You will be prompted to give a filename for which to save the CSV as.

Detailed instructions on using the text-based user interface are given on running the program.

## TODO
- Parsers for different Plate Readers
- Framework for handling different parsers
- Proper code packaging
- Use a proper TUI framework instead of own dodgy implementation
