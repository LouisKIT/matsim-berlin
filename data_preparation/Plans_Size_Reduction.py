# -*- coding: utf-8 -*-
"""
Created on Tue May 23 14:41:09 2023

@author: Rudi
"""

# Specify the path to the input XML file
input_file_path = "C:/Users/Rudi/Downloads/berlin-v5.5-10pct.plans.xml"

# Specify the path to the output XML file
output_file_path = "C:/Users/Rudi/Downloads/new.plans.xml"

print("Start reading lines")

# Read the input XML file and extract the first 10,000 lines
with open(input_file_path, 'r') as input_file:
    lines = []
    for line_number, line in enumerate(input_file, start=1):
        lines.append(line)

        if line_number % 100 == 0:
            print(f"Read {line_number} lines.")

        if line_number == 10000:
            break
        
print("Done reading lines")

# Write the extracted content to the output XML file
with open(output_file_path, 'w') as output_file:
    output_file.writelines(lines)
    
print("Done writing lines in new file")