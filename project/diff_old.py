import re
import os

def diff_files(file1, file2):
    with open(file1) as f1, open(file2) as f2:
        pre_lines = f1.readlines()
        post_lines = f2.readlines()

        # Ignore lines containing timestamp in format of hh:mm:ss or ##w##d##h
        timestamp_regex = re.compile(r'\b\d{1,2}:\d{1,2}:\d{1,2}\b|\d+w\d+d\d+h')
        pre_lines = [line for line in pre_lines if not timestamp_regex.search(line)]
        post_lines = [line for line in post_lines if not timestamp_regex.search(line)]

        diff = []
        for line_num, (pre_line, post_line) in enumerate(zip(pre_lines, post_lines)):
            if pre_line != post_line:
                diff.append(f'\n{file1}:{line_num+1}: {pre_line.rstrip()}\n{file2}:{line_num+1}: {post_line.rstrip()}\n')

        # Print the differences
        if len(diff) == 0:
            print(f"identical!!!\n")
            return

        for line in diff:
            print(line)