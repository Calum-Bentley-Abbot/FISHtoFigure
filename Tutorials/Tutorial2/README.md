Included are example data from a RNAScope experiment investigating T.brucei infection in the ventricles and choroid plexus of mouse brains. This tutorial includes two concatenated datasets created using the FISHtoFigure preprocessor (Dataset1 comprises images taken of a naive sample [9 images], Dataset2 comprises images of an infected sample [17 images]). The mRNA targets for these data are as follows: Cd79a, Cx3cr1, Il10, Il10ra.

Step 1: 
Download both datasets and store them in an empty directory (folder).

Step 2: 
Within FISHtoFigure, specify the path to the directory containing the tutorial datasets in the input folder path field and click "Find" to commit this selection. For demonstrative purposes, we will conduct all analysis available in FISHtoFigure, to this end, tick all options in the select analysis options section. 
To conduct multi-target analysis, we must specify the trascriptional profile we wish to analyse, this will be a subset of the detection channel names provided in the next section of the user interface and each individual target name should be seperated by a comma and single space. As mentioned our RNA targets in this dataset are: Cd79a, Cx3cr1, Il10, Il10ra. Therefore, in the first set of multi-positive channels enter "Cd79a, Il10" (without "") and in the second enter "Cx3cr1, Il10ra".
For now, we will leave the positive cell threshold blank, this can be used to adjust the number of transcriptional spots a cell must express to be included in analysis. You can have a play with this and compare your results to the provided tutorial results to see how this works in practice.
Once all the analysis options have been selected and required information provided, click the commit selection button.

![Tut2_fig1](https://user-images.githubusercontent.com/109809682/183069937-ca5203eb-53f4-4483-baf1-999d63b12648.png)

Step 3:
Finally, we must specify both the names of our RNA targets (in the order they appear in the quantified QuPath file, this will be the same as the order they were quatified in within QuPath) and the names of the datasets we are analysing (This should be ordered as they appear in the input directory). In our case, the channel name list should be entered as "Cd79a, Cx3cr1, Il10, Il10ra" and since Dataset1 and Dataset2 are our naive data and infected data respectively, enter "Naive, Infected" in the dataset names field.
Click commit selection to assign these channel and dataset labels.

![Tut2_fig2](https://user-images.githubusercontent.com/109809682/183069971-1db6cb9d-9a11-47bc-a116-a5a25d0e8b25.png)

Finally, click run to conduct the analysis, for a dataset of this size this will likely take approximately 1-3 minutes depeding on computer hardware.
Running FISHtoFigure will create 2 new directories within the input directory, "csv files" simply contains a csv equivilant of each input file, "F2F output" contains all analysis outputs and supporting datasets as csv files. The output for this tutorial is shown within the tutorial output directory for reference.
