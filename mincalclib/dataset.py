# coding=utf-8
'''
Created on Mar 29, 2019

@author: miki
'''


from copy import deepcopy
import pandas as pd
from mincalclib import formula, inoutfile
#import formula, inoutfile # 6 january 2023 tolto mincalclib
import matplotlib.pyplot as plt ###2 nov
#from matplotlib import interactive ###2 nove
import openpyxl
import seaborn as sns
plt.style.use('seaborn-whitegrid')

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

        # global recalc_data_oxides_cats_OX_by_mineral_list;
        input_data_oxides_sample_mineral_OX_list = inoutfile.readFILE_E_ESTRAI_DATI_MA_CONTROLLA_MINLABEL_SET_OX(inputfile_path)
        print("DATASET2_1 input_data_oxides_sample_mineral_OX_list", input_data_oxides_sample_mineral_OX_list)
        pd_data = pd.DataFrame.from_dict(input_data_oxides_sample_mineral_OX_list)
        print("DATASET2_1.1 dataframe from ORDERED dict: ")
        for item in pd_data.iterrows():
            print(item)
        print(pd_data)

        recalc_data_oxides_cats_OX_list = formula.formula_for_a_list_of_dict_oxides(input_data_oxides_sample_mineral_OX_list)
        print("DATASET2_2 recalc_data_oxides_cats_OX_list ", recalc_data_oxides_cats_OX_list)
        pd_data2 = pd.DataFrame.from_dict(recalc_data_oxides_cats_OX_list)
        for item in pd_data2.iterrows():
            print(item)
        print(pd_data2)

        new_list = deepcopy(recalc_data_oxides_cats_OX_list)
        recalc_data_oxides_cats_OX_by_mineral_list = formula.extract_check_calc_specific_sites(new_list)

        global fileOUT;
        fileOUT = inoutfile.write_out_base_data(recalc_data_oxides_cats_OX_list, inputfile_path)
        print("WRITE TO EXCEL FILE BASIC RECALC + TAB transpose")
        # InOutFile.write_out_data_by_mineral_with_specific_sites(recalc_data_oxides_cats_OX_by_mineral_list, fileOUT)
        
        inoutfile.write_out_data_by_mineral_with_specific_sites2(recalc_data_oxides_cats_OX_by_mineral_list, fileOUT)
        print("WRITE TO THE SAME EXCEL FILE worksheets, one for each mineral group")

        inoutfile.writeAX_formatted_input(recalc_data_oxides_cats_OX_by_mineral_list, fileOUT)
        print("WRITE TO EXCEL a last worksheet with same INPUT BUT in AX format")
        return
    
    def return_recalculated_data(self):
        return recalc_data_oxides_cats_OX_by_mineral_list

    def return_fileout(self):
        return fileOUT

    # def plot_data_recalculated(self, data):
    #     #print(type(data))
    #     pandas_data=pd.read_excel(fileOUT, sheet_name='APPEND', index_col=0, engine='openpyxl')
    #     print(pandas_data)
    #     #sns.scatterplot(x="SiO2", y="Al2O3", data=pandas_data, hue="mineral")
    #     #plt.show()
    #     #df=pd.read_excel('/Users/miki/Dropbox/Development/PycharmProjects/pyMin3/src/input_formatDHZ_OUT.xlsx',sheet_name='APPEND')
    #     df = pd.read_excel(fileOUT,sheet_name='APPEND', engine='openpyxl')
    #     f1 = plt.figure(1)
    #     df1 = df[['SiO2', 'Al2O3', 'FeO', 'MgO', 'mineral']]
    #     sns.pairplot(df1, hue="mineral")
    #     #f1.show()
    #     interactive(True)
    #     plt.show()
    #
    #     f2 = plt.figure(2)
    #     df2 = df[['Na2O', 'CaO', 'K2O', 'mineral']]
    #     sns.pairplot(df2, hue="mineral")
    #     interactive(False)
    #     plt.show()
    #
    #     #input()

    def read_pd_data(self,pd_data):
            print("pandas in dataset")
            print(pd_data)

#===============================================================================

####RUN RUN RUN######
      
if __name__ == '__main__':
    dataset()
    