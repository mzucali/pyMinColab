# coding=utf-8
'''
Created on Mar 29, 2019

@author: miki
'''


from copy import deepcopy
import pandas as pd
from mincalclib import formula, inoutfile
import matplotlib.pyplot as plt ###2 nov
#from matplotlib import interactive ###2 nove
import openpyxl
import seaborn as sns
#plt.style.use('seaborn')

class dataset(object):
    '''
    classdocs
    '''
    #inputfile_path = 'file.xlsx'
    #input_data_oxides_sample_mineral_OX_list = []
    #recalc_data_oxides_cats_OX__list = []
    #recalc_data_oxides_cats_OX_by_mineral_list = []
    #recalc_data_oxides_cats_OX_list = []; ## RISULTATI
    def __init__(self, inputfile_path):# CALL dataset.dataset(fileINPUT)

        # global dict_recalc_data_oxides_cats_OX_by_mineral_list;
        list_df_input_data_oxides_sample_mineral_OX_dict = inoutfile.readFILE_E_ESTRAI_DATI_MA_CONTROLLA_MINLABEL_SET_OX(inputfile_path)
        #print("DATASET2_1 list_df_input_data_oxides_sample_mineral_OX_dict", list_df_input_data_oxides_sample_mineral_OX_dict)
        pd_data = pd.DataFrame.from_dict(list_df_input_data_oxides_sample_mineral_OX_dict)
        #print("DATASET2_1.1 dataframe from ORDERED dict: ")
        for item in pd_data.iterrows():
            print("DATA INPUT")
            print(item)
        #print("OUTPUT ALL INPUT DATA",pd_data)
        print("NOW STARTING RECALC PROCEDURE\n")
        ## quello che segue ha come output una lista di analisi ricalcolate utilizzano FORMULA
        recalc_data_oxides_cats_OX_list = formula.formula_for_a_list_of_dict_oxides(list_df_input_data_oxides_sample_mineral_OX_dict)
        #print("DATASET2_2 recalc_data_oxides_cats_OX_list TUTTE LE ANALISI RICALCOLATE", recalc_data_oxides_cats_OX_list)
        pd_data2 = pd.DataFrame.from_dict(recalc_data_oxides_cats_OX_list)
        for item in pd_data2.iterrows():
            print("DATA RECALC")
            print(item)
        print(pd_data2)

        new_list = deepcopy(recalc_data_oxides_cats_OX_list)
        dict_recalc_data_oxides_cats_OX_by_mineral_list = formula.extract_check_calc_specific_sites(new_list)

        global fileOUT;
        fileOUT = inoutfile.write_out_base_data(recalc_data_oxides_cats_OX_list, inputfile_path)
        print("WRITE TO EXCEL FILE BASIC RECALC + TAB transpose")
        # InOutFile.write_out_data_by_mineral_with_specific_sites(dict_recalc_data_oxides_cats_OX_by_mineral_list, fileOUT)
        
        inoutfile.write_out_data_by_mineral_with_specific_sites2(dict_recalc_data_oxides_cats_OX_by_mineral_list, fileOUT)
        print("WRITE TO THE SAME EXCEL FILE worksheets, one for each mineral group")

        inoutfile.writeAX_formatted_input(dict_recalc_data_oxides_cats_OX_by_mineral_list, fileOUT)
        print("WRITE TO EXCEL a last worksheet with same INPUT BUT in AX format")
        return
    
    # def return_recalculated_data(self):
    #     return recalc_data_oxides_cats_OX_by_mineral_list

    def return_fileout(self):
        return fileOUT


#===============================================================================

####RUN RUN RUN######
      
if __name__ == '__main__':
    dataset()
    