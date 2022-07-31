# FISHtoFigure
A Python-based platform for the in-depth analysis of smFISH data

FISHtoFigure enables in-depth probing of the transcriptome in smFISH image data quantified using QuPath. QuPath quantified data can either be directly used as input data for FISHtoFigure or quantified datasets from multiple images can be concatenated using the preprocessing tool before analysis with FISHtoFigure.  

FISHtoFigure analysis capacities: 

Plot transcript occurences: Histogram showing number of cells expressing a given number of spots for each RNA target channel. (This recreates the pre-existing in-house histographic analysis of quantified smFISH data within QuPath)

Plot transcript distribution: Scatter plot showing quantified transcriptional spot data in a format analogous to the input image. This function creates a plot in which each point in x/y represents a cell in the input image (as defined by the x/y cell centroid data in the quantified image datafile). Points are plotted and coloured by RNA target channel, points are sized by number of RNA transcripts expressed within the given cell. This function provides a means to validate the data quantification carried out in QuPath and the data harvesting conducted by FISHtoFigure by directly comparing this plot with the input image, in addition to providing a quantified equivalent of the input smFISH image. The threshold function allows users to define a minimum number of transcripts which must be expressed by a cell for it to be included in the distribution plot. This allows for the removal of low-level background transcript expression. 

![Github fig1_2](https://user-images.githubusercontent.com/109809682/182032194-273be54e-38b7-4056-ad68-d8733c2d8dab.png)

Transcript abundance analysis: Differential transcript expression analysis can be conducted between an arbitrary number of quantified datasets. Names of target channels and datasets being compared will be shown on analysis outputs as they appear in the Channel names and Dataset names lists provided by the user within the GUI. RNA target channel names must be defined in the order they appear in quantified QuPath data, and dataset names should named in the order they appear in the input directory. Multi-target abundance analysis: Conducts differential transcript expression analysis on cells expressing a user defined set of targets, enabling analysis of specific cell profiles or cell types in quantified smFISH data.

![Github fig3](https://user-images.githubusercontent.com/109809682/182028486-fb2d5315-85c2-4c1d-9401-9c28309d872d.png)
