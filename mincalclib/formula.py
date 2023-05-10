'''
Created on Mar 28, 2019

Jan 27, 2023

@author: miki
'''

from collections import OrderedDict
from copy import deepcopy
#import config

import scipy.constants

from mincalclib.mineral_constants import dict_molecular_weights, dict_oxydes_by_formula, \
    dict_cations_by_formula, list_oxides_order, list_cations_order, dict_mineral_oxigens, dict_cation_labels
from numpy import math

#####################

dict_data_input_Ox = {}  # input OX data from FILE
dict_data_recalc_Ox = {}  # input OX data plus SUM
dict_mol_proportion = {}
dict_wt_perc_oxides = {}
dict_mol_by_oxygens = {}
cats_per_oxy_dict = {}
dict_mineral_Ox = {}
dict_mineral_phase = {}
dict_oxygens_prop = {}
dict_completo = {}
cation_per_oxy_sum = 0
mol_prop_sum = 0
oxygens = 0
# oxygeni = 0
mol_prop_by_oxygens_sum = 0
nyx = 0
oxygens_in_formula_dict = {}
cations_apfu_dict_list = []
data_input_Ox_dict_list = []  # ossidi in entrata letti dal FILE
oxygens_in_formula_list = []
data_Ox_with_OX_list = []


# list_oxides_order = ['Sample','mineral','SiO2', 'TiO2', 'Al2O3','Fe2O3','FeO','MnO','MgO','CaO','Na2O','K2O',
#                 'Th2O3','PbO','UO2','Cr2O3','ZnO','NiO','P2O5','La2O3','Y2O3','Ce2O3','Pr2O3','As2O5', 'Dy2O5','Gd2O3','OxSum', 'OX'] 
# 
# list_cations_order = ['Si', 'Ti', 'Al','AlVI','AlIV','Fe3','Fe2','Mn','Mg','Ca','Na','K',
#                 'Th','Pb','U','Cr','Zn','Ni','P','La','Y','Ce','Pr','As', 'Dy','Gd','SUMcat']


def formula_for_a_list_of_dict_oxides(lista):
    print("STARTING FORMULA formula_for_a_list_of_dict_oxides(lista)")
    print("input from dataset")
    listaOUT = []
    data_input_Ox_dict_list = lista
    print("data_input_Ox_dict_list...\n", data_input_Ox_dict_list)
    # per ogni analisi nella lista di analisi ricalcola la formula
    for input_data_OX_single_dict in data_input_Ox_dict_list:
        #print("input...", input_data_OX_single_dict)
        formula_from_oxides(input_data_OX_single_dict)
        #print("dict_completo", dict_completo)
        listaOUT.append(dict_completo)
        #print("listaOUT", listaOUT)

    print("FROM formula_calc formula_for_a_list_of_dict_oxides")
    print("data_Ox_with_OX_list: ", data_Ox_with_OX_list)
    print("cations_apfu_dict_list", cations_apfu_dict_list)
    print("LISTAOUT...", listaOUT)

    return listaOUT

def case_insensitive_key(a,k): # a=> dict dell'analisi; k => valore della lista es. SiO2, mineral
    for k2 in a.keys():
          k = k.casefold()
          return [a[k2] for k2 in a if k2 == k]
# print 'yes' if case_insensitive_key(a,'Xyz') else 'no'

def flat(key): # a=> dict dell'analisi; k => valore della lista es. SiO2, mineral
    k = key.upper().lower()
    #k = key.lower()
    return k

## flat(key0) in (flat(key) for key in list(dict.keys()))



def compareLabelsDictDataToListOx(dict_data, list_oxides_order):
  dict_unsorted_data_recalc_Ox = {}
  for key,val in dict_data.items():
    # print("key: ",key)
    # print("flat key:", flat(key))
    for k in list_oxides_order: # controlla tutti i termini nella list_oxides_order (e.g., sample, mineral
      # print("list_oxides_order: ",k)
      # print("flat k:", flat(k))
      #if k.upper().lower() in (key.upper().lower()):
      if flat(k) in flat(key):
        # print("key: ", key, "exists in list :",k)
        item = [(k, dict_data[key])]
        # print("item: ",item)
      #else:
      #  print("cannot find: ", k)
    dict_unsorted_data_recalc_Ox.update(item)

  return dict_unsorted_data_recalc_Ox

## RIORDINA un dict di ossidi {'SiO2':23.34, 'TiO2':1.2}
## PERO' deve avere già i labels corretti come in list_oxides_order
def sortDictOxides(dict_unsorted_Ox):
    dict_sorted_Ox ={}
    for k in list_oxides_order:
        if k in dict_unsorted_Ox.keys(): # se quel valore è in
            item = [(k, dict_unsorted_Ox[k])]  # for k in order]
            #print("items oxide:", item)
        #elif k not in dict_unsorted_Ox.keys():
            #print("missing value: ", k)
        dict_sorted_Ox.update(item)
    return dict_sorted_Ox

## RIORDINA un dict di cationi {'Si':23.34, 'Ti':1.2}
## PERO' deve avere già i labels corretti come in list_oxides_order
def sortDictCations(dict_unsorted_cats):
    dict_sorted_Ox ={}
    for k in list_cations_order:
    # print("list_cations_order: ",k)
      if k in dict_unsorted_cats.keys():
        item = [(k, dict_unsorted_cats[k])]  # for k in order]
        # print("item cat:", item)
  #    elif k not in dict_unsorted_cats.keys():
        #print("missing value in cations: ", k)
        # print("???")
    dict_sorted_Ox.update(item)

    return dict_sorted_Ox

def formula_from_oxides(mineral_Ox_dict):
    '''
    QUESTA LA FUNZIONE che gestisce il ricalcolo secondo moduli successivi
    
    '''

    '''
    STARTING
    '''
    # dict_mineral_Ox=dict_mineral_Ox
    #print()
    #print("pyPT.calculation.formula_calc: printing oxides")
    #print("FEW testing before start calculations")
    #print("mineral_OX_dict NO COMPARED", mineral_Ox_dict)
    mineral_Ox_dict=compareLabelsDictDataToListOx(mineral_Ox_dict,list_oxides_order)
    #print("list oxes order",list_oxides_order)
    #print("mineral_OX_dict COMPARED",mineral_Ox_dict )
    global nyx
    # #print("\nK = V")
    # for k, v in mineral_Ox_dict.items():
    #     print(k + " = " + str(v))
    # print()
    print("\nstarting formula")
    '''
    COPYING wt percent oxides
    '''
    global dict_wt_perc_oxides
    dict_wt_perc_oxides = deepcopy(mineral_Ox_dict)
    '''
    CALC SUM of oxides and update dict_mineral_Ox
    '''
    #print("\nSUM OXIDES")
    sum_oxides(mineral_Ox_dict)
    # addValueDictEasy("SumOX", wt_perc_oxides_sum, dict_wt_perc_oxides)
    #print("dict_mineral_Ox con SOMMA")
    #print_mineral_key_value(mineral_Ox_dict)
    #print("print_mineral_key_value(dict_wt_perc_oxides)")
    #print_mineral_key_value(dict_wt_perc_oxides)
    #print("molecular weight used")
    #print_mineral_key_value(dict_molecular_weights)
    #print("\nMOL PROPORTION")
    global dict_mol_proportion
    global dict_oxygens_prop
    # global dict_mol_proportion
    # dict_mol_proportion = mol_proportion(dict_mineral_Ox)
    dict_mol_proportion, mol_prop_sum = mol_proportion(dict_wt_perc_oxides)
    #print("\nmole proportion dict EXT (updated?): ")
    #print(dict_mol_proportion)
    #print("MOL prop sum EXT")
    #print(mol_prop_sum)
    #print("\nMULTIPLY BY OXYGENS")
    mol_by_oxygens_dict, mol_prop_by_oxygens_sum = multipl_by_num_oxygens(dict_mol_proportion)
    #print("\nOXYGENS PROPORTIONS")
    #print("dict_mol_by_oxygens type ", type(mol_by_oxygens_dict))

    #print(".dict_oxygens_prop type ", type(dict_oxygens_prop))
    dict_oxygens_prop = oxygen_proportion(dict_wt_perc_oxides, mol_by_oxygens_dict, mol_prop_by_oxygens_sum)
    #print("OXYGENS from Formula = " + str(oxygens))
    #print("oxygens_in_formula_list[nyx] ", oxygens_in_formula_list[nyx])

    oxygens_in_formula_list[nyx] = oxygens
    #print("last added oxygens value = ", oxygens_in_formula_list[nyx])
    #print("all added oxygens values = ", oxygens_in_formula_list)
    # oxygens_in_formula_dict_list.append(oxygens_in_formula_dict)

    # print "oxygens_in_formula_dict_list: ", oxygens_in_formula_dict_list[nyx]
    nyx += 1
    #print("\nCATION APFU")

    # global cations_apfu_dict_list
    global cats_per_oxy_dict
    global cation_per_oxy_sum
    cats_per_oxy_dict, cation_per_oxy_sum = cations_apfu(dict_oxygens_prop)
    #print("FORMULA cats_per_oxy_dict ", cats_per_oxy_dict)

    calcSiteDistribution(cats_per_oxy_dict)
    headers_written = False
    #print("\nFormula calculation terminated")
    #print()

    #print("MINERAL PHASE DICT")
    #print("ossidi")
    print(oxygens_in_formula_list)
    #print("cationi")
    print(cats_per_oxy_dict)

    global dict_data_recalc_Ox
    dict_data_recalc_Ox.update({'OX': oxygens})
    #print("dict_data_recalc_Ox before SORTING", dict_data_recalc_Ox)

    dict_sorted_data_recalc_Ox = {}
    dict_unsorted_data_recalc_Ox = compareLabelsDictDataToListOx(dict_data_recalc_Ox, list_oxides_order) # <= test 2/2/23
    dict_ordered_Ox = sortDictOxides(dict_unsorted_data_recalc_Ox) # <= test 2/2/23
    #print("dict_ordered_Ox: ",dict_ordered_Ox)

    ##sort
    #flat(key0) in (flat(key) for key in list(dict.keys()))
    for k in list_oxides_order: # controlla tutti i termini nella list_oxides_order (e.g., sample, mineral
        ##items = [(k, dict_data_recalc_Ox[k])] if case_insensitive_key(dict_data_recalc_Ox, k) else print('no') ### test per controllo case sensitive
#        print("list_oxides_order: ",k.lower())
        #print("key.lower: ", (key.lower() for key in list(dict_data_recalc_Ox.keys())))
        #lista = []
        if k in dict_data_recalc_Ox.keys(): # se quel valore è in
            items = [(k, dict_data_recalc_Ox[k])]  # for k in order]
 #          #print("items oxide:", items)
        #elif k not in dict_data_recalc_Ox.keys():
            #print("missing value: ", k)

        dict_sorted_data_recalc_Ox.update(items)

    global data_Ox_with_OX_list
    #print("data_Ox_with_OX_list BEFORE",data_Ox_with_OX_list)
 #   data_Ox_with_OX_list.append(dict_sorted_data_recalc_Ox) # <= OLD working check 2/2/23
    data_Ox_with_OX_list.append(dict_ordered_Ox) # <= test 2/2/23
    #print("data_Ox_with_OX_list AFTER",data_Ox_with_OX_list)

    # global cats_per_oxy_dict
    cats_per_oxy_dict.update({"SUMcat": round(cation_per_oxy_sum, 3)})
    cats_per_oxy_dict = changeALLKeys(cats_per_oxy_dict)
    #print("cats_per_oxy_dict Prima: ", cats_per_oxy_dict)
    ##sort
    #sorted_cats_per_oxy_dict = {}
    dict_sorted_cats = sortDictCations(cats_per_oxy_dict) # NEW Feb 2023
    #print("sorted_cats_per_oxy_dict NEW", dict_sorted_cats)  # NEW Feb 2023

    sorted_cats_per_oxy_dict = {}# <= OLD check
    for k in list_cations_order:
        # print("list_cations_order: ",k)
        if k in cats_per_oxy_dict.keys():
            itema = [(k, cats_per_oxy_dict[k])]  # for k in order]
            # print("itema cat:", itema)
       # elif k not in cats_per_oxy_dict.keys():
            #print("missing value in cations: ", k)
            # print("???")

        sorted_cats_per_oxy_dict.update(itema)

    cations_apfu_dict_list.append(sorted_cats_per_oxy_dict)
    #print("sorted_cats_per_oxy_dict OLD", cations_apfu_dict_list)
    global dict_completo
    dict_completo = deepcopy(dict_sorted_data_recalc_Ox)
    dict_completo.update(sorted_cats_per_oxy_dict)

    return dict_completo


def sum_oxides(mineral_dict1):
    #print("\nSUM starts here")
    #    global sum
    summa = 0

    for oxides_value in mineral_dict1.values():
        if type(oxides_value) == float:
            #print("summa che?")
            summa = summa + oxides_value
            #print("somma = ", summa)
        #            print("Progressive Sum = %f") % summa
        else:
            print("not a digitaaa?? ", mineral_dict1.values())

    #print("Total Sum = %f" % summa)
    # global dict_mineral_Ox
    #print("mineral_dict")
    #print(mineral_dict1)
    #    mineral_dict1 = addValueDict("OxSum", sum, mineral_dict1, mineral_dict1)
    mineral_dict1.update({"OxSum": round(summa, 2)})
    #print("UPDATED?")
    #print(mineral_dict1)
    # global dict_data_input_Ox
    # oxides_dict = mineral_dict1
    global dict_data_recalc_Ox
    dict_data_recalc_Ox = mineral_dict1
    #print("SUM  = " + str(mineral_dict1['OxSum']))
    #print()
    return round(summa, 2)


def addValueDict(key, val, old_dict, new_dict):
    new_dict.update({key: val})
    return new_dict


def print_mineral_keys(mineral_dict):
    #print("\nprint_mineral_keys")
    for mineral_keys in mineral_dict.keys():
        print(mineral_keys)
    return mineral_dict


def print_mineral_key_value(dicto):
    for k, v in dicto.items():
        print("{}".format(k), " = {}".format(v))


def mol_proportion(wt_oxides_dict):
    #   global mol_prop_sum
    #   global dict_mol_proportion
    mol_proportion_dict_tmp = OrderedDict()  ##<<<====
    # mol_proportion_dict_tmp = {}
    mol_prop_sum_tmp = 0
    #print("mol_prop_sum_tmp = " + str(mol_prop_sum))
    for k, v in wt_oxides_dict.items():
        #print("KAPPA: ",k)
        if k in dict_molecular_weights:
            mol_prop = v / dict_molecular_weights[k]
            #            global dict_mol_proportion
            mol_proportion_dict_tmp[k] = round(mol_prop, 3)
            #            dict_mol_proportion[k] = mol_prop
            # print "mol_prop: %f" % mol_prop
            # global mol_prop_sum
            mol_prop_sum_tmp = mol_prop_sum_tmp + mol_prop
            # print "mol_prop sum progress: %f" % mol_prop_sum
        else:
            None
            print("none....")

    #print("mol_prop sum total: %f" % mol_prop_sum_tmp)
    #print("\ndict_mol_proportion NO sum")
    #print(mol_proportion_dict_tmp)
    # addValueDictEasy("mol_prop_sum", mol_prop_sum_tmp, mol_proportion_dict_tmp)
    return mol_proportion_dict_tmp, mol_prop_sum_tmp


def multipl_by_num_oxygens(mol_proportion_dict1):
    # mol_prop_by_oxygens_sum_tmp
    mol_by_oxygens_dict_tmp = OrderedDict()  # <<==
    #    mol_by_oxygens_dict_tmp = {}
    mol_prop_by_oxygens_sum_tmp = 0
    for k, v in mol_proportion_dict1.items():
        # if k in dict_oxydes_by_formula:
        # k = str(k).replace("_mol","")
        if k in dict_oxydes_by_formula:
            mol_by_oxygens = v * dict_oxydes_by_formula[k]
            mol_by_oxygens_dict_tmp[k] = mol_by_oxygens
            mol_prop_by_oxygens_sum_tmp = mol_prop_by_oxygens_sum_tmp + mol_by_oxygens
            # print (mol_by_oxygens_dict_tmp[k])
            # print ("progression SUM = " + str(mol_prop_by_oxygens_sum_tmp))
    #print("final SUM = " + str(mol_prop_by_oxygens_sum_tmp))
    #print("\ndict_mol_by_oxygens")
    #print_mineral_key_value(mol_by_oxygens_dict_tmp)
    return mol_by_oxygens_dict_tmp, mol_prop_by_oxygens_sum_tmp


def oxygen_proportion(mineral_input_dict, mol_by_oxygens_dict, mol_prop_sum):
    oxygens_prop_dict_tmp = OrderedDict()  # <<==
    # oxygens_prop_dict_tmp = {}
    # .dict_wt_perc_oxides = mineral_input_dict
    # print("mineral_input_dict: ", mineral_input_dict)
    # print(".dict_wt_perc_oxides ", .dict_wt_perc_oxides)
    #print("searching for mineral: ", mineral_input_dict['mineral'])
    # print ("searching for mineral: " + mineral_input_dict['Mineral'].casefold())
    # labels = labels
    for k, v in dict_mineral_oxigens.items():
        k.lower()
        #print("k.lowerAAA: ", k.lower())
    global oxygens
    for k, v in dict_mineral_oxigens.items():
        if k.lower() == mineral_input_dict['mineral'.casefold()].lower():
         #   print(mineral_input_dict['mineral'.casefold()] + " found, it has %s oxygens" % str(v))
            oxygens = v

    # print ("OXYGENI = ",oxygeni)
    # print ("OXYGENS = ",oxygens)
    # print("len: ",len(oxygens_in_formula_list))
    ox_num = 0
    global oxygens_in_formula_dict
    #print("oxygens_in_formula_dict", oxygens_in_formula_dict)
    # oxygens_in_formula_dict = []
    oxygens_in_formula_dict[ox_num] = oxygens
    # print("oxygens_in_formula_list type", oxygens_in_formula_list)
    oxygens_in_formula_list.append(oxygens)
    # print(".oxygens_in_formula_list type", oxygens_in_formula_list)
    # print("oxygens_in_formula_dict :", oxygens_in_formula_dict)
    ox_num += 1
    # print(".oxygens_in_formula_list type", oxygens_in_formula_list)

    for k, v in mol_by_oxygens_dict.items():
        #print(k)
        #       if type(v) == float:
        oxygen_prop = v * (oxygens / mol_prop_sum)
        # print "=> v * (oxygens / sum_mol_prop_by_oxygens) = "+ str(v * (oxygens / mol_prop_sum))

        oxygens_prop_dict_tmp[k] = round(oxygen_prop, 3)
        # oxygens_prop_dict_tmp.update(oxygen_prop)

    #print("Oxygens_prop_dict")
    #print_mineral_key_value(oxygens_prop_dict_tmp)
    return oxygens_prop_dict_tmp

    #print("oxygens_in_formula_dict[]")
    #print_mineral_key_value(oxygens_in_formula_dict)
    return oxygens_in_formula_dict


def cations_apfu(oxygens_prop_dict_tmp):
    cats_per_oxy_dict_tmp = OrderedDict()  # <<==

    cats_per_oxy_sum_tmp = 0
    for k, v in oxygens_prop_dict_tmp.items():
        cation_per_oxy = round(v, 3) * round(dict_cations_by_formula[k], 3)

        cats_per_oxy_dict_tmp[k] = round(cation_per_oxy, 3)
        cats_per_oxy_sum_tmp = round(cats_per_oxy_sum_tmp, 3) + cation_per_oxy

    #print("Total SUM CATIONS = " + str(cats_per_oxy_sum_tmp))

    return cats_per_oxy_dict_tmp, cats_per_oxy_sum_tmp


def roundValuesInDict(dictio):
    for k, v in dictio.items():
        dictio[k] = round(v, 3)
    return dictio


def calcSiteDistribution(cats_per_oxy_dict):
    print("TO BE IMPLEMENTED")


def changeKeys(dictionary, old_key, new_key):
    #print(dictionary)
    for k, v in dictionary.items():
        #print("keys ", k)
        #print("value ", v)

        new_key = "Fe2"
        old_key = "FeO"
        dictionary[new_key] = dictionary[old_key]
        del dictionary[old_key]
        #print(dictionary)
        #for k, v in dictionary.items():
            #print("keys ", k)
           # print("value ", v)
    return dictionary


def changeALLKeys(cats_dict):
    # module to change labels in cation dict because it now uses same as oxides
    #print("cats_dict before...")
    #print(cats_dict)

    for key in cats_dict.keys() & dict_cation_labels.keys():
        #print("changeALLKeys found: ", key)

        new_key = dict_cation_labels[key]
        old_key = key
        cats_dict[new_key] = cats_dict[old_key]
        del cats_dict[old_key]
    #print("cats_dict after...")
    #print(cats_dict)
    return cats_dict


def extract_check_calc_specific_sites(recalc_data_oxides_cats_OX_list):
    #print("\n\tFORMULA=> extract_check_calc_specific_sites(recalc_data_oxides_cats_OX__list)")

    #print("\t\tDEVO SEPARARE PER LISTE DI MINERALE")
    #print("\t\t\tPER OGNI LISTA DI MINERALE FARE I CALCOLI")
    #print("\t\t\t\tRITORNARE LISTE DI LISTE DI MINERALI CON specific sites")
    #print()

    a_args = []
    #print("recalc_data_oxides_cats_OX_list\n")
    #print(recalc_data_oxides_cats_OX_list)

    lista = []
    for each_analysis in recalc_data_oxides_cats_OX_list:
        lista.append(each_analysis)
    #print("LISTA ", lista)

    for l in lista:
        #print("l: ", l)
        if l['mineral'] not in a_args:
            a_args += [l['mineral']]
            new_list = [[]] * len(a_args)

    dict_of_list = {}
    for i in range(len(a_args)):
        for l in [l for l in lista if l['mineral'] == a_args[i]]:
            new_list[i] = new_list[i] + [l]
            sublist_list = new_list[i]
        dict_of_list[a_args[i]] = sublist_list

    for mine, value in dict_of_list.items():
        #print("\nmineral group = ", mine, 'is: ', value)
        global zzz
        zzz = 100.00001
        if mine == 'grt':
            # GARNET#
            for single in value:
                alm = single['Fe2'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                py = single['Mg'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                gr = single['Ca'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                sps = single['Mn'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                XFe = single['Fe2'] / (single['Fe2'] + single['Mg']+single['Mn']+single['Ca'])
                XMg = single['Mg'] / (single['Fe2'] + single['Mg']+single['Mn']+single['Ca'])
                XMn = single['Mn'] / (single['Fe2'] + single['Mg']+single['Mn']+single['Ca'])
                XCa = single['Ca'] / (single['Fe2'] + single['Mg'] + single['Mn']+single['Ca'])

                # T SITE
                if single['Si']<3:
                    Si_T = single['Si']
                else:
                    Si_T = 3

                if 3-single['Si']>0:
                    if 3-single['Si'] > single['Al']:
                        Al_T = single['Al']
                    else:
                        Al_T = 3 - Si_T
                    pass
                else:
                    Al_T = 0


                Sum_T = Si_T + Al_T

                # Y SITE
                if single['Si']<3:
                    Si_Y = 0
                else:
                    Si_Y = single['Si']-3

                Al_Y = single['Al'] - Al_T
                Ti_Y = single['Ti']
                Cr_Y = single['Cr']

                if (Si_Y + Al_Y + Ti_Y + Cr_Y) < 2 and (2-(Si_Y + Al_Y + Ti_Y + Cr_Y)) > single['Mg']:
                    Mg_Y = single['Mg']
                else:
                    Mg_Y = 2-(Si_Y + Al_Y + Ti_Y + Cr_Y)

                if (Si_Y + Al_Y + Ti_Y + Cr_Y + Mg_Y) < 2 and (2-(Si_Y + Al_Y + Ti_Y + Cr_Y + Mg_Y)) > single['Fe2']:
                    Fe2_Y = single['Fe2']
                else:
                    Fe2_Y = 2-(Si_Y + Al_Y + Ti_Y + Cr_Y + Mg_Y)

                if (Si_Y + Al_Y + Ti_Y + Cr_Y + Mg_Y + Fe2_Y) < 2 and 2-(Si_Y + Al_Y + Ti_Y + Cr_Y + Mg_Y + Fe2_Y) > single['Mn']:
                    Mn_Y = single['Mn']
                else:
                    Mn_Y = 2-(Si_Y + Al_Y + Ti_Y + Cr_Y + Mg_Y + Fe2_Y)

                Sum_Y = Si_Y + Al_Y + Ti_Y + Cr_Y + Fe2_Y + Mg_Y + Mn_Y

                # X SITE
                if 'Y' in single:
                    Y_X = single['Y']
                Mg_X = single['Mg'] - Mg_Y
                Fe2_X = single['Fe2'] - Fe2_Y
                Mn_X = single['Mn'] - Mn_Y
                Ca_X = single['Ca']
                Na_X = single['Na']
                try:
                    Y_X
                except NameError:
                    #print("no Y")
                    Sum_X = Mg_X + Fe2_X + Mn_X + Ca_X + Na_X
                else:
                    Sum_X = Y_X + Mg_X + Fe2_X + Mn_X + Ca_X + Na_X
                #if Y_X:
                #    Sum_X = Y_X + Mg_X + Fe2_X + Mn_X + Ca_X + Na_X
                #else:
                #    Sum_X = Mg_X + Fe2_X + Mn_X + Ca_X + Na_X


                '''
                Fe3+ = 2*X*(1-T/S)
                X=>oxigens in formula
                T=>ideal number of cations
                S=>observed cations
                '''
                if 'Fe3' in single:
                    #print("good to know")
                    pass
                else:
                    #print("CATIONI SUM GRT: ", single['SUMcat'])
                    Fe3 = 2 * 12 * (1 - 8 / single['SUMcat'])
                    single.update({'Fe3': round(Fe3, 3)})
                    pass

                single.update({'alm': round(alm, 3)})
                single.update({'py': round(py, 3)})
                single.update({'gr': round(gr, 3)})
                single.update({'sps': round(sps, 3)})
                single.update({'XFe': round(XFe, 3)})
                single.update({'XMg': round(XMg, 3)})
                single.update({'XMn': round(XMn, 3)})
                single.update({'XCa': round(XCa, 3)})
                single.update({'Si_T': round(Si_T,3)})
                single.update({'Al_T': round(Al_T,3)})
                single.update({'Sum_T': round(Sum_T, 3)})
                single.update({'Si_Y': round(Si_Y,3)})
                single.update({'Al_Y': round(Al_Y,3)})
                single.update({'Ti_Y': round(Ti_Y, 3)})
                single.update({'Cr_Y': round(Cr_Y, 3)})
                single.update({'Mg_Y': round(Mg_Y, 3)})
                single.update({'Fe2_Y': round(Fe2_Y, 3)})
                single.update({'Mn_Y': round(Mn_Y, 3)})
                single.update({'Sum_Y': round(Sum_Y, 3)})
                try:
                    Y_X
                #except NameError:
                    #print("no Y")
                else:
                    single.update({'Y_X': round(Y_X,3)})

                single.update({'Mg_X': round(Mg_X, 3)})
                single.update({'Fe2_X': round(Fe2_X, 3)})
                single.update({'Mn_X': round(Mn_X, 3)})
                single.update({'Ca_X': round(Ca_X, 3)})
                single.update({'Na_X': round(Na_X, 3)})
                single.update({'Sum_X': round(Sum_X, 3)})

                #print("every mineral analysis: ", single, "")
                # P_grt(kbar@550°C)-doi.org/10.3390/min9090540
                TempK = 923  # 650 Celsius
                R = scipy.constants.R
                Grt_a = 0.337*(XFe**2)-24.976*(XMg**2)+9.67*(XCa**2)-5.07*(XMn**2)+1.4335*XFe*XMg\
                    -20.014*XFe*XCa-4.6665*XFe*XMn-16.1735*XMg*XCa-16.173*XMg*XMn-5.4735*XCa*XMn
                #print("Grt_a = ", Grt_a)
                Grt_b = 0.04*(XFe**2)+0.102*(XMg**2)-0.135*(XCa**2)-5.19*(XMn**2)-0.1515*XFe*XMg\
                    +0.19*XFe*XCa+0.1165*XFe*XMn+0.3315*XMg*XCa+0.137*XMg*XMn+0.0035*XCa*XMn
                #print("Grt_b = ", Grt_b)
                Grt_c = -1304.0*(XFe**2)+71786*(XCa**2)-19932.0*(XCa**2)+1002.0*(XMn**2)\
                    +8082.5*XFe*XMg+42472*XFe*XCa+9122*XFe*XMn+20191.5*XMg*XCa+42769.5*XMg*XMn+28282*XCa*XMn
                #print("Grt_c = ", Grt_c)
                P_grt = (-8904.5+24.542*TempK+0.45*R*TempK*math.log(XCa/XFe)+0.15*TempK*Grt_a+0.15*Grt_c)/(1-0.15*Grt_b)/1000   ## Minerals 2019, 9(9), 540; https://doi.org/10.3390/min9090540
                single.update({'P_grt(kbar@550°C)-doi.org/10.3390/min9090540': round(P_grt, 3)})
                single.update({'Grt_a': round(Grt_a,5)})
                single.update({'Grt_b': round(Grt_b, 5)})
                single.update({'Grt_c': round(Grt_c, 5)})

        elif mine == 'amph':
            # AMPH#
            for single in value:
                if 8 - single['Si'] > 0:
                    aliv = 8 - single['Si']
                else:
                    aliv = 0
                single.update({'aliv': aliv})

                alvi = single['Al'] - aliv
                single.update({'alvi': round(alvi, 3)})

                single.update({'T': zzz})

                if 'Fe3' in single:
                    print("good to know")
                    pass
                else:
                    print("CATTTIONI SUM: ", single['SUMcat'])
                    Fe3 = 2 * 12 * (1 - 8 / single['SUMcat'])
                    single.update({'Fe3': round(Fe3, 3)})
                    pass

                print("every mineral analysis: ", single, "")

        elif mine == 'px':
            # PYROXENE#
            for single in value:
                if 2 - single['Si'] > 0:
                    aliv = 2 - single['Si']
                else:
                    aliv = 0
                single.update({'aliv': round(aliv, 3)})

                alvi = single['Al'] - aliv
                single.update({'alvi': round(alvi, 3)})

                jd1 = single['Na'] * 2
                single.update({'jd1': round(jd1, 3)})

                if single['alvi'] > (single['Na'] + single['K']):
                    jd2 = single['alvi']
                else:
                    jd2 = single['Na'] + single['K']
                single.update({'jd2': round(jd2, 3)})

                if single['alvi'] > (single['Na'] + single['K']):
                    acm = single['Na'] + single['K'] - single['alvi']
                else:
                    acm = 0

                single.update({'acm': round(acm, 3)})

                if 'Fe3' in single:
                    print("good to know")
                    pass
                else:
                    print("CATTTIONI SUM: ", single['SUMcat'])
                    Fe3 = 2 * 12 * (1 - 8 / single['SUMcat'])
                    single.update({'Fe3': round(Fe3, 3)})
                    pass

                if (single['Fe3'] + single['Cr']) / 2 > single['acm']:
                    CaFeTs = (single['Fe3'] + single['Cr']) / 2
                else:
                    CaFeTs = 0
                single.update({'CaFeTs': round(CaFeTs, 3)})

                CaTiTs = single['Ti']
                single.update({'CaTiTs': round(CaTiTs, 3)})

                if ((single['aliv'] + single['alvi'] - single['jd2'] - 2 * single['Ti']) / 2) > 0:
                    CaTs = (single['aliv'] + single['alvi'] - single['jd2'] - 2 * single['Ti']) / 2
                else:
                    CaTs = 0
                single.update({'CaTs': CaTs})

                if (single['Ca'] - single['CaFeTs'] - single['CaTiTs'] - single['CaTs']) > 0:
                    woll = single['Ca'] - single['CaFeTs'] - single['CaTiTs'] - single['CaTs']
                else:
                    woll = 0

                single.update({'woll': round(woll, 3)})

                if 'Ni' in single.keys():
                    en = (single['Mg'] + single['Ni']) / 2
                else:
                    en = (single['Mg'])
                single.update({'en': round(en, 3)})

                fs = (single['Mn'] + single['Fe2']) / 2
                single.update({'fs': round(fs, 3)})

                print("every mineral analysis: ", single, "")

        elif mine == 'bt':
            for single in value:
                #  BIOTITE  ##
                print("every mineral analysis: ", single, "")
                # print("TIIIII: ", single['Ti'])
                #  BIOTITE BAROMETER Jiiang et al 2008 - Acta Petrologica Sinica, 2008
                P_bt = 3.03 * single['Al'] - 6.53  # Jiiang et al 2008 - Acta Petrologica Sinica, 2008
                # Geochemical and Sr-Nd-Hf
                # isotopic compositions of granodiorite from the Wushan
                # copper deposit, Jiangxi Province and their implications
                # for petrogenesis
                single.update({'P_bt(kbar)-Jiang et al 2008-22-OX-Total Al': round(P_bt, 3)})
                T_henry2005 = 0

                if (single['Ti'] > 0.06 and single['Ti'] < 0.6):
                    # print("TIIIIIAAA: ", single['Ti'])
                    b = 4.6482E-09
                    a = -2.3594
                    # b = 4648200000
                    c = -1.7283
                    lnTi = round(math.log(single['Ti']), 3)
                    xmg = round(single['Mg'] / (single['Mg'] + single['Fe2']), 3)

                    print("lnTi ", lnTi)
                    print("xmg ", xmg)

                    primo = lnTi
                    secondo = a
                    terzo = round(c * (math.pow(xmg, 3)), 3)

                    print("terzo", terzo)

                    quarto = round((primo - secondo - terzo), 3)

                    quinto = round((quarto / b), 3)
                    print("quarto ", quarto)
                    print("quinto", quinto)

                    if quinto > 0:
                        finale = math.pow(quinto, 0.333)
                        ##global T_henry2005
                        T_henry2005 = finale


                    else:
                        print("cannot use Henry's calibration, see original paper")
                        single.update({'T_henry2005': 'OutOf_XMg_Range'})
                        pass
                else:
                    print("cannot use Henry's calibration, see original paper")
                    single.update({'T_henry2005': 'OutOf_Ti_Range'})
                    pass

                if (T_henry2005 > 400 and T_henry2005 < 800):
                    single.update({'T_henry2005': round(T_henry2005, 3)})
                else:
                    print("cannot use Henry's calibration, see original paper")
                    single.update({'T_henry2005': 'OutOf_T_Range'})

    return dict_of_list  ##LISTE_DI_LISTE_DI_MINERALI_CON_specific_sites
