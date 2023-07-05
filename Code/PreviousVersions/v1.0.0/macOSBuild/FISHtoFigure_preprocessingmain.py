"""
Dataset Preparation for analysis by FISHtoFigure
Takes a series of image datasets from RNAScope experiment and returns a single concatanated dataset in csv and txt format
Main FISHtoFigure code currently takes a txt format input and the txt output of this script will suffice
"""

import csv
import re
import os
   
def run(rawdata_folder):

    infolder = rawdata_folder
    
    
    file_list = []                                              #list of file names as they appear in input directory
    files = []                                                  #list of file names without .txt extension, such that when converted to .csv filenames remain clear
    path_list = []                                              #list of paths to the files within file_list, these are all the .txt files in the input folder, make sure that the only .txt files in the input folder are Qupath output files
    file_indices = []                                           #list of file numbers (eg slice1, slice2, etc) this is used to maintain the z-stack order during processing
    
    for file in os.listdir(infolder):                           #creates a list of the files within the input folder to be analysed
        if file.endswith(".txt"):                               #non-txt files are ignored
            filename = repr(infolder + file).strip("'")         #generates a raw string equivilant of the input file path, neccessary due to characters used in the path having intrinsic unicode properties
            files.append(file)                                  #removes .txt extension and adds resulting file name to the shortened file names list "file_list_cut"
            file_indices.append(int(re.sub('\D', '', file)))    #Adds the file number (eg slice1, slice2, etc) to the list of file numbers
    file_indices.sort()                                         #Orders the list of file numbers in numerical ascending order, these can then be assigned to the relevant files to keep the z-stack in order
    files.sort()                                                #Added in macOS version such that files are ordered correctly to allow for split_string to be generated
    split_string = files[0].split("1", 1)
    substringa = split_string[0]
    substringb = split_string[1]
    
    print('List of files to concatenate:')
    for i in range(len(file_indices)):
        file_list.append(substringa + str(file_indices[i]) + substringb)
        path_list.append(infolder + substringa + str(file_indices[i]) + substringb)                             #creates a list of files in the directory in the correct order ready for analysis using the file numbers list created above
    print(path_list)                                                                                            #prints list of file paths to be analysed to the console
    
    lc = 0
    with open(f'{infolder}/Concatanated Dataset.csv', 'w', newline = '') as out_file:                          #creates a csv file for the current dataset
        for i in range (len(path_list)):                                                                        #this loop creates the csv file equivilants for the qupath datasets
            with open(path_list[i], 'r') as in_file:
                stripped = (line.strip() for line in in_file)                                                   #removes any excess white space in the qupath output which could affect conversion to csv file
                lines = (line.split("\t") for line in stripped if line)                                         #sets tab (shown here as \t) as the delimiter (the character seperating dataset entries we want to be sepearted by a comma in our csv file)
                if lc == 0:
                    writer = csv.writer(out_file)                                                               #writes the qupath .txt dataset to the newly created csv file
                    writer.writerows(lines)
                    lc += 1
                else:
                    next(lines, None)
                    writer = csv.writer(out_file)                                                               #writes the qupath .txt dataset to the newly created csv file
                    writer.writerows(lines)
                
    
    
    lc = 0
    with open(f'{infolder}/Concatanated Dataset.txt', 'w', newline = '') as out_file:                          #creates a csv file for the current dataset
        for i in range (len(path_list)):                                                                        #this loop creates the csv file equivilants for the qupath datasets
            with open(path_list[i], 'r') as in_file:
                stripped = (line.strip() for line in in_file)                                                   #removes any excess white space in the qupath output which could affect conversion to csv file
                lines = (line.split("\t") for line in stripped if line)                                         #sets tab (shown here as \t) as the delimiter (the character seperating dataset entries we want to be sepearted by a comma in our csv file)
                if lc == 0:
                    writer = csv.writer(out_file, delimiter = "\t")                                             #writes the qupath .txt dataset to the newly created csv file
                    writer.writerows(lines)
                    lc += 1
                else:
                    next(lines, None)
                    writer = csv.writer(out_file, delimiter = "\t")                                             #writes the qupath .txt dataset to the newly created csv file
                    writer.writerows(lines)
