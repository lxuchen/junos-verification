import difflib
import re
import os


def ignore_timestamps(line):
    """Helper function to ignore lines containing timestamps"""
    return not re.search(r'(\d{2}:){2}\d{2}|\d+w\d+d\d+h', line)

def diff_files(file1, file2):
    print(f"\nComparing {file1}, {file2} and results are...\n")
    """Compare two files, ignoring lines with timestamps"""
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        diff = difflib.unified_diff(f1.readlines(), f2.readlines(), n=0)
        # Filter out lines with timestamps
        diff = filter(ignore_timestamps, diff)
        # Join the remaining lines into a single string
        diff_str = ''.join(diff)
        print(diff_str)

# Example usage
# file1 = 'tmp/router_1_pre.output'
# file2 = 'tmp/router_2_post.output'
# diff_str = diff_files(file1, file2)
# print(diff_str)
