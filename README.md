# FISHtoFigure
A Python-based platform for the in-depth analysis of smFISH data.

Use the Quick-start Tutorial to get started using the FISHtoFigure pipeline, this contains all the information required to conduct analysis. The FISHtoFigure User Information contains more detailed descriptions of how analysis is performed and is more useful for troubleshooting or further code development. 

See the pre-print here for full details: https://www.biorxiv.org/content/10.1101/2023.06.28.546871v1

FISHtoFigure enables in-depth probing of the transcriptome in smFISH image data quantified using QuPath. QuPath quantified data can either be directly used as input data for FISHtoFigure or quantified datasets from multiple images can be concatenated using the preprocessing tool before analysis with FISHtoFigure. To facilitate this analysis by all users, regardless of bioinformatic experience levels, FISHtoFigure runs from a dedicated graphical user interface, allowing transcriptome and cell type analysis without custom code or interaction with raw data:

![guiannotation](https://github.com/Calum-Bentley-Abbot/FISHtoFigure/assets/109809682/0b23f957-44b2-40ef-bc16-795d8a657750)

FISHtoFigure analysis capacities: 

Plot transcript occurences: Histogram showing number of cells expressing a given number of spots for each RNA target channel. (This recreates the pre-existing in-house histographic analysis of quantified smFISH data within QuPath).

Plot transcript distribution: Scatter plot showing quantified transcriptional spot data in a format analogous to the input image. This function creates a plot in which each point in x/y represents a cell in the input image (as defined by the x/y cell centroid data in the quantified image datafile). Points are plotted and coloured by RNA target channel, points are sized by number of RNA transcripts expressed within the given cell. This function provides a means to validate the data quantification carried out in QuPath and the data harvesting conducted by FISHtoFigure by directly comparing this plot with the input image as shown below, in addition to providing a quantified equivalent of the input smFISH image. The threshold function allows users to define a minimum number of transcripts which must be expressed by a cell for it to be included in the distribution plot. This allows for the removal of low-level background transcript expression. 

![github Figure2](https://github.com/Calum-Bentley-Abbot/FISHtoFigure/assets/109809682/df52d515-04b7-4afe-8489-7dcf12261ef8)

Transcript abundance analysis: Differential transcript expression analysis can be conducted between an arbitrary number of quantified datasets. Names of target channels and datasets being compared will be shown on analysis outputs as they appear in the Channel names and Dataset names lists provided by the user within the GUI. RNA target channel names must be defined in the order they appear in quantified QuPath data, and dataset names should named in the order they appear in the input directory. Multi-target abundance analysis: Conducts differential transcript expression analysis on cells expressing a user defined set of targets, enabling analysis of specific cell profiles or cell types in quantified smFISH data. 

Below are examples of transcript abundance analysis for 4 mRNA targets (which can be performed either on a cell-by-cell basis (**Figure A**) or by the cummulative intensity for all cells (**Figure B**). **Figure C** shows a multi-target analysis for two distinct cell types each defined by the expression of two mRNA targets, statistical tests were performed in GraphPad PRISM. For more information see the pre-print here: https://www.biorxiv.org/content/10.1101/2023.06.28.546871v1.

![figure3](https://github.com/Calum-Bentley-Abbot/FISHtoFigure/assets/109809682/3144bb44-f809-43e4-b348-6a69110cf1b0)
