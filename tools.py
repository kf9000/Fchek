import zlib
import os

def calculate_file_amount(filepath):
    total = 0
    for root, dirs, files in os.walk(filepath):
        total += len(files)
    return total

def calculate_hash(filepath, chunksize=65536):
        with open(filepath, "rb") as file:
            hash = 0
            while (chunk := file.read(chunksize)):
                hash = zlib.crc32(chunk, hash)
            return hex(hash).upper().removeprefix("0X")

def get_region(file):
    in_parenthesis = False
    found = False

    region = ""
    for char in file:
        if char == ")":
            found = True
            in_parenthesis = False
        if in_parenthesis and not found:
            region = region + char
        if char == "(":
            in_parenthesis = True

    if len(region) <= 2:
        temp_region = ""
        for char in region:
            if char == "A":
                temp_region = temp_region + ", Australia"
            elif char == "E":
                temp_region = temp_region + ", Europe"
            elif char == "U":
                temp_region = temp_region + ", USA"
            elif char == "J":
                temp_region = temp_region + ", Japan"
        region = temp_region[2:]
    if("disc" in region.lower()):
        region = ""
    return region

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)

        source : https://stackoverflow.com/a/34325723
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()