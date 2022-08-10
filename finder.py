import os
import re
#from spanish_finder import the_input
from spanish import spanish_words
import ctypes
import sys
import time

def get_csbi_attributes(handle):
    # Based on IPython's winconsole.py, written by Alexander Belchenko
    import struct
    csbi = ctypes.create_string_buffer(22)
    res = ctypes.windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi)
    assert res

    (bufx, bufy, curx, cury, wattr,
    left, top, right, bottom, maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
    return wattr

def print_red(text):
    if os.name == 'nt':
        # Constants from the Windows API
        STD_OUTPUT_HANDLE = -11
        FOREGROUND_RED    = 0x0004 # text color contains red.

        handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        reset = get_csbi_attributes(handle)

        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, FOREGROUND_RED)
        print(text)
        ctypes.windll.kernel32.SetConsoleTextAttribute(handle, reset)

        # call win32 api
        
    else:
        print("\033[91m{}\033[00m".format(text))

def print_blue(text):
    print("\033[94m{}\033[00m".format(text))

# converts:
# 
# a(){} 
# 
# into 
# 'a'
# by removing all the characters that are not a letter using a python regex
def code2words(input):
    return re.sub(r'[^a-zA-Z]', ' ', input)
    #return input.replace(r'AAA', '')

def spanish_language_dict():
    return {word: True for word in spanish_words.split()}

def detect_spanish_words(file_name):
    the_input = ""
    with open(file_name, 'r') as f:
        the_input = f.read()

    #print(the_input)
    #print(len(" ".join(the_input)))
    # convert input to list of words

    # remove non-alphabetic characters
    #the_input = the_input.replace('.', ' ')

    def extract_comments(lines):
        comments = []
        for line in lines:
            if re.match(r'^\s*//', line):
                comments.append(line)
        return comments

    lines = the_input.split('\n')
    comments = extract_comments(lines)
    # make all comments lowercase
    comments = [comment.lower() for comment in comments]

    the_input = " ".join([ code2words(word) for word in comments ])
    # normalize spaces
    the_input = re.sub(r'\s+', ' ', the_input)
    the_dict = {word:word for word in the_input.split()}
    # check how many of the words in spanish were found
    found = 0
    spdict = spanish_language_dict()
    word_list = []
    for word in the_dict:
        if word in spdict:
            found += 1
            word_list.append(word)

    if found > 0:
        print_red(file_name + ": Spanish words found: {}".format(found))
        print_red(file_name + ": Spanish words: {}".format(word_list))
    else:
        print(file_name + ": OK")


def process_folder(folder_name):
    for file_name in os.listdir(folder_name):
        #if it is a folder, recurse
        if os.path.isdir(os.path.join(folder_name, file_name)):
            process_folder(os.path.join(folder_name, file_name))
        else:
            if file_name.endswith('.js'):
                print("Processing {}".format(file_name))
                detect_spanish_words(os.path.join(folder_name, file_name))
            else:
                pass
                #print("Skipping {}".format(file_name))

if __name__ == "__main__":
    # start time measure
    start = time.time()
    if len(sys.argv) == 2:
        process_folder(sys.argv[1])
    else:
        process_folder(".")
    #print_red("HELLO")
    # print time elapsed in seconds (rounded to 2 decimals)
    print("Time elapsed: {} seconds".format(round(time.time() - start,2)))