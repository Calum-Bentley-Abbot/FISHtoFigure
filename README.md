# FISHtoFigure
A Python-based platform for the in-depth analysis of smFISH data

Spatial transcriptomic tools, such as single molecule fluorescent in situ hybridisation (smFISH) provide a means to image transcriptional factors within tissues. However, resulting datasets are large and tools for quantifying these data are lacking. The aim of this project was to generate a tool for the automated detection of in situ hybridisation signals. FISHtoFigure enables in-depth probing of the transcriptome in smFISH image data quantified using QuPath. QuPath quantified data can either be directly used as input data for FISHtoFigure or quantified datasets from multiple images can be concatenated using the preprocessing tool before analysis with FISHtoFigure.  FISHtoFigure analysis capacities: Plot transcript occurences: Histogram showing number of cells expressing a given number of spots for each RNA target channel. (This recreates the pre-existing in-house histographic analysis of quantified smFISH data within QuPath) Plot transcript distribution: Scatter plot showing quantified transcriptional spot data in a format analogous to the input image. This function creates a plot in which each point in x/y represents a cell in the input image (as defined by the x/y cell centroid data in the quantified image datafile). Points are plotted and coloured by RNA target channel, points are sized by number of RNA transcripts expressed within the given cell. This function provides a means to validate the data quantification carried out in QuPath and the data harvesting conducted by FISHtoFigure by directly comparing this plot with the input image, in addition to providing a quantified equivalent of the input smFISH image. The threshold function allows users to define a minimum number of transcripts which must be expressed by a cell for it to be included in the distribution plot. This allows for the removal of low-level background transcript expression. Transcript abundance analysis: Differential transcript expression analysis can be conducted between multiple quantified datasets. Names of target channels and datasets being compared will be shown on analysis outputs as they appear in the Channel names and Dataset names lists provided by the user input. RNA target channel names must be defined in the order they were quantified in QuPath, and dataset names should named in the order they appear in the input directory. Multi-target abundance analysis: Conducts differential transcript expression analysis on cells expressing a user defined set of targets, enabling analysis of specific cell profiles or cell types in quantified smFISH data.  Please note: When defining channel names and dataset names as they should appear on analysis outputs, please separate names by a comma and a single space i.e., ", "


MIT License

Copyright (c) 2022 Calum Bentley-Abbot

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
