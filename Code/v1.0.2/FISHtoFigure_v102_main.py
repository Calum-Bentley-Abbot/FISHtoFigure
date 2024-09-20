# -*- coding: utf-8 -*-
"""
Main program file for FISHtoFigure
"""

import csv
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from contextlib import redirect_stdout

from matplotlib.patches import Patch

plt.rcParams['figure.dpi'] = 600
plt.rcParams['savefig.dpi'] = 600

def run(input_folder, hist, scatter, thresh, expression, dubposA, dubposAchans, dubposAthresh, dubposB, dubposBchans, dubposBthresh, chan_headers, dataset_labels):

    #ASSIGNS USER INPUTS FROM GUI SCRIPT TO VARIABLES USED BELOW
    
    infolder = input_folder

    Plot_Spot_Histogram = hist

    Plot_Spot_Map = scatter
    
    Plot_RNA_expression = expression
    
    Plot_dubposA = dubposA
    #Double positive channels
    dubposA_channels = dubposAchans.split(", ")
    
    Plot_dubposB = dubposB
    #Double positive channels
    dubposB_channels = dubposBchans.split(", ")
    
    threshold = int(thresh)
    dubposA_threshold = int(dubposAthresh)
    dubposB_threshold = int(dubposBthresh)
    
    #Labels for channels and datasets
    col_labels = chan_headers.split(", ")               #Creates a list from the user input string of channel names
    
    col_labels_spots = [s + " Spots" for s in col_labels]
    col_labels_clusters = [s + " Clusters" for s in col_labels]
    
    datasetlabels = dataset_labels.split(", ")          #Creates a list from the user input string of dataset names
    
    #SETTING GENERAL PLOTTING PARAMETERS FOR SEABORN AND MATPLOTLIB
    #Creating a custom colour palette
    colours = ["#FFFFFF", "#808080", "#E69F00", "#56B4E9", "#009E73", "#CC79A7", "#F0E442", "#0072B2", "#D55E00"]   
    sns.set_palette(sns.color_palette(colours))
    
    #Setting box plot visual parameters
    plt.rc("axes.spines", top=False, right=False)
    PROPS = {
    'boxprops':{'edgecolor':'black'},
    'medianprops':{'color':'black'},
    'whiskerprops':{'color':'black'},
    'capprops':{'color':'black'}
    }
    
    #Creating custom legend parameters
    custom_lines = [Patch(ec = "Black", fc=colours[i], lw = 1) for i in range(len(datasetlabels))]
    
    #Setting text font sizes for figures
    plt.rc('font', size=15)
    plt.rc('axes', titlesize=15)
    plt.rc('axes', labelsize=15)
    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)
    plt.rc('legend', fontsize=12)
    plt.rc('figure', titlesize=14)
    plt.rcParams['axes.titley'] = 1.07


    #GENERATING RELEVANT LISTS AND DIRECTORIES USED THROUGHOUT SCRIPT FOR CUMMULATIVELY STORING DATA FROM MULTIPLE DATASETS AND OUTPUT OF ANALYSIS
    #Creating lists for multi-dataset information
    
    spotcount_tot = []
    intensity_tot = []
    poscells = []
    poscells_tot = []
    allcells = []
    
    dubposAspot_tot = []
    dubposAnum = []
    dubposAnum_tot = []
    dubposAintensity_tot = []
    
    dubposBspot_tot = []
    dubposBnum = []
    dubposBnum_tot = []
    dubposBintensity_tot = []
    
    line_count = 0

    #Creation (or assignment if pre-existing) of output directories for converted csv files and pipeline output
    
    try:
        os.mkdir(f'{infolder}csv files\\')                      #if "csv files" directory does not already exist within the input directory then it is created and will be used for storage of converted csv files 
    except:
        pass                                                    #if "csv files" directory already exists, do nothing (this will still be used as the storage location for converted csv files)
    try:
        os.mkdir(f'{infolder}F2F output\\')                #same as above but for the generation of a output directory for the pipeline, console output (cellular transcript information and basic analysis) and non-zero spot/cluster count information for each dataset will be saved here
    except:
        pass
    output_folder = f'{infolder}F2F output\\'              #sets output destination
    
    
    
    
    
    #FILE CONVERSION FROM QUPATH .TXT OUTPUT TO .CSV FILE FOR PIPELINE INTERPRETATION
    #Segmenting input dataset names to preserve "human order" of files when passed to the pipline
    
    file_list = []                                              #list to contain file names as they appear in input directory
    files = []                                                  #list to caontain file names without .txt extension, such that when converted to .csv filenames remain clear
    path_list = []                                              #list to contain paths to the files within file_list, these are all the .txt files in the input folder, make sure that the only .txt files in the input folder are Qupath output files
    file_indices = []                                           #list to contain file numbers (eg slice1, slice2, etc) this is used to maintain the order of input datasets during processing
    
    for file in os.listdir(infolder):                           #creates a list of the files within the input folder to be analysed
        if file.endswith(".txt"):                               #non-txt files are ignored
            filename = repr(infolder + file).strip("'")         #generates a raw string equivilant of the input file path, neccessary due to characters used in the path having intrinsic unicode properties
            files.append(file)                                  
            file_indices.append(int(re.sub('\D', '', file)))    #Adds the file number (eg slice1, slice2, etc) to the list of file numbers
    file_indices.sort()                                         #Orders the list of file numbers in numerical ascending order, these can then be assigned to the relevant files to keep the datasets in order
    split_string = files[0].split("1", 1)                       #creates two string, one from the start of the dataset name (before the digit signifying which dataset this is), one from the end (e.g. the file extension), these are used to preserve input dataset order below
    substringa = split_string[0]                                #First part of dataset name
    substringb = split_string[1]                                #Second part of dataset name
    
    #Generating and printing the correctly ordered input dataset list to the console 
    
    print('List of files to be analysed:')
    for i in range(len(file_indices)):
        file_list.append(substringa + str(file_indices[i]) + substringb)                #creates a correctly ordered list of the datasets being passed to the pipeline
        path_list.append(infolder + substringa + str(file_indices[i]) + substringb)     #creates a list of files in the correct order by using the file numbers list and segmented dataset name created above
    print(path_list)                                                                    #prints list of file paths to be analysed to the console
    
    #csv file conversion
    
    for i in range (len(path_list)):                                                                    #this loop creates the csv file equivilants for the qupath datasets
        with open(path_list[i], 'r') as in_file:
            stripped = (line.strip() for line in in_file)                                               #removes any excess white space in the qupath output which could affect conversion to csv file
            lines = (line.split("\t") for line in stripped if line)                                     #sets tab (shown here as \t) as the delimiter (the character seperating dataset entries we want to be sepearted by a comma in our csv file)
            with open(f'{infolder}csv files\\{file_list[i]}.csv', 'w', newline = '') as out_file:       #creates a csv file for the current dataset in the csv files directory created above
                writer = csv.writer(out_file)                                                           #writes the qupath .txt dataset to the newly created csv file
                writer.writerows(lines)
    
    
    #Normalising channel number across all images (see user guide for details)
    
    for i in range (len(path_list)):
        with open(f'{infolder}csv files\\{file_list[i]}.csv', 'r') as in_file:
            df = pd.read_csv(in_file)
            df.fillna(0, inplace=True)
            out_file = f'{infolder}csv files\\{file_list[i]}.csv'
            df.to_csv(out_file, index = False)                                             #writes the qupath .txt dataset to the newly created csv file

    infolder = f'{infolder}csv files\\'                                                                 #change input folder to the directory containing the newly created csv files corresponding to each dataset
    
    
    
    
    
    #ESTABLISHING OUTPUT FILE AND REDIRECTING CONSOLE OUTPUT FOR LOGGING ROI AND SPOT/CLUSTER INFORMATION
    
    with open(f'{output_folder}Analysis Ouput.txt', 'w') as f:                  #creates a file in the output folder for the console output (this contains non-zero spot/cluster count cellular information as well as basic analysis such as mean spot counts and percentage cell RNA expression)
        with redirect_stdout(f):                                                                    #redirects the console output to newly created file
            path_list = []                                                                          #refreshed path list, the information contained from previous loops is no longer needed so we can reuse this rather than create another variable
            
            for i in range(len(file_indices)):
                path_list.append(infolder + substringa + str(file_indices[i]) + substringb + '.csv')        #same as for above for .txt path list created above but for .csv files
            
            print('List of files to be analysed:')                                                          #prints a list of the input files to the console output file created above
            print(file_list)
            print("___________________________________________________________")

            #LOADING AN INPUT FILE AND ESTABLISHING HEADERS RELATING TO COLUMNS OF INTEREST (SPOTS, CLUSTERS, INTENSITY INFORMATION)
            
            for a in range(len(path_list)):                                                                             #cycles through csv files created above, this constitutes the main loop for the script
                input_file = path_list[a]                                                                               #assigns the current file being analysed
                print("The input file is:")
                print(input_file)
                with open(input_file) as file:                                                                          #Opens the current file
                    data_in = list(csv.reader(file, delimiter = ','))                                                   #This creates a series of lists, each list is a row from the dataset
                    headers = data_in[0]                                                                                #Creates a list of the headers for the columns in your dataset from the first line in the dataset
                    
                    print(f"Beginning analysis of file: {path_list[a]}")
                    print("___________________________________________________________")
            
                    #Establishing the columns containing ROI centroid coordinates and spot and cluster information

                    req_cols = []                                                                                               #Here, the headers list created earlier will be used to find columns of interest in the dataset (e.g. Channel 1 Num Clusters), for now these are just empty lists this information will be contained in.
                    req_headers = []                                                                                            
                    spot_headers = []
                    spot_cols = []                                                                                      
                    cluster_headers = []
                    cluster_cols = []
                    intensity_headers = []
                    intensity_cols = []
                    for header in headers:                                                                                      #Cycles through all headers in the creted headers list
                        if re.search('Name', header):
                            name_index = headers.index(header)                       
                        elif re.search('Nucleus: Area', header):
                            NucleusArea_index = headers.index(header)                        
                        elif re.search('Centroid X.+', header):                                                                   #searches the headers list for names of columsn of interest
                            x_centroids_index = headers.index(header)                                                           #Here the scrpit finds the index of the centroid data columns in the dataset, these will be used for identifying ROIs
                        elif re.search('Centroid Y.+', header):
                            y_centroids_index = headers.index(header)
                        elif re.search('Subcellular.+', header):                                                                #Searches the headers list for those containing the given string shown in parenthesis
                            if re.search('.+ estimated', header):                                                               #skips the estimated spot/cluster count for each channel
                                print(f"Skipped header: {header}")                                                              #message to inform user of which columns have been skipped
                            elif re.search('.+ Area', header):                                                                  #skips channel area columns
                                print(f"Skipped header: {header}")
                            else:
                                req_cols.append(headers.index(header))                                                          #Adds the index of the relevant columns to the list created above
                                req_headers.append(header)                                                                      #Adds the name of the relevant header to the list made above
                                if re.search('.+ spots', header):
                                    spot_headers.append(header)
                                    spot_cols.append(headers.index(header)) 
                                elif re.search('.+ clusters', header):
                                    cluster_headers.append(header)
                                    cluster_cols.append(headers.index(header))
                                elif re.search('.+ intensity', header):
                                    intensity_headers.append(header)
                                    intensity_cols.append(headers.index(header))
                
                
                
                
                #CHECKING WHETHER ALL CHANNELS HAVE NON-ZERO FLUORESCENCE (See user manual for why this is important)
                
                if len(intensity_headers) != len(spot_headers):
                    newline = "\n"
                    print(f"______________________________{newline} WARNING: {newline}One or more channels have zero intensity. Therefore some analysis options could not be performed.{newline}Please see user manual for further instructions.{newline}______________________________")
                    channel_consistency = 0
                else:
                    channel_consistency = 1
                
                



                print(f"Indices of required columns: {req_cols}")                                                           #Prints the list containing the indices of columns of interst for checking against input dataset
                print(f"List of required headers: {req_headers}")                                                           #Prints the headers of relevant columns for use later
                print("___________________________________________________________")

                #ESTABLISHING FURTHER VARIABLES FOR DATASET ANALYSIS    
                #Creates lists of centroid data for all cells
                
                x_centroids = []                                                                                            #Creates a pair of empty lists which will store centroid data
                y_centroids = []  
                
                for row in data_in:
                    try:                            
                        float(row[x_centroids_index])                                                                       #Here we check whether the value in the centroid columns in this row is a numerical values, in which case we add them to the lists created above, if not we discard them. This eliminates headers.
                        x_centroids.append(float(row[x_centroids_index]))
                    except ValueError:                                                                                      #This part discards non-numerical values
                        pass
                    try:
                        float(row[y_centroids_index])                                                                       #Same as above for Y centroids
                        y_centroids.append(float(row[y_centroids_index]))
                    except ValueError:
                        pass
                    
                    
                    
                    
                        
                #CELLULAR SPOT AND CLUSTER DATA ANALYSIS FOR CURRENT DATASET
                        
                spot_data = []                                                                                  #Generates an empty list to hold our spot data
                spot_lc = int()                                                                                 #Here, we implement a system to remove only the header but non the NaN values         
                for col in spot_cols:                                                                           #Iterates over each channel in our dataset
                        spot_innerlist=[]                                                                       #Sets up an internal list to store data gathered during each iteration of the loop (one channel's data) which will be appended to the final list before iterating over the next channel, thus building up a list containing a series of lists, each corresponding to a channel
                        for row in data_in:                                                                     #Iterates over each row in the input data
                            try:                                                                                #Basically same as for centroid data, eliminates non-numcerical values and stores spot data in created list
                                int(row[col])
                                spot_innerlist.append(int(row[col]))
                            except ValueError:
                                if spot_lc == 0:
                                    pass
                                    spot_lc += 1
                                else:
                                    spot_innerlist.append(0)                                                    #When encoutering a NaN value (or a non-integer), the script instead appends a 0 which can be used without error in later analysis.
                        spot_data.append(spot_innerlist)                                                        #appends internal list to spot_data list
                        spot_lc = 0
                
                cluster_lc = int()     
                cluster_data = []                                                                               #Sames as above but for cluster data rather than spot data
                for col in cluster_cols:
                        cluster_innerlist=[]
                        for row in data_in:    
                            try:
                                int(row[col])
                                cluster_innerlist.append(int(row[col]))
                            except ValueError:
                                if cluster_lc == 0:
                                    pass
                                    cluster_lc += 1
                                else:
                                    cluster_innerlist.append(0)
                        cluster_data.append(cluster_innerlist)
                        cluster_lc = 0
                 
                    
                 
                    
 
                #SUBCELLULAR INTENSITY DATA AND SUM CALCULATIONS FOR CURRENT DATASET
                #Ordering intensity column headers as they appear to be randomly ordered in the input dataset and change sporadically based on unknown elements of pre-pipeline analysis
                
                intensitysorter = []                                                            #creates a list to store our ordered column headers/indices
                for i in range(len(intensity_cols)):                                            #adds each header to the list with the associated index
                    intensitysorter.append(f"{intensity_headers[i]} ={str(intensity_cols[i])}")
                
                def digitgrabber(text):                                                         #returns an input as an integer if possible  
                    return int(text) if text.isdigit() else text
    
                def natural_keys(text):
                    return [digitgrabber(c) for c in re.split(r'(\d+)', text)]                  #splits each string entry in the intensitysorter list about the digit (channel number), and runs the digitgrabber function to find the channel number
                sorteditems = intensitysorter.sort(key=natural_keys)                            #orders our headers/indices list by channel number by reference to the above functions, thus putting the indices in the correct channel order
                
                intensity_cols_sorted = []
                for i in intensitysorter:                                                       #removes the header from the newly sorted list leaving the indices only such that they can be used in channel order
                    column = re.sub(r'^.*?=', '', i)
                    intensity_cols_sorted.append(int(column))

                
                #Storing subcellular intensity data by channel
                
                subcell_intensity = []                                                          #Creates list to store the intensity data for the current cell in the current channel
                subcell_intensity_temp=[]                                                       #Will store a list of lists, each list containing one cell's intensity data (With NaN values still in place)
                for i in range(len(intensity_cols_sorted)):                                     #This creates the list of lists, each internal list of numerical elements contains information about a particular cell. Each numerical element is the intensity for each subcellular spot in that cell. Lists containing channel headers seperate each set of cellular spot information lists by channel
                    cell_numerator = 0                                                          #A value to keep track of which cell we are currently investigating, gets reset everytime we encounter a new channel
                    for row in data_in:                                                         #Here, we iterate over the rows in our dataset, the dataset is structured such that a row contains information relating to a cell, then subsequent rows contain information relating to any subcellular spots/clusters in that cell until all subcellular objects have been reported when the next row then pertains to the next cell, thus we refer here to data_in since the output data proccessed above contains only cellular rows and eliminated subcellular information.
                        if row[name_index] == 'PathCellObject':                                          #If the row represents a cell rather than a subcellular object
                            subcell_intensity_temp.append(subcell_intensity)                    #we first add the spot intensity from the previous iteration of the loop
                            if cell_numerator == 0:                                             #After moving to a new channel, before we append the first cells information, we add the channel name so we can keep track of the cellular information relating to a given channel
                               subcell_intensity_temp.append([col_labels[i]])                   #Adds said channel name
                            cell_numerator += 1                                                 #Increaes the cell number everytime we encoutner a new cell (PathCellObject)
                            subcell_intensity = []                                              #each new cell encoutered resets the list we use for storing the subcellular spot information for a given cell
                        elif row[name_index].startswith("Subcellular spot:"):                            #Since subcellular rows can contain either spot information or cluster information this provides a filter to remove any rows containing cluster information.
                            try:                                                                #for rows representing subcellular spots rather than cells we add the information for that row to the list emptied above
                                subcell_intensity.append(float(row[intensity_cols_sorted[i]]))  #this creates a list of elements, each of which is the intensity of a particular spot in the cell 
                            except ValueError:                                                  #eliminates headers of columns from our list
                                pass        
                        elif row[name_index] == '0.0':                                              #Failsafe for QuPath output data which contains a blank Name column, unsure of the cause of this blank column however, this block serves the same purpose
                            if row[NucleusArea_index] != '0.0':                                     #Nucleus:Area column is expected to be populated for all QuPath data using DAPI as a cell marker, since this is required for F2F analysis, this should never not work
                                subcell_intensity_temp.append(subcell_intensity)                    #we first add the spot intensity from the previous iteration of the loop
                                if cell_numerator == 0:                                             #After moving to a new channel, before we append the first cells information, we add the channel name so we can keep track of the cellular information relating to a given channel
                                   subcell_intensity_temp.append([col_labels[i]])                   #Adds said channel name
                                cell_numerator += 1                                                 #Increaes the cell number everytime we encoutner a new cell (PathCellObject)
                                subcell_intensity = []
                            else:
                                try:                                                                #for rows representing subcellular spots rather than cells we add the information for that row to the list emptied above
                                    subcell_intensity.append(float(row[intensity_cols_sorted[i]]))  #this creates a list of elements, each of which is the intensity of a particular spot in the cell 
                                except ValueError:                                                  #eliminates headers of columns from our list
                                    pass
                
                
                subcell_intensity_temp.append(subcell_intensity)                                #adds the list we have just created for the cell to our list of lists, thus creating a list of cell-lists, each of which contains a series of values relating to the intensities of individual subcellular objects
                del subcell_intensity_temp[0]                                                   #removes initial empty list (artifact of adding previous loops data to the list of lists at the start of the loop)
                
                #Replaces any NaN values with 0 such that sums can be calculated
    
                subcell_intensity_list = []                                                     #Will become a list which is the same as subcell_intensity_temp but with NaN values replaced with 0 for calculation and plotting
                for i in subcell_intensity_temp:                                                #loops through each cell's data
                    i = pd.Series(i, dtype = object).fillna(0).tolist()                         #replaces NaN values with 0
                    subcell_intensity_list.append(i)                                            #adds each replaced list to the list created above
                
                #Calculating total intensity per cell from sum of subcellular intensity objects
                
                cell_intensity_list = []                                                        #This will create a list of lists, each sublist represents a channel, each value in said sublist represents the total intensity for a cell in that channel
                cell_intensity_innerlist = []                                                   #Here we create a list which will store the total intensities (sum of subcellular element intensities) for each given cell per channel
                for i in subcell_intensity_list:                                                #Iterates over our list of subcellular elements created above
                    try:
                        cell_intensity_innerlist.append(sum(i))                                 #Adds sum of subcellular elements for a given cell to the innerlist, thus creating a data point for the total intensity of that cell
                    except TypeError:
                        cell_intensity_list.append(cell_intensity_innerlist)                    #when reaching a new channel header in the subcellular list this appends the innerlist to the list of lists, thus creating a sublist for each channel's information (this causes an error due to the fact that the channel name cannot be summed, so this error is used as a flag for a new channel) 
                        cell_intensity_innerlist = []                                           #resets the inner list for use in the next channels data collection
                cell_intensity_list.append(cell_intensity_innerlist)                            #appends the final dataset from the last channel, this would otherwise not be appended since there is no channel name to be encountered at the end of the final channel, thus no error, thus no append of the innerlist to the final list
                del cell_intensity_list[0]                                                      #Gets rid of empty list added to the start of the list of lists, this is an artifact like above.
                
                print(cell_intensity_list)
                
                #Reshaping cellular intensity dataframe for plotting purposes
                
                df = pd.DataFrame(cell_intensity_list)                                          #Stores the list of lists relating to the total cellular intensities for each cell in each channel as a dataframe
                dfi = df.transpose()                                                            #Creating dataframes from lists results in each innerlist forming a row in the dataframe, since here each list represents a channel we must transpose the dataframe such that channel are instead represented by columns and each row represents a cell.
                for i in range(len(col_labels)):                                                #Loop to rename columns based on user inputted channel names
                    dfi.rename(columns = {i:col_labels[i]}, inplace = True)
                dfi["Dataset"] = datasetlabels[a]                                               #Adds a column to the dataframe containing the user specified dataset name
                
                if channel_consistency == 1:
                    #Calculating total intensities per channel
        
                    intensitytot_innerlist = []
                    for i in col_labels:                                                            #creates list of lists
                        intensitytot_innerlist.append(dfi[i].sum())                                 #each list represents a dataset (input file)
                    intensitytot_innerlist.append(datasetlabels[a])                                 #within each of those lists the values are the total intensity of each spot channel
                    intensity_tot.append(intensitytot_innerlist)
                    
                
                
                #WRITING CELLULAR INFORMATIONTO NEW FILE
                
                output_file = output_folder + datasetlabels[a] + ' output.csv'                                       #creates a file to which the script will write the processed dataset to with the user defined path.
                w = open(output_file, 'w', newline = '')                                                                #opens the created output file to write to
                csv_writer = csv.writer(w)
                lc = 1           
                objects_seen = []                                                                                       #Creates a list for storing the centroids of objects to remove duplicates in the new file    
                for row in data_in:                                                                                     #This loop writes the headers to the new file
                    if lc == 0:
                        csv_writer.writerow(data_in[0])
                        lc += 1
                    else:                                                                                               #This loop writes the data to the new file based on the data in the relevant columns determined above
                        if row[name_index] == 'PathCellObject':                                                                  #Eliminates any subcellular rows, these are processed below seperately
                            csv_writer.writerow(row)
                            lc += 1
                        elif row[name_index] == '0.0':
                            csv_writer.writerow(row)
                            lc += 1
                
                allcells.append([lc, datasetlabels[a]])
                
                #WRITING NON-ZERO CELL INFORMATION TO NEW FILE
                
                output_file = output_folder + datasetlabels[a] + ' nonzero_output.csv'                                       #creates a file to which the script will write the processed dataset to with the user defined path.
                w = open(output_file, 'w', newline = '')                                                                #opens the created output file to write to
                csv_writer = csv.writer(w)
                lc = 0           
                objects_seen = []                                                                                       #Creates a list for storing the centroids of objects to remove duplicates in the new file    
                for row in data_in:                                                                                     #This loop writes the headers to the new file
                    if lc == 0:
                        csv_writer.writerow(data_in[0])
                        lc += 1
                    else:                                                                                               #This loop writes the data to the new file based on the data in the relevant columns determined above
                        if row[name_index] == 'PathCellObject':                                                                  #Eliminates any subcellular rows, these are processed below seperately
                            for i in req_cols:
                                if row[i] != '0' and row[i] != 'NaN' and row[i] != '0.0':                                                   #Eliminates any rows in which all columns of interest contain no data
                                    if row[x_centroids_index] not in objects_seen:                                      #Refers to the list of already copied objects such that rows are not duplicated if they have multiple relevant columns which contain information
                                        csv_writer.writerow(row)                                                        #Writes the current row to the new file
                                        objects_seen.append(row[x_centroids_index])                                     #Adds the copied object to the seen objects list for later referral
                                    else:
                                        print(f'Cell with centroid at x={row[x_centroids_index]} already written to file, cell skipped')    #If the object's centroid is logged in the objects_seen list, this prints a message to let you know its been skipped
                        if row[name_index] == '0.0':                                                                  #Eliminates any subcellular rows, these are processed below seperately
                            for i in req_cols:
                                if row[i] != '0' and row[i] != 'NaN' and row[i] != '0.0':                                                   #Eliminates any rows in which all columns of interest contain no data
                                    if row[x_centroids_index] not in objects_seen:                                      #Refers to the list of already copied objects such that rows are not duplicated if they have multiple relevant columns which contain information
                                        csv_writer.writerow(row)                                                        #Writes the current row to the new file
                                        objects_seen.append(row[x_centroids_index])                                     #Adds the copied object to the seen objects list for later referral
                                    else:
                                        print(f'Cell with centroid at x={row[x_centroids_index]} already written to file, cell skipped')    #If the object's centroid is logged in the objects_seen list, this prints a message to let you know its been skipped

                w.close()
                print("_______________________________________________________________")
            
            
            
            
            
                #CALUCULATING AND OUTPUTTING ROI AND GENERAL DATASET ANALYSIS FOR CLUSTERS AND SPOTS TO THE PIPELINE OUTPUT FILE
                #Printing non-zero cell information to ouput file in pipeline output folder
                
                print(f'Dataset {a+1} Regions of Interest:')    
                print("_______________________________________________________________")
                print("Output Format:")
                r = open(output_file,'r')                                                                                                   #Opens the new file created above containing the processed non-zero data and initialises csv reader for this file
                csv_reader = csv.reader(r, delimiter = ',')    
                data_out = list(csv_reader)                                                                                                 #This creates a series of lists, each list is a row from your dataset 
                for row in data_out:                                                                                                        #Prints information about the centroid of the ROI to which the following information pertains for ease of comprehension
                    print(f"Cell with centroid: {row[x_centroids_index]}, {row[y_centroids_index]}")
                    for i in spot_cols:                                                                                                     #Prints the information relating to spots for this ROI
                        print(f"{col_labels_spots[spot_cols.index(i)]} = {row[i]}")
                    for i in cluster_cols:                                                                                                  #Prints the cluster information relating to this ROI
                        print(f"{col_labels_clusters[cluster_cols.index(i)]} = {row[i]}")
                    print("End of Cell")
                    print("___________________________________________________________")                                                    #Simply prints a line to seperate information on ROIs
                print(f"Dataset {a+1} Transcript Expression Analysis")
                
                #Calculating percentage of cells with non-zero spot counts
                
                nz_cell_percentage = ((len(data_out)-1)/(len(data_in)-1))*100                                                               #Here, len(x) is just the length of a list, in this case this is just the list of rows in the raw input data and the processed (non-zero) data, so this just takes a ratio of the lengths of the rows in the two files, thus giving non-zero cell percentage
                
                print(f"Percentage of cells with non-zero transcript count = {nz_cell_percentage}%")
            
                #Calculating mean number of spots and clusters per cell
                
                total_spots = (len(data_in)-1)*(len(spot_cols))                                                                             #Calculate cummulative number of cells in all channels                                                             
                nz_spots = (len(data_out)-1)*(len(spot_cols))                                                                               #Calculate cummulative number of cells with non-zero spot/cluster counts in all channels
                nz_spot_count = []
                for row in data_out:                                                                                                        #Same as previous loops for collecting spot and cluster data, but here we collect all non-zero spot values
                        for col_index in spot_cols:
                            try:
                                float(row[col_index])
                                nz_spot_count.append(float(row[col_index]))
                            except ValueError:
                                pass
                nz_spot_total = sum(nz_spot_count)                                                                                          #Returns total number of spots across all cells in dataset    
                nz_mean_spot_count = nz_spot_total/nz_spots                                                                                 #Calculates mean spot counts, for both the non-zero cells and the total cells
                total_mean_spot_count = nz_spot_total/total_spots
                
                
                nz_cluster_count = []                                                                                                       #Same as above for clusters
                for row in data_out:
                        for col_index in cluster_cols:
                            try:
                                float(row[col_index])
                                nz_cluster_count.append(float(row[col_index]))
                            except ValueError:
                                pass
                nz_cluster_total = sum(nz_cluster_count)
                nz_mean_cluster_count = nz_cluster_total/nz_spots
                total_mean_cluster_count = nz_cluster_total/total_spots
                
                #Print holistic spot and cluster analysis for this dataset to output file in pipeline output folder
                
                print(f"Mean transcript count in non-zero cells = {nz_mean_spot_count}")                                                  
                #print(f"Mean cluster count in non-zero cells = {nz_mean_cluster_count}")
                print(f"Mean transcript count in all cells = {total_mean_spot_count}")
                #print(f"Mean cluster count in all cells = {total_mean_cluster_count}")
                
                print("___________________________________________________________")
                print(f'End of analysis of file: {path_list[a]}')
                print("___________________________________________________________")
                
                
                
                
                
                #PARTITIONING DATA AND CREATION OF ASSOCIATED DATAFRAMES
                #Storing file information as a dataframe, columns will be preserved from input csv, as such can be called using same indices (spot_cols/cluster_cols)
                
                dfinheaders = data_in.pop(0)                                                    #Defines first row in data_in as the headers which will be used for the columns in the dataframe created below                            
                dfinheaders[x_centroids_index] = "X Centroids"                                  #Renames headers for centroid data to something easier to call without unusual characters
                dfinheaders[y_centroids_index] = "Y Centroids"
                dfin = pd.DataFrame(data_in, columns = dfinheaders)                             #Here, a dataframe for the raw input data is created
                dfin["Dataset"] = datasetlabels[a]                                              #Appends a column to the dataframe containing the dataset name
                
                dfoutheaders = data_out.pop(0)                                                  #Same as aobove for the processed output data
                dfoutheaders[x_centroids_index] = "X Centroids"
                dfoutheaders[y_centroids_index] = "Y Centroids"
                dfout = pd.DataFrame(data_out, columns = dfoutheaders)
                dfout["Dataset"] = datasetlabels[a]
                
                dfin = dfin.replace({'NaN': '0'}, regex=True)                                   #Removes Nan values from input dataframe
                dfin[spot_headers] = dfin[spot_headers].astype(float)
                dfin[spot_headers] = dfin[spot_headers].astype(int)                             #Changes values in the input data from strings to integers for the appropriate columns of interst
                dfin[cluster_headers] = dfin[cluster_headers].astype(float)
                dfin[cluster_headers] = dfin[cluster_headers].astype(int)
                dfin["X Centroids"] = dfin["X Centroids"].astype(float)                         #Changes values in appropriate columns of interest from strings to floats
                dfin["Y Centroids"] = dfin["Y Centroids"].astype(float)
                                
                dfout = dfout.replace({'NaN': '0'}, regex=True)                                 #Same as above but for procewssed output data
                dfout[spot_headers] = dfout[spot_headers].astype(float)
                dfout[spot_headers] = dfout[spot_headers].astype(int)
                dfout[cluster_headers] = dfout[cluster_headers].astype(float)
                dfout[cluster_headers] = dfout[cluster_headers].astype(int)
                dfout["X Centroids"] = dfout["X Centroids"].astype(float)
                dfout["Y Centroids"] = dfout["Y Centroids"].astype(float)
                for i in range(len(spot_headers)):                                              #Renames spot columns using channel names provided by user
                    dfout.rename(columns = {spot_headers[i]:col_labels_spots[i]}, inplace = True)
                                
                #Construct sub dataframes for box plot data, this is so we can create another dataframe with the data from each dataset concatanated into it

                dfs = dfout[col_labels_spots]                                               #Creates a dataframe containing only the data from spot columns in the processed output data       
                dfs = pd.concat([dfs, dfout["Dataset"]], axis = 1)                              #Adds dataset label cloumn as above

                #Calculating number of spots per channel
                
                spotcount_innerlist = []
                for i in col_labels_spots:                                          
                    spotcount_innerlist.append(dfs[i].sum())                                    #each list represents a dataset (input file)
                spotcount_innerlist.append(datasetlabels[a])                                    #within each of those lists the values are the total count of each spot channel
                spotcount_tot.append(spotcount_innerlist)                                       #Appends total spot count per channel information to multi-dataset list, each innerlist represents a dataset

                #Calculating number of positive cells per channel
                
                poscells_innerlist = []                                     
                for i in col_labels_spots:                                                            #each innerlist contains the number of spot-positive cells in each channel in that dataset       
                    poscells_innerlist.append(len(dfs[dfs[i] != 0]))                            #appends number of positive cells in channel to inner list for each spot channel
                poscells_tot.append([len(dfs), datasetlabels[a]])                               #Creates list of the total number of cells positive in ANY CHANNEL for this dataset
                poscells_innerlist.append(datasetlabels[a])      
                poscells.append(poscells_innerlist)                                             #appends cuurent dataset information to multi-dataset list, each innerlist contains the cell number information for a particular dataset
                
                
                
                
                
                #GENERATING RELEVANT DATA FOR FIRST DOUBLE POSITIVE CHANNEL PAIR (See RNA Expression for annotation)
                
                if Plot_dubposA == 1:
                
                    #Creating a dataframe containing only double positive cells for first two channels of interest
                    
                    dfdpAst = dfs
                    for i in dubposA_channels:
                        dfdpAst = dfdpAst[dfdpAst[f"{i} Spots"] >= dubposA_threshold]                                   #creates a new dataframe with only double positive cells based on the condition that the list of chosen channels are non-zero for each cell
                    dfdpAs = dfdpAst                                                                    #After partitioning is complete for all chosen channels, the temporary dataframe is stored as the final dataframe used for plotting below
                    
                    #Calculating spots per cell per channel for double positive cells only
                    
                    dubposA_innerlist = []
                    for i in col_labels_spots:                                          
                        dubposA_innerlist.append(dfdpAs[i].sum())                                       #each list represents a dataset (input file)
                    dubposA_innerlist.append(datasetlabels[a])                                          #within each of those lists the values are the total count of each spot channel
                    dubposAspot_tot.append(dubposA_innerlist)                                           #Appends current dataset data to multi-daatset list, each innerlist is a dataset
                    
                    #Calculating number of positive cells for double positive cells
                    
                    dubposA_innerlist = []                                              
                    for i in col_labels_spots:                                                                #each innerlist contains the number of double positive cells in each channel in that dataset       
                        dubposA_innerlist.append(len(dfdpAs[dfdpAs[i] != 0]))                           #appends number of dub positive cells in channel to inner list for each spot channel
                    dubposAnum_tot.append([len(dfdpAs), datasetlabels[a]])                              #Creates list of the total number of cells positive irrespective of channel for this dataset
                    dubposA_innerlist.append(datasetlabels[a])                                          #Adds dataset label
                    dubposAnum.append(dubposA_innerlist)                                                #Appends current dataset information to multi-dataset list
                    
                    

                    #SUBCELLULAR INTENSITY DATA AND SUM CALCULATIONS FOR FIRST DOUBLE POSITIVE DATASET
                    #Storing subcellular intensity data for double-positive cells only
                
                    dfdpAit = dfi
                    for i in dubposA_channels:                                                          #Same process as above for multi-positive cell spot/cluster data but for handling subcellular intensity data
                        dfdpAit = dfdpAit[dfdpAit[i] != 0]                                              #Paritions non-zero data for each channel in user defined multi-positive channel list
                    dfdpAi = dfdpAit
                    
                    if channel_consistency == 1:
                        #Calculating total intensities per channel for all double positive cells for first double positive channel pair
                        
                        dubposAintensitytot_innerlist = []
                        for i in col_labels:                                                        
                            dubposAintensitytot_innerlist.append(dfdpAi[i].sum())                   
                        dubposAintensitytot_innerlist.append(datasetlabels[a])                      
                        dubposAintensity_tot.append(dubposAintensitytot_innerlist)
                    
                    
                
                
                
                #GENERATING RELEVANT DATA FOR SECOND DOUBLE POSITIVE CHANNEL PAIR (See RNA Expression  and first double positive sections above for annotation)
                
                if Plot_dubposB == 1:
                
                    #Creating a dataframe containing only double positive cells for second two channels of interest
                    
                    dfdpBst = dfs
                    for i in dubposB_channels:
                        dfdpBst = dfdpBst[dfdpBst[f"{i} Spots"] >= dubposB_threshold]                                   #creates a new dataframe with only double positive cells based on the condition that the list of chosen channels are non-zero for each cell
                    dfdpBs = dfdpBst                                                                    #After partitioning is complete for all chosen channels, the temporary dataframe is stored as the final dataframe used for plotting below
              
                    #Calculating spots per cell per channel for double positive cells only
                    
                    dubposB_innerlist = []
                    for i in col_labels_spots:                                            
                        dubposB_innerlist.append(dfdpBs[i].sum())                                       #each innerlist represents a dataset (input file)
                    dubposB_innerlist.append(datasetlabels[a])                                          #within each of those lists the values are the total count of each spot channel
                    dubposBspot_tot.append(dubposB_innerlist)                                           #Appends current dataset informatioin to multi-dataset list, each list is a dataset
                        
                    #Calculating number of positive cells for double positive cells
                    
                    dubposB_innerlist = []                                          
                    for i in col_labels_spots:                                                                #each innerlist contains the number of double positive cells in each channel in that dataset       
                        dubposB_innerlist.append(len(dfdpBs[dfdpBs[i] != 0]))                           #appends number of dub positive cells in channel to inner list for each spot channel
                    dubposBnum_tot.append([len(dfdpBs), datasetlabels[a]])                              #Creates list of the total number of cells positive irrespective of channel for this dataset
                    dubposB_innerlist.append(datasetlabels[a])                                          #Adds dataset label
                    dubposBnum.append(dubposB_innerlist)                                                #Appends current dataset data to multi-set list
                    
                    

                    #SUBCELLULAR INTENSITY DATA AND SUM CALCULATIONS FOR SECOND DOUBLE POSITIVE DATASET
                    #Storing subcellular intensity data for double-positive cells only
                    
                    dfdpBit = dfi
                    for i in dubposB_channels:                                                          #Same process as above for multi-positive cell spot/cluster data but for handling subcellular intensity data
                        dfdpBit = dfdpBit[dfdpBit[i] != 0]                                              #Paritions non-zero data for each channel in user defined multi-positive channel list
                    dfdpBi = dfdpBit
                    
                    if channel_consistency == 1:
                        #Calculating total intensities per channel for all double positive cells for second double positive channel pair
                        
                        
                        dubposBintensitytot_innerlist = []
                        for i in col_labels:                                                            
                            dubposBintensitytot_innerlist.append(dfdpBi[i].sum())                       
                        dubposBintensitytot_innerlist.append(datasetlabels[a])                          
                        dubposBintensity_tot.append(dubposBintensitytot_innerlist)                
                    
                    
                
                
                
                #CREATING MULTI-DATASET DATAFRAMES AND APPENDING DATA GENERATED FOR CURRENT DATASET
                
                if line_count == 0:                                                                 #For first dataset in input folder, simply copies specified dataframes to a dataframe which will be used to store said data for all datasets
                    dfspot = dfs
                    dfintensity = dfi
                    if Plot_dubposA == 1:
                        dfdubposAspot = dfdpAs
                        dfdubposAintensity = dfdpAi
                    if Plot_dubposB == 1:
                        dfdubposBspot = dfdpBs
                        dfdubposBintensity = dfdpBi
                    line_count += 1
                    
                else:                                                                               #For subsequent datasets, concatanates the data for that dataset to the large multi-dataset dataframe generated above
                    dfspot = pd.concat([dfspot, dfs], axis = 0)
                    dfintensity = pd.concat([dfintensity, dfi], axis = 0)
                    if Plot_dubposA == 1:
                        dfdubposAspot = pd.concat([dfdubposAspot, dfdpAs], axis = 0)
                        dfdubposAintensity = pd.concat([dfdubposAintensity, dfdpAi], axis = 0)
                    if Plot_dubposB == 1:
                        dfdubposBspot = pd.concat([dfdubposBspot, dfdpBs], axis = 0)
                        dfdubposBintensity = pd.concat([dfdubposBintensity, dfdpBi], axis = 0)
                
                if channel_consistency == 1:
                    dfnzintensity = pd.DataFrame()                                                      #creates an empty dataframe for non-zero intensity data
                    for i in col_labels:                                                                #Special case; Runs through channels in intensity dataframe created above to find only non-zero intensities and stores these to a seperate dataframe
                            dfnzi = dfintensity[dfintensity[i] != 0]
                            dfnzintensity = pd.concat([dfnzintensity, dfnzi], axis = 0)
                            dfnzintensity = dfnzintensity.drop_duplicates()
    




                #CURRENT DATASET PLOTTING
        
                sns.set_palette("tab10")        
        
                #Scatter plot of cell distribution (based on centroid) throughout dataset, sized by spot count, coloured by channel
                
                if Plot_Spot_Map == 1:
                    dfout_scatter = dfout                                                                       #Create dataframe of data to be thresholded and subsequently poltted
                    for i in range(len(col_labels)):                                                            #Loop to rename columns based on user inputted channel names
                        dfout_scatter.rename(columns = {col_labels_spots[i]:col_labels[i]}, inplace = True)
                    fig = plt.figure()                                                                                                                    
                    ax = fig.add_subplot(111)
                    size = []
                    plt.xlim(min(x_centroids) - 10, max(x_centroids)+10)
                    plt.ylim(min(y_centroids) - 10, max(y_centroids)+10)                                                                                                                                        #List which will be used to store spot information to be plotted following thresholding 
                    for i in range(len(spot_headers)):                                                                                                              #For each channel, plots the centroids of all cells and sizes them according to the number of spots in that cell (weights created during thresholdingstep below). Colours are then assigned automatically for each channels data.
                        for d in range(len(dfout_scatter[col_labels])):                                                                                             #For loop cycling through each individual cell for the current target channel, this allows us to determine whether each cell passes the threshold for the current channel, thus only cells expressing above threshold in this channel will be plotted    
                            if dfout_scatter[col_labels].iloc[d,i] >= threshold:                                                                                    #Checks current cell is above threshold for current channel
                                size.append(10*(dfout_scatter[col_labels].iloc[d,i]))                                                                               #If so, cell will plotted with size according to number of transcripts expressed in this channel
                            elif dfout_scatter[col_labels].iloc[d,i] == dfout_scatter[col_labels].iloc[d,:].sum():                                                  #If cell does not meet the threshold for the current channel BUT is only expressing in this channel (that is, the current channel transcript number is equal to the total number of transcripts expressed by the cell) then this cell is plotted despite being below the threshold
                                size.append(10*(dfout_scatter[col_labels].iloc[d,i]))                                                                               #this is done because the thresholding feature is designed to allow users to reduce the impact of mis-categorised transcripts arising from boundary approximations on the profiles of cells, this means that single expressing cells which do not have ambiguous expression profiles are left unaffected even if they have low expression (below threshold)
                            else:                                                                                                                                   #If cell does not surpass threshold size is set to zero such that cell will not be plotted
                                size.append(0)
                        plt.scatter(x = dfout["X Centroids"], y = dfout["Y Centroids"], s = size, alpha = 0.5, label = col_labels[i])                               #Creates the scatter plot of centroid data for the current channel, 's' is the size this allows us to make the size a function of the number of spots in this cell (the number of spots within this cell is being read from the spots dataframe we created above), 'label' simply names your data based on the channel being plotted
                        plt.xlabel("X Centroids", fontsize = 10)
                        plt.ylabel("Y Centroids", fontsize = 10)
                        size = []                                                                                                                                   #Empties size list following plotting of the information for the current channel such that this list can be used for information relating to the next channel to be plotted
                    plt.title(f"{datasetlabels[a]} Transcript Distribution")
                    ax.invert_yaxis()
                    ax.set_aspect('equal')                                                                                                               
                    lgnd = plt.legend(scatterpoints=1, fontsize=10, loc='center left', bbox_to_anchor=(1, 0.5))                                                   #Shows the legend for the plotted datasets on the figure
                    lgnd.legendHandles[0]._sizes = [30]                                                                                                           #Makes legend datapoints uniform                                                                                             
                    lgnd.legendHandles[1]._sizes = [30]
                    plt.savefig(f"{output_folder}{datasetlabels[a]} Transcript Distribution by Channel", bbox_inches = "tight", dpi=500)

                sns.set_palette(sns.color_palette(colours))
                
                #Plotting histogram of spot count occurances in current dataset
                
                if Plot_Spot_Histogram == 1:
                    dfout_hist = dfout                                                                       #Create dataframe of data to be thresholded and subsequently poltted
                    for i in range(len(col_labels)):                                                            #Loop to rename columns based on user inputted channel names
                        dfout_hist.rename(columns = {col_labels_spots[i]:col_labels[i]}, inplace = True)
                    plt.figure()                                                                                                                                        #Creates a figure to which data can be plotted
                    dfout_hist = dfout[dfout[col_labels] > 0]
                    sns.histplot(dfout_hist[col_labels], binwidth = 1, multiple = "dodge", kde = True)                                                                  #creates a histogram of spot data for current dataset stored in the dataframe created above
                    plt.xlabel("Transcript Count")                                                                                                                            #labels the axes and titles figure
                    plt.ylabel("Occurance")
                    plt.title(f"{datasetlabels[a]} Transcript Count Occurances")
                    plt.savefig(f"{output_folder}{datasetlabels[a]} Transcript Count Occurance Histogram", bbox_inches = "tight", dpi=500)

    #Changing column names for the purposes of plotting  
    
    for i in range(len(col_labels)):
        dfspot.rename(columns = {col_labels_spots[i]:col_labels[i]}, inplace = True)

    #Reshaping dataframes to ease plotting with repect to channel
    
    dfspotlong = pd.melt(dfspot, id_vars = "Dataset", value_vars = col_labels, var_name = "Channel", value_name = "Spots")
    
    if channel_consistency == 1:
        dfintensitylong = pd.melt(dfintensity, id_vars = "Dataset", value_vars = col_labels, var_name = "Channel", value_name = "Cell Intensity")
        dfnzintensitylong = pd.melt(dfnzintensity, id_vars = "Dataset", value_vars = col_labels, var_name = "Channel", value_name = "Cell Intensity")
        
    
    #MULTI-DATASET ANALYSIS AND PLOTTING
     
    plotting_headers = col_labels.copy()
    plotting_headers.append("Dataset")
    
    
    if Plot_RNA_expression == 1:
        try:
            os.mkdir(f'{output_folder}\\General Transcript Abundance Analytics')                  #Make a subdirectory in the pipeline output for each set of expression analytics 
        except:
            pass 
        
        #Plot spot count data per cell per channel
        
        plt.figure()
        sns.boxplot(data = dfspotlong, x = "Channel", y = "Spots", hue = "Dataset", showfliers = False, **PROPS)
        sns.stripplot(data = dfspotlong, x = "Channel", y = "Spots", hue = "Dataset", dodge = True, size = 3.5, palette = colours, edgecolor = "Black", linewidth = 1, jitter = 0.06)
        plt.xticks(plt.xticks()[0])
        plt.xlabel("Channel")
        plt.ylabel("Transcripts per Cell")
        plt.title("Cell-wise Transcript Count by Channel")
        plt.legend(custom_lines, datasetlabels)
        plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Cell-wise Transcript Count by Channel", bbox_inches = "tight", dpi=500)
        dfspot.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Cell-wise Trascript Count by Channel.csv", sep=',')
        
        if channel_consistency == 1:
            #Plot total cellular intensity per cell per channel
            
            plt.figure()
            sns.boxplot(data = dfintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", showfliers = False, **PROPS)
            sns.stripplot(data = dfintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", dodge = True, size = 3.5, palette = colours, edgecolor = "Black", linewidth = 1, jitter = 0.06)
            plt.xticks(plt.xticks()[0])
            plt.xlabel("Channel")
            plt.ylabel("Intensity per Cell")
            plt.title("Cell-wise Intensity by Channel")
            plt.legend(custom_lines, datasetlabels)
            plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Cell-wise Intensity by Channel", bbox_inches = "tight", dpi=500)
            dfintensity.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Cell-wise Intensity by Channel.csv", sep=',')
            
            #Plot non-zero cellular intensity per cell per channel
            
            plt.figure()
            sns.boxplot(data = dfnzintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", showfliers = False, **PROPS)
            sns.stripplot(data = dfnzintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", dodge = True, size = 3.5, palette = colours, edgecolor = "Black", linewidth = 1, jitter = 0.06)
            plt.xticks(plt.xticks()[0])
            plt.xlabel("Channel")
            plt.ylabel("Intensity per Cell")
            plt.title("Cell-wise Intensity for Non-Zero Cells by Channel")
            plt.legend(custom_lines, datasetlabels)
            plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Intensity of Non-Zero Cells by Channel", bbox_inches = "tight", dpi=500)
            dfnzintensity.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Intensity of Non-Zero Cells by Channel.csv", sep=',')
            
        #Creating dataframe containing total spot count information per channel for plotting
        
        dfspottotal = pd.DataFrame(spotcount_tot, columns = plotting_headers)
        dfspottotallong = pd.melt(dfspottotal, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Spot Count")
    
        #Bar plot for overall sample spot count (sum of spots in all cells) per channel
    
        plt.figure()
        sns.barplot(data = dfspottotallong, x = "Channel", y = "Spot Count", hue = "Dataset", edgecolor = "Black")
        plt.title("Total Transcript Count by Channel")
        plt.xticks(plt.xticks()[0])
        plt.legend()
        plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Total Transcript Count by Channel", bbox_inches = "tight", dpi=500)
        dfspottotal.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Total Transcript Count by Channel.csv", sep=',')

        #Equivilant dataframe and plot for total intensity per channel
    
        dfintensitytotal = pd.DataFrame(intensity_tot, columns = plotting_headers)
        dfintensitytotallong = pd.melt(dfintensitytotal, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Intensity")
        
        if channel_consistency == 1:
            plt.figure()
            sns.barplot(data = dfintensitytotallong, x = "Channel", y = "Intensity", hue = "Dataset", edgecolor = "Black")
            plt.title("Total Intensity by Channel")
            plt.xticks(plt.xticks()[0])
            plt.legend()
            plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Total Intensity by Channel", bbox_inches = "tight", dpi=500)
            dfintensitytotal.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Total Intensity by Channel.csv", sep=',')
        
        #Creating dataframe containing spot-positive cell number information for plotting
    
        dfposcells = pd.DataFrame(poscells, columns = plotting_headers)
        dfposcellslong = pd.melt(dfposcells, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "CellNum")
    
        #Bar plot for total positive cell number per channel
    
        plt.figure()
        sns.barplot(data = dfposcellslong, x = "Channel", y = "CellNum", hue = "Dataset", edgecolor = "Black")
        plt.title("Number of Transcript Expressing Cells per Channel")
        plt.ylabel("Number of Transcript Expressing Cells")
        plt.xticks(plt.xticks()[0])
        plt.legend()
        plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Transcript Expressing Cell Count by Channel", bbox_inches = "tight", dpi=500)
        dfposcells.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Transcript Expressing Cell Count by Channel.csv", sep=',')
        
        #Plotting total positive cell number irrespective of channel
    
        dfposcells_tot = pd.DataFrame(poscells_tot, columns =  ["Value", "Dataset"])
    
        plt.figure()
        sns.barplot(data = dfposcells_tot, x = "Dataset", y = "Value", edgecolor = "Black")
        plt.ylabel("Number of Transcript Expressing Cells")
        plt.title("Total Transcript Expressing Cells (All Channels)")
        plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Transcript Expressing Cell Count", bbox_inches = "tight", dpi=500)
        dfposcells_tot.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Transcript Expressing Cell Count.csv", sep=',')

        #Plotting total cell number as quantified in QuPath
        
        dfallcells = pd.DataFrame(allcells, columns = ["Value", "Dataset"])
        
        plt.figure()
        sns.barplot(data = dfallcells, x = "Dataset", y = "Value", edgecolor = "Black")
        plt.ylabel("Number of Cells")
        plt.title("Total Quantified Cells (All Channels)")
        plt.savefig(f"{output_folder}\\General Transcript Abundance Analytics\\Quantified Cell Count", bbox_inches = "tight", dpi=500)
        dfallcells.to_csv(f"{output_folder}\\General Transcript Abundance Analytics\\Quantified Cell Count.csv", sep=',')


    if Plot_dubposA == 1:
        try:
            os.mkdir(f'{output_folder}\\[{dubposAchans}] Positive Cells')                   
        except:
            pass
        
        #Changing column names for the purposes of plotting
        try:
            for i in range(len(col_labels)):
                dfdubposAspot.rename(columns = {col_labels_spots[i]:col_labels[i]}, inplace = True)
    
            #Creating dataframes containing plotting information for first double posititve pair
        
            dfdubposAspotlong = pd.melt(dfdubposAspot, id_vars = "Dataset", value_vars = col_labels, var_name = "Channel", value_name = "Spots")
            
            
            dfdubposAnum = pd.DataFrame(dubposAnum, columns = plotting_headers)
            dfdubposAnumlong = pd.melt(dfdubposAnum, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Number of Cells")
            
            dfdubposAspottotal = pd.DataFrame(dubposAspot_tot, columns = plotting_headers)
            dfdubposAspottotallong = pd.melt(dfdubposAspottotal, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Spot Count")
            
                    
            if channel_consistency == 1:
                dfdubposAintensitylong = pd.melt(dfdubposAintensity, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Cell Intensity")
                dfdubposAintensitytotal = pd.DataFrame(dubposAintensity_tot, columns = plotting_headers)
                dfdubposAintensitytotallong = pd.melt(dfdubposAintensitytotal, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Intensity")
    
                
        
            #Box plot of cell-wise spot count for first set of double positive cells per channel (basically a stripped down version of the box plt above but showing only the spots for double positive cells)
        
            plt.figure()
            sns.boxplot(data = dfdubposAspotlong, x = "Channel", y = "Spots", hue = "Dataset", showfliers = False, **PROPS)
            sns.stripplot(data = dfdubposAspotlong, x = "Channel", y = "Spots", hue = "Dataset", dodge = True, size = 3.5, palette = colours, edgecolor = "Black", linewidth = 1, jitter = 0.06)
            plt.xticks(plt.xticks()[0])
            plt.xlabel("Channel")
            plt.ylabel("Transcripts per Cell")
            plt.title(f"Cell-Wise Transcript Count for [{dubposAchans}] Positive Cells")
            plt.legend(custom_lines, datasetlabels)
            plt.savefig(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Cell-wise Transcript Count [{dubposAchans}]", bbox_inches = "tight", dpi=500)
            dfdubposAspot.to_csv(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Cell-wise Transcript Count [{dubposAchans}].csv", sep=',')
            
            if channel_consistency == 1:
                #Box plot of cell-wise intensity for first double positive channel pair
        
                plt.figure()
                sns.boxplot(data = dfdubposAintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", showfliers = False, **PROPS)
                sns.stripplot(data = dfdubposAintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", dodge = True, size = 3.5, palette = colours, edgecolor = "Black", linewidth = 1, jitter = 0.06)
                plt.xticks(plt.xticks()[0])
                plt.xlabel("Channel")
                plt.ylabel("Intensity per Cell")
                plt.title(f"Cell-wise Intensity for [{dubposAchans}] Positive Cells")
                plt.legend(custom_lines, datasetlabels)
                plt.savefig(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Cell-wise Intensity [{dubposAchans}]", bbox_inches = "tight", dpi=500)
                dfdubposAintensity.to_csv(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Cell-wise Intensity [{dubposAchans}].csv", sep=',')
    
                #Bar plot for total intensity per channel
                
                plt.figure()
                sns.barplot(data = dfdubposAintensitytotallong, x = "Channel", y = "Intensity", hue = "Dataset", edgecolor = "Black")
                plt.title(f"Total Intensity for [{dubposAchans}] Positive Cells")
                plt.xticks(plt.xticks()[0])
                plt.legend()
                plt.savefig(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Total Intensity [{dubposAchans}]", bbox_inches = "tight", dpi=500)
                dfdubposAintensitytotal.to_csv(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Total Intensity [{dubposAchans}].csv", sep=',')
                
            #Bar plot of double positive spot count (total spots in all cells) per channel per dataset
        
            plt.figure()
            sns.barplot(data = dfdubposAspottotallong, x = "Channel", y = "Spot Count", hue = "Dataset", edgecolor = "Black")
            plt.title(f"Total Transcript Count for [{dubposAchans}] Positive Cells")
            plt.xticks(plt.xticks()[0])
            plt.legend(custom_lines, datasetlabels)
            plt.savefig(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Total Transcript Count [{dubposAchans}]", bbox_inches = "tight", dpi=500)
            dfdubposAspottotal.to_csv(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Total Transcript Count [{dubposAchans}].csv", sep=',')
        
            #Bar plot of double positive cell number per channel per dataset
        
            plt.figure()
            sns.barplot(data = dfdubposAnumlong, x = "Channel", y = "Number of Cells", hue = "Dataset", edgecolor = "Black")
            plt.title(f"Total Number of [{dubposAchans}] Positive Cells by Target Channel")
            plt.xticks(plt.xticks()[0])
            plt.legend()
            plt.savefig(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Positive Cell Number [{dubposAchans}]", bbox_inches = "tight", dpi=500)
            dfdubposAnum.to_csv(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Positive Cell Number [{dubposAchans}].csv", sep=',')
           
            #Bar plot of double positive cell count totals 
        
            dfdubposAnum_tot = pd.DataFrame(dubposAnum_tot, columns =  ["Value", "Dataset"])
        
            plt.figure()
            sns.barplot(data = dfdubposAnum_tot, x = "Dataset", y = "Value", edgecolor = "Black")
            plt.ylabel("Number of Cells", fontsize = 14)
            plt.title(f"Total Number of [{dubposAchans}] Positive Cells (All Channels)", y = 1.05)
            plt.savefig(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Total Positive Cells [{dubposAchans}]", bbox_inches = "tight", dpi=500)
            dfdubposAnum_tot.to_csv(f"{output_folder}\\[{dubposAchans}] Positive Cells\\Total Positive Cells [{dubposAchans}].csv", sep=',')
        except:
            with open(f'{output_folder}\\[{dubposAchans}] Positive Cells\\Exception.txt', 'w', newline = '') as exceptA:                          #creates a csv file for the current dataset
                exceptA.write(f"No cells displying [{dubposAchans}] profile")

    if Plot_dubposB == 1:
        try:
            os.mkdir(f'{output_folder}\\[{dubposBchans}] Positive Cells')                   
        except:
            pass
        
        #Changing column names for the purposes of plotting  
        try:
            for i in range(len(col_labels)):
                dfdubposBspot.rename(columns = {col_labels_spots[i]:col_labels[i]}, inplace = True)
            
            #Creating dataframes containing plotting information for second double posititve pair
        
            dfdubposBspotlong = pd.melt(dfdubposBspot, id_vars = "Dataset", value_vars = col_labels, var_name = "Channel", value_name = "Spots")
            
            dfdubposBnum = pd.DataFrame(dubposBnum, columns = plotting_headers)
            dfdubposBnumlong = pd.melt(dfdubposBnum, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Number of Cells")
            
            dfdubposBspottotal = pd.DataFrame(dubposBspot_tot, columns = plotting_headers)
            dfdubposBspottotallong = pd.melt(dfdubposBspottotal, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Spot Count")
            
            if channel_consistency == 1:
                dfdubposBintensitylong = pd.melt(dfdubposBintensity, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Cell Intensity")
                dfdubposBintensitytotal = pd.DataFrame(dubposBintensity_tot, columns = plotting_headers)
                dfdubposBintensitytotallong = pd.melt(dfdubposBintensitytotal, id_vars = "Dataset", value_vars = plotting_headers, var_name = "Channel", value_name = "Intensity")
        
        
            #Box plot of cell-wise double positive cells per channel
        
            plt.figure()
            sns.boxplot(data = dfdubposBspotlong, x = "Channel", y = "Spots", hue = "Dataset", showfliers = False, **PROPS)
            sns.stripplot(data = dfdubposBspotlong, x = "Channel", y = "Spots", hue = "Dataset", dodge = True, size = 3.5, palette = colours, edgecolor = "Black", linewidth = 1, jitter = 0.06)
            plt.xticks(plt.xticks()[0])
            plt.xlabel("Channel")
            plt.ylabel("Transcripts per Cell")
            plt.title(f"Cell-Wise Transcript Count for [{dubposBchans}] Positive Cells")
            plt.legend(custom_lines, datasetlabels)
            plt.savefig(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Cell-wise Transcript Count [{dubposBchans}]", bbox_inches = "tight", dpi=500)
            dfdubposBspot.to_csv(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Cell-wise Transcript Count [{dubposBchans}].csv", sep=',')
        
            if channel_consistency == 1:
                #Box plot of cell-wise intensity for second double positive channel pair
        
                plt.figure()
                sns.boxplot(data = dfdubposBintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", showfliers = False, **PROPS)
                sns.stripplot(data = dfdubposBintensitylong, x = "Channel", y = "Cell Intensity", hue = "Dataset", dodge = True, size = 3.5, palette = colours, edgecolor = "Black", linewidth = 1, jitter = 0.06)
                plt.xticks(plt.xticks()[0])
                plt.xlabel("Channel")
                plt.ylabel("Intensity per Cell")
                plt.title(f"Cell-wise Intensity for [{dubposBchans}] Positive Cells")
                plt.legend(custom_lines, datasetlabels)
                plt.savefig(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Cell-wise Intensity [{dubposBchans}]", bbox_inches = "tight", dpi=500)
                dfdubposBintensity.to_csv(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Cell-wise Intensity [{dubposBchans}].csv", sep=',')
            
                #Equivilant plot for total intensity per channel
            
                plt.figure()
                sns.barplot(data = dfdubposBintensitytotallong, x = "Channel", y = "Intensity", hue = "Dataset", edgecolor = "Black")
                plt.title(f"Total Intensity for [{dubposBchans}] Positive Cells")
                plt.xticks(plt.xticks()[0])
                plt.legend()
                plt.savefig(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Total Intensity [{dubposBchans}]", bbox_inches = "tight", dpi=500)
                dfdubposBintensitytotal.to_csv(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Total Intensity [{dubposBchans}].csv", sep=',')
            
            #Bar plot of double positive Spot Count (total spots in all cells) per channel per dataset
        
            plt.figure()
            sns.barplot(data = dfdubposBspottotallong, x = "Channel", y = "Spot Count", hue = "Dataset", edgecolor = "Black")
            plt.title(f"Total Transcript Count for [{dubposBchans}] Positive Cells")
            plt.xticks(plt.xticks()[0])
            plt.legend()
            plt.savefig(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Total Transcript Count [{dubposBchans}]", bbox_inches = "tight", dpi=500)
            dfdubposBspottotal.to_csv(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Total Transcript Count [{dubposBchans}].csv", sep=',')
        
            #Bar plot of double positive cell number per channel per dataset
        
            plt.figure()
            sns.barplot(data = dfdubposBnumlong, x = "Channel", y = "Number of Cells", hue = "Dataset", edgecolor = "Black")
            plt.title(f"Total Number of [{dubposBchans}] Positive Cells by Target Channel")
            plt.xticks(plt.xticks()[0])
            plt.legend()
            plt.savefig(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Positive Cell Number [{dubposBchans}]", bbox_inches = "tight", dpi=500)
            dfdubposBnum.to_csv(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Positive Cell Number [{dubposBchans}].csv", sep=',')
           
            #Bar plot of double positive cell count totals
        
            dfdubposBnum_tot = pd.DataFrame(dubposBnum_tot, columns =  ["Value", "Dataset"])
        
            plt.figure()
            sns.barplot(data = dfdubposBnum_tot, x = "Dataset", y = "Value", edgecolor = "Black")
            plt.ylabel("Number of Cells")
            plt.title(f"Total Number of [{dubposBchans}] Positive Cells (All Channels)")
            plt.savefig(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Total Positive Cells [{dubposBchans}]", bbox_inches = "tight", dpi=500) 
            dfdubposBnum_tot.to_csv(f"{output_folder}\\[{dubposBchans}] Positive Cells\\Total Positive Cells [{dubposBchans}].csv", sep=',')
        except:
            with open(f'{output_folder}\\[{dubposBchans}] Positive Cells\\Exception.txt', 'w', newline = '') as exceptB:                          #creates a csv file for the current dataset
                exceptB.write(f"No cells displying [{dubposBchans}] profile")            
        
    #Close all datafiles opened by the program
    r.close()
    w.close()    
    file.close()
    f.close()
    print("done")