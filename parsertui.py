from plateparser2 import PlateParser, PlateParserError
import sys
import os
import platform


__version__ = "1.0.0"


class ParserTUI:
    title = "Platereader Parser".upper()

    def __init__(self):
        self.parser = None
        self.plate = None

    def window(self):
        self.clear()
        print("=*={} - V{}".format(self.title, __version__), end="\n\n")
        self.instructions()

    def heading(self, header):
        print("{}".format(header))

    def clear(self):
        plat = platform.system()
        if plat == "Windows":
            os.system("cls")
        elif plat == "Linux":
            os.system("clear")
        else:
            print("(Clear screen is not supported on this platform.)")

    def prompt_yn(self, message):
        yn = input(">> {} ['Y':YES, ENTER:NO]: ".format(message))
        return yn == "Y" or yn == "y"

    def mode_pick_input(self):
        files = [x for x in os.listdir() if os.path.isfile(x)]
        files = [x for x in files if os.path.splitext(x)[1] == ".DAT"]
        if not files:
            print("Error! No .DAT files in this directory!")
            self.finish()
        print()
        selected_files = self.select_from_list(files, n=1000, message="Choose DAT files", ask_all=True)
        print()
        self.parser = PlateParser(selected_files)

    def mode_pick_dates(self):
        selected_dates = self.select_from_list(self.parser.dates, n=2, message="Choose dates by range (start and end, inclusive)")
        print()
        plate = self.parser.plate_from_daterange(selected_dates[0], selected_dates[1])
        self.plate = plate

    def write_file(self, path, data):
        if os.path.exists(path):
            print("File or directory with name {!r} already exists!".format(path))
            overwrite = self.prompt_yn("Overwrite file?")
            if not overwrite:
                return False

        elif not path:
            print("File path was empty")
            return False

        with open(path, "w") as f:
            f.write(data)
            print("Written to {!r}".format(path))
            return True

    def mode_output_csv(self):
        while True:
            path = input(">> Name of output CSV file (eg 'data.csv'): ")
            write = self.write_file(path, self.plate.to_csv())
            if write:
                break

    def select_from_list(self, li, n=1, message=None, info=None, ask_all=False):
        if info is None:
            info = [""] * len(li)
        print("==========")
        print("OPT - ITEM")
        print("----------")
        for i, (x, inf) in enumerate(zip(li, info)):
            out = "[{}] - {!r}".format(i, x)
            if inf:
                out += " ({})".format(inf)
            print(out)
        print()

        if ask_all:
            collect_all = self.prompt_yn("Select ALL available options?")
        else:
            collect_all = False


        while True:
            choices = []
            if not collect_all:
                while len(choices) < n:
                    choice = self.prompt_number(message)
                    if choice is None:
                        break
                    else:
                        print("Selected option {}".format(choice))
                        choices.append(choice)
                    print()
            else:
                choices = [i for i in range(len(li))]
            if not choices:
                print("Error! Nothing selected!")
                continue
            else:
                try:
                    output = [li[i] for i in choices]
                except IndexError as e:
                    print("Error! Invalid choice(s)!")
                    continue
                else:
                    break

        self.window()
        str_output = list(map(str, output))
        print("Selected {!r}".format(str_output), end=" ")
        happy = self.prompt_yn("Okay?")
        if not happy:
            output = self.select_from_list(li, n=n, message=message)
            print()
        return output

    def prompt_number(self, message):
        while True:
            n_str = input(">> {} [option eg '0', press ENTER again to finish selection]: ".format(message))
            if not n_str:
                return None
            try:
                n = int(n_str)
            except ValueError:
                print("Error! Input was not a number!")
                print()
            else:
                return n

    def finish(self):
        print()
        print(">> PRESS ENTER TO EXIT")
        input()
        sys.exit(0)

    def instructions(self):
        print("""Built by Zac Rubin github.com/z-0

~Currently tested with BMG Labtech Fluostar Optima data~

USAGE

Please ensure that the files have the .DAT extension.
Please ensure that the files are in the same directory as this program.
User interaction is prompted by '>>'.
Input options are shown in square brackets - eg ['Y'].
When prompted for multiple options, press ENTER after each individual option.
Remember that options are zero-indexed (ie 0 is for the first option).""")
        print()
        print("***")
        print()

    def run(self):
        self.window()
        self.heading("SELECT INPUT FILES")
        self.mode_pick_input()
        print(end="\n\n")
        self.window()
        self.heading("FILTER DATA BY DATES")
        try:
            self.mode_pick_dates()
        except PlateParserError as e:
            print("ERROR!")
            print(e)
            self.finish()
        print(end="\n\n")
        self.window()
        print("Data loaded OKAY!", end="\n\n")
        self.heading("WRITE DATA")
        self.mode_output_csv()
        self.finish()


if __name__ == "__main__":
    app = ParserTUI()
    app.run()


