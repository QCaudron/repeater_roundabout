import sys


files = [
    "assets/programming_files/d878.csv",
    "assets/programming_files/d878-talk-groups.csv",
    "assets/programming_files/d878-scanlist.csv",
]


if __name__ == "__main__":

    all_is_well = True

    for file in files:
        with open(file, "rb") as f:
            text = f.read()

            crlf, lf = text.count(b"\r\n"), text.count(b"\n")
            if crlf != lf:
                print(f"{file} may not have CRLF line endings.")
                all_is_well = False

    # if not all_is_well:
    #     sys.exit(1)
