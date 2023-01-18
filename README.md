# pyMinColab
pyMin, versione Colab 2023

by Michele Zucali, Department of Earth Sciences - University of Milan - Italy

https://github.com/mzucali/pyMinColab

This is a basic code to re-calculate mineral structural formula for rock-forming mineral starting from SEM-EMPA data, Wt% of oxides (e.g., SiO2, Al2O3, MgO, etc.).

*********************
HOW TO USE IT

1) Select the pyMinColab0X.ipynb file
2) Select the Open in Colab banner
3) You will be re-directed to Google Colab (you need a google account) => works better in Chrome
4) There, follow the instructions

*********************
INPUT FILE PREPARATION
1) INPUT file format is preferibly XLSX but XLS, TAB, CSV, TXT are also accepted.

2) MANDATORY headers are Sample, Mineral and oxides names (e.g. SiO2, Al2O3, MgO, etc.). Case INSENSITIVE, so SIO2, SIo2, SiO2, sio2, siO2, sIo2, ALL accepted!

3) REMOVE any column with numerical data NOT oxides names (e.g., TOTAL), but you can leave any text comment

4) SAMPLE column is FREE and reports sample your labels (e.g., 2mZB26_domain2_Grt34)

5) MINERAL column is mandatory and report a label specific for the mineral phase (e.g., grt, als, ttn, amp, etc...). Mineral has a specific list with a large number of cases.

HERE links to an Example_INPUT_FILE (xlsx) [https://github.com/mzucali/pyMinColab/blob/8f00b4148f715caabdbe38331063c9e9c2679e84/testData/example_input_file.xlsx] and MINERAL_lables [https://github.com/mzucali/pyMinColab/blob/8f00b4148f715caabdbe38331063c9e9c2679e84/testData/labelsMIN.xlsx]

HOW TO RUN your INPUT File

1) select Run All from Runtime menu

2) select Choose Files form the button appeared at the bottom of this page (as your run Run All not before)

3) it will start the computation with a LONG list of outputs as it finished a folder mydata will be created with your input file, the output file (inputfilename_OUT)

4) you can download the output


## 11 January 2023
