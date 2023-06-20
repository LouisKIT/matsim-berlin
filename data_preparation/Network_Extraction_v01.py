# -*- coding: utf-8 -*-
"""
Created on Tue May 23 11:30:40 2023

@author: LK
"""

from pyproj import Proj, transform
import xml.etree.ElementTree as ET
from openpyxl import Workbook
import random
import os

"""Identify all nodes within that area"""
""""""
# Construct the file path using raw string or escaped backslashes
file_path = r'/home/louis/MA/Input_Preprocessed/berlin-drt-v5.5-1pct.output_network.xml'  # Using raw string

# Check if the file path exists & Parse the XML file
if os.path.isfile(file_path): 
    tree = ET.parse(file_path)
    root = tree.getroot()

else:
    print(f"File not found: {file_path}")

#empty list for all nodes in DRT Area, i = counter of nodes in DRT Area
link_list = []
i=0

# Iterate over each 'link' element in the XML
for link in root.findall('.//link'):
    # Get the value of the 'modes' attribute
    modes = link.get('modes')
    
    # Check if "drt" is present in the 'modes' attribute
    if "drt" in modes.split(","):
        link_list.append(link.get("id"))
        print("The 'modes' attribute includes 'drt' for link with ID:", link.get('id'))
        i=i+1
        print("node nr.: " + str(i))

# Create a new workbook and select the active sheet
wb = Workbook()
ws = wb.active

# Write data to node sheet
ws.title = "Links"
ws.append(['Link ID'])
for links in link_list:
    ws.append([links])

# Generate a random 10-digit number
rand_num = random.randint(1e9, 1e10-1)

# Change the directory to "/Input_Processed"
directory = "/home/louis/MA/Input_Processed"
os.makedirs(directory, exist_ok=True)
os.chdir(directory)

# Save the workbook based on the date
filename = 'drt_links.xlsx'
wb.save(filename)
print("Updated Excel saved")