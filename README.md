# easyplate
Bioscience Plate Reader parser for quicker data analysis.

## About
Bioscience Plate Readers often produce data in file formats that makes analysis take longer due to cumbersome data processing steps prior to analysis.

This tool converts BMG Plate Reader raw data in to CSV, for quicker analysis.

### Platform Support & Downloads
Stand-alone binaries compiled with [pyinstaller](https://github.com/pyinstaller/pyinstaller) are available for Windows and Debian-based operating systems.

### Features
- Parses data from **BMG Labtech Fluostar Optima** machines
- Handles runs with files split over multiple days
- Handles runs with files split with one timepoint per file
- Allows filtering data via date range
- Outputs to CSV

## TODO
- Parsers for different Plate Readers
- Proper code packaging
- Use a proper TUI framework instead of own dodgy implementation
