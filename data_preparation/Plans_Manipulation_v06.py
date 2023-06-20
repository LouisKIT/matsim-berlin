"""
Created on Tue May 23 16:21:45 2023

@author: LK
"""

import pandas as pd
import glob
import time
import os
import xml.etree.ElementTree as ET
import shutil
import random


"""Define Szenario"""
scenario = "1pct"
#scenario = "10pct"

"""Import Links (AV Zone) out of excel sheet"""
""""""

# Change the directory to "/Input_Processed"
directory = "/home/louis/MA/Input_Processed"
os.makedirs(directory, exist_ok=True)
os.chdir(directory)

#reused later to move the plans file into the Input_Processed folder
destination_dir = os.path.join(directory, scenario)

# Get a list of all Excel files in the current directory
excel_files = glob.glob('av_nodes_and_links.xlsx')

# If there is exactly one Excel file, read it
if len(excel_files) == 1:
    xls = pd.ExcelFile(excel_files[0])
else:
    print("There are either no Excel files or more than one Excel file in the current directory.")

# Read the second sheet into a DataFrame
df = xls.parse(xls.sheet_names[1])

# Convert the DataFrame to a list
link_list = df.astype(str).values.tolist()

#print(link_list)
print("")

# If the DataFrame consists of a single column, the list will be nested. Flatten it in this case:
if df.shape[1] == 1:
    link_list = [item for sublist in link_list for item in sublist]

""" Update leg mode in plans.xml based on links (AV Zone): car => AV; INCREMENTAL APPROACH TO SAVE MEMORY CAPACITY"""
""""""
print("initiate new xml creation...")

# Change the directory to "/Input_PreProcessed"
os.chdir(os.path.dirname(os.getcwd()))
directory = os.path.join("/home/louis/MA/Input_Preprocessed", scenario)
os.makedirs(directory, exist_ok=True)
os.chdir(directory)

current_directory = os.getcwd()
print("Current Directory:", current_directory)

p = 0

# Generate a random 10-digit number
rand_num = random.randint(1e9, 1e10-1)

filename = 'berlin-v5.5-' + scenario + f'_modified_{rand_num}.plans.xml'

old_filename = "berlin-v5.5-" + scenario + ".plans.xml"

with open(filename, 'w') as f:
    # Write the header
    f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('<!DOCTYPE population SYSTEM "http://www.matsim.org/files/dtd/population_v6.dtd">\n')
    f.write('\n')
    f.write('<population>\n')
    f.write('\n')
    f.write('\t<attributes>\n')
    f.write('\t\t<attribute name="coordinateReferenceSystem" class="java.lang.String">DHDN_GK4</attribute>\n')
    f.write('\t</attributes>\n')
    f.write('\n')
    f.write('\n')
    f.write('<!-- ====================================================================== -->\n')
    f.write('\n')
    f.write('\t')
    """
    for event, element in ET.iterparse(old_filename, events=('end',)):
        if element.tag == 'person':
            p += 1
            if p % 10000 == 0:
                print ("Nr.: " + str(p))
            legs = [elem for elem in element.iter() if elem.tag == 'leg' or elem.tag == 'activity']
            for i, leg in enumerate(legs):
                route = leg.find('.//route')
                if leg.get('mode') == 'car': 
                    start_link = str(route.get('start_link')) 
                    end_link = str(route.get('end_link')) 
                    route_links = route.text.split() if route.text else []  # Split the route text into a list
                    if start_link in link_list and end_link in link_list:
                        for leg2 in legs:
                            if leg2.get('mode') == 'car':
                                leg2.set('mode', 'drt')
                                attributes = element.findall('.//attribute[@name="routingMode"]')
                                for attribute in attributes:
                                    attribute.text = 'drt'
                                    print(f"Adjustment made at person id {element.get('id')}")
                                    time.sleep(10)
                            # Check if there is an activity element before the leg
                            if leg2.tag == 'activity' and leg2.get('type') == 'car interaction':
                                leg2.set('type', 'drt interaction')
                            
            # Write the modified person element and its descendants to the new file
            f.write(ET.tostring(element, encoding='unicode'))
        
            # Clear the element and its descendants from memory once it's written
            element.clear()
    """
    for event, element in ET.iterparse(old_filename, events=('end',)):
        if element.tag == 'person':
            p += 1
            if p % 10000 == 0:
                print("Nr.: " + str(p))
            
            # Find leg and activity elements
            legs = [elem for elem in element.iter() if elem.tag == 'leg' or elem.tag == 'activity']
            
            for i, leg in enumerate(legs):
                route = leg.find('.//route')
                
                # Check if leg mode is "car"
                if leg.get('mode') == 'car' and route.get('start_link') != route.get('end_link'):
                    # Update route "type" attribute to "drt"
                    leg.set('mode', 'drt')
                    attributes = element.findall('.//attribute[@name="routingMode"]')
                    for attribute in attributes:
                        attribute.text = 'drt'
                    route.set('type', 'drt')
                    route.attrib.pop('vehicleRefId', None)
                    # Remove existing text inside route element
                    route.text = None
                    
                    # Add new text inside route element
                    route.text = '300.0 208.7665374999924'
                    print(str(p) + " updated")
                # Check if there is an activity element before the leg
                if leg.tag == 'activity' and leg.get('type') == 'car interaction':
                    leg.set('type', 'drt interaction')

            # Write the modified person element and its descendants to the new file
            f.write(ET.tostring(element, encoding='unicode'))

            # Clear the element and its descendants from memory once it's written
            element.clear()

    # Write the root element end tag manually
    f.write('</population>\n')

print("plans file for scenario " + scenario + " updated")

# Construct the source and destination paths
source_path = os.path.join(directory, filename)
new_filename = "berlin-v5.5-" + scenario + ".plans.xml"
destination_path = os.path.join(destination_dir, new_filename)

# Move the file
shutil.move(source_path, destination_path, copy_function=shutil.copy2)