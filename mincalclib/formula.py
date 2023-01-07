'''
Created on Mar 28, 2019

@author: miki
'''

from collections import OrderedDict
from copy import deepcopy

import scipy.constants
#import mineral_constants
from mincalclib.mineral_constants import molecular_weights, oxydes_by_formula, \
    cations_by_formula, oxides_order, cations_order, mineral_oxigens, cation_labels
from numpy import math

#####################

data_input_Ox_dict = {}  # input OX data from FILE
data_recalc_Ox_dict = {}  # input OX data plus SUM

mol_proportion_dict = {}
wt_perc_oxides_dict = {}
mol_by_oxygens_dict = {}
cats_per_oxy_dict = {}
mineral_Ox_dict = {}
mineral_phase_dict = {}
oxygens_prop_dict = {}
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


# oxides_order = ['Sample','mineral','SiO2', 'TiO2', 'Al2O3','Fe2O3','FeO','MnO','MgO','CaO','Na2O','K2O',
#                 'Th2O3','PbO','UO2','Cr2O3','ZnO','NiO','P2O5','La2O3','Y2O3','Ce2O3','Pr2O3','As2O5', 'Dy2O5','Gd2O3','OxSum', 'OX'] 
# 
# cations_order = ['Si', 'Ti', 'Al','AlVI','AlIV','Fe3','Fe2','Mn','Mg','Ca','Na','K',
#                 'Th','Pb','U','Cr','Zn','Ni','P','La','Y','Ce','Pr','As', 'Dy','Gd','SUMcat']


def formula_for_a_list_of_dict_oxides(lista):
    print("STARTING FORMULA formula_for_a_list_of_dict_oxides(lista)")

    listaOUT = []
    data_input_Ox_dict_list = lista
    print("data_input_Ox_dict_list...", data_input_Ox_dict_list)
    for input_data_OX_single_dict in data_input_Ox_dict_list:
        print("input...", input_data_OX_single_dict)
        formula_from_oxides(input_data_OX_single_dict)
        print("dict_completo", dict_completo)
        listaOUT.append(dict_completo)
        print("listaOUT", listaOUT)

    print("FROM formula_calc formula_for_a_list_of_dict_oxides")
    print("data_Ox_with_OX_list: ", data_Ox_with_OX_list)
    print("cations_apfu_dict_list", cations_apfu_dict_list)
    print("LISTAOUT...", listaOUT)

    return listaOUT


def formula_from_oxides(mineral_Ox_dict):
    '''
    QUESTA LA FUNZIONE che gestisce il ricalcolo secondo moduli successivi
    
    '''

    '''
    STARTING
    '''
    # mineral_Ox_dict=mineral_Ox_dict
    print()
    print("pyPT.calculation.formula_calc: printing oxides")
    print("FEW testing before start calculations")
    global nyx
    print("\nK = V")
    for k, v in mineral_Ox_dict.items():
        print(k + " = " + str(v))
    print()
    print("\nstarting formula")

    '''
    COPYING wt percent oxides
    '''
    global wt_perc_oxides_dict
    wt_perc_oxides_dict = deepcopy(mineral_Ox_dict)

    '''
    CALC SUM of oxides and update mineral_Ox_dict
    '''
    print("\nSUM OXIDES")
    sum_oxides(mineral_Ox_dict)
    # addValueDictEasy("SumOX", wt_perc_oxides_sum, wt_perc_oxides_dict)
    print("mineral_Ox_dict con SOMMA")
    print_mineral_key_value(mineral_Ox_dict)
    print_mineral_key_value(wt_perc_oxides_dict)

    print("molecular weight used")
    print_mineral_key_value(molecular_weights)
    print("\nMOL PROPORTION")
    global mol_proportion_dict
    global oxygens_prop_dict
    # global mol_proportion_dict
    # mol_proportion_dict = mol_proportion(mineral_Ox_dict)
    mol_proportion_dict, mol_prop_sum = mol_proportion(wt_perc_oxides_dict)
    print("\nmole proportion dict EXT (updated?): ")
    print(mol_proportion_dict)
    print("MOL prop sum EXT")
    print(mol_prop_sum)
    print("\nMULTIPLY BY OXYGENS")
    mol_by_oxygens_dict, mol_prop_by_oxygens_sum = multipl_by_num_oxygens(mol_proportion_dict)
    print("\nOXYGENS PROPORTIONS")
    print("mol_by_oxygens_dict type ", type(mol_by_oxygens_dict))

    print(".oxygens_prop_dict type ", type(oxygens_prop_dict))
    oxygens_prop_dict = oxygen_proportion(wt_perc_oxides_dict, mol_by_oxygens_dict, mol_prop_by_oxygens_sum)
    print("OXYGENS from Formula = " + str(oxygens))
    print("oxygens_in_formula_list[nyx] ", oxygens_in_formula_list[nyx])

    oxygens_in_formula_list[nyx] = oxygens
    print("last added oxygens value = ", oxygens_in_formula_list[nyx])
    print("all added oxygens values = ", oxygens_in_formula_list)
    # oxygens_in_formula_dict_list.append(oxygens_in_formula_dict)

    # print "oxygens_in_formula_dict_list: ", oxygens_in_formula_dict_list[nyx]
    nyx += 1
    print("\nCATION APFU")

    # global cations_apfu_dict_list
    global cats_per_oxy_dict
    global cation_per_oxy_sum
    cats_per_oxy_dict, cation_per_oxy_sum = cations_apfu(oxygens_prop_dict)
    print("FORMULA cats_per_oxy_dict ", cats_per_oxy_dict)

    calcSiteDistribution(cats_per_oxy_dict)
    headers_written = False
    print("\nFormula calculation terminated")
    print()

    print("MINERAL PHASE DICT")
    print("ossidi")
    print(oxygens_in_formula_list)
    print("cationi")
    print(cats_per_oxy_dict)

    global data_recalc_Ox_dict
    data_recalc_Ox_dict.update({'OX': oxygens})
    sorted_data_recalc_Ox_dict = {}
    ##sort
    for k in oxides_order:
        # print("oxides_order: ",k)
        if k in data_recalc_Ox_dict.keys():
            items = [(k, data_recalc_Ox_dict[k])]  # for k in order]
        #   print("items oxide:", items)
        elif k not in data_recalc_Ox_dict.keys():
            print("missing value in oxides: ", k)

        sorted_data_recalc_Ox_dict.update(items)

    global data_Ox_with_OX_list
    data_Ox_with_OX_list.append(sorted_data_recalc_Ox_dict)

    # global cats_per_oxy_dict
    cats_per_oxy_dict.update({"SUMcat": round(cation_per_oxy_sum, 3)})
    cats_per_oxy_dict = changeALLKeys(cats_per_oxy_dict)
    ##sort
    sorted_cats_per_oxy_dict = {}
    for k in cations_order:
        # print("cations_order: ",k)
        if k in cats_per_oxy_dict.keys():
            itema = [(k, cats_per_oxy_dict[k])]  # for k in order]
            # print("itema cat:", itema)
        elif k not in cats_per_oxy_dict.keys():
            print("missing value in cations: ", k)
            # print("???")

        sorted_cats_per_oxy_dict.update(itema)

    cations_apfu_dict_list.append(sorted_cats_per_oxy_dict)

    global dict_completo
    dict_completo = deepcopy(sorted_data_recalc_Ox_dict)
    dict_completo.update(sorted_cats_per_oxy_dict)

    # sg.EasyPrint("fatto")

    return dict_completo


def sum_oxides(mineral_dict1):
    print("\nSUM starts here")
    #    global sum
    summa = 0

    for oxides_value in mineral_dict1.values():
        if type(oxides_value) == float:
            print("summa che?")
            summa = summa + oxides_value
            print("somma = ", summa)
        #            print("Progressive Sum = %f") % summa
        else:
            print("not a digitaaa?? ", mineral_dict1.values())

    print(("Total Sum = %f") % (summa))
    # global mineral_Ox_dict
    print("mineral_dict")
    print(mineral_dict1)
    #    mineral_dict1 = addValueDict("OxSum", sum, mineral_dict1, mineral_dict1)
    mineral_dict1.update({"OxSum": round(summa, 2)})
    print("UPDATED?")
    print(mineral_dict1)
    # global data_input_Ox_dict
    # oxides_dict = mineral_dict1
    global data_recalc_Ox_dict
    data_recalc_Ox_dict = mineral_dict1
    print("SUM  = " + str(mineral_dict1['OxSum']))
    print()
    return round(summa, 2)


def addValueDict(key, val, old_dict, new_dict):
    new_dict.update({key: val})
    return new_dict


def print_mineral_keys(mineral_dict):
    print("\nprint_mineral_keys")
    for mineral_keys in mineral_dict.keys():
        print(mineral_keys)
    return mineral_dict


def print_mineral_key_value(dicto):
    for k, v in dicto.items():
        print("{}".format(k), " = {}".format(v))


def mol_proportion(wt_oxides_dict):
    #   global mol_prop_sum
    #   global mol_proportion_dict
    mol_proportion_dict_tmp = OrderedDict()  ##<<<====
    # mol_proportion_dict_tmp = {}
    mol_prop_sum_tmp = 0
    print("mol_prop_sum_tmp = " + str(mol_prop_sum))
    for k, v in wt_oxides_dict.items():
        if k in molecular_weights:
            mol_prop = v / molecular_weights[k]
            #            global mol_proportion_dict
            mol_proportion_dict_tmp[k] = round(mol_prop, 3)
            #            mol_proportion_dict[k] = mol_prop
            # print "mol_prop: %f" % mol_prop
            # global mol_prop_sum
            mol_prop_sum_tmp = mol_prop_sum_tmp + mol_prop
            # print "mol_prop sum progress: %f" % mol_prop_sum
        else:
            print("\nnone....")
    print("mol_prop sum total: %f" % mol_prop_sum_tmp)
    print("\nmol_proportion_dict NO sum")
    print(mol_proportion_dict_tmp)
    # addValueDictEasy("mol_prop_sum", mol_prop_sum_tmp, mol_proportion_dict_tmp)
    return mol_proportion_dict_tmp, mol_prop_sum_tmp


def multipl_by_num_oxygens(mol_proportion_dict1):
    # mol_prop_by_oxygens_sum_tmp
    mol_by_oxygens_dict_tmp = OrderedDict()  # <<==
    #    mol_by_oxygens_dict_tmp = {}
    mol_prop_by_oxygens_sum_tmp = 0
    for k, v in mol_proportion_dict1.items():
        # if k in oxydes_by_formula:
        # k = str(k).replace("_mol","")
        if k in oxydes_by_formula:
            mol_by_oxygens = v * oxydes_by_formula[k]
            mol_by_oxygens_dict_tmp[k] = mol_by_oxygens
            mol_prop_by_oxygens_sum_tmp = mol_prop_by_oxygens_sum_tmp + mol_by_oxygens
            # print (mol_by_oxygens_dict_tmp[k])
            # print ("progression SUM = " + str(mol_prop_by_oxygens_sum_tmp))
    print("final SUM = " + str(mol_prop_by_oxygens_sum_tmp))
    print("\nmol_by_oxygens_dict")
    print_mineral_key_value(mol_by_oxygens_dict_tmp)
    return mol_by_oxygens_dict_tmp, mol_prop_by_oxygens_sum_tmp


def oxygen_proportion(mineral_input_dict, mol_by_oxygens_dict, mol_prop_sum):
    oxygens_prop_dict_tmp = OrderedDict()  # <<==
    # oxygens_prop_dict_tmp = {}
    # .wt_perc_oxides_dict = mineral_input_dict
    # print("mineral_input_dict: ", mineral_input_dict)
    # print(".wt_perc_oxides_dict ", .wt_perc_oxides_dict)
    print("searching for mineral: ", mineral_input_dict['mineral'])
    # print ("searching for mineral: " + mineral_input_dict['Mineral'].casefold())
    # labels = labels
    for k, v in mineral_oxigens.items():
        print("k.lowerAAA: ", k.lower())
    global oxygens
    for k, v in mineral_oxigens.items():
        if k.lower() == mineral_input_dict['mineral'.casefold()].lower():
            print(mineral_input_dict['mineral'.casefold()] + " found, it has %s oxygens" % str(v))

            oxygens = v

    # print ("OXYGENI = ",oxygeni)
    # print ("OXYGENS = ",oxygens)
    # print("len: ",len(oxygens_in_formula_list))
    ox_num = 0
    global oxygens_in_formula_dict
    print("oxygens_in_formula_dict", oxygens_in_formula_dict)
    # oxygens_in_formula_dict = []
    oxygens_in_formula_dict[ox_num] = oxygens
    # print("oxygens_in_formula_list type", oxygens_in_formula_list)
    oxygens_in_formula_list.append(oxygens)
    # print(".oxygens_in_formula_list type", oxygens_in_formula_list)
    # print("oxygens_in_formula_dict :", oxygens_in_formula_dict)
    ox_num += 1
    # print(".oxygens_in_formula_list type", oxygens_in_formula_list)

    for k, v in mol_by_oxygens_dict.items():
        print(k)
        #       if type(v) == float:
        oxygen_prop = v * (oxygens / mol_prop_sum)
        # print "=> v * (oxygens / sum_mol_prop_by_oxygens) = "+ str(v * (oxygens / mol_prop_sum))

        oxygens_prop_dict_tmp[k] = round(oxygen_prop, 3)
        # oxygens_prop_dict_tmp.update(oxygen_prop)

    print("Oxygens_prop_dict")
    print_mineral_key_value(oxygens_prop_dict_tmp)
    return oxygens_prop_dict_tmp

    print("oxygens_in_formula_dict[]")
    print_mineral_key_value(oxygens_in_formula_dict)
    return oxygens_in_formula_dict


def cations_apfu(oxygens_prop_dict_tmp):
    cats_per_oxy_dict_tmp = OrderedDict()  # <<==

    cats_per_oxy_sum_tmp = 0
    for k, v in oxygens_prop_dict_tmp.items():
        cation_per_oxy = round(v, 3) * round(cations_by_formula[k], 3)

        cats_per_oxy_dict_tmp[k] = round(cation_per_oxy, 3)
        cats_per_oxy_sum_tmp = round(cats_per_oxy_sum_tmp, 3) + cation_per_oxy

    print("Total SUM CATIONS = " + str(cats_per_oxy_sum_tmp))

    return cats_per_oxy_dict_tmp, cats_per_oxy_sum_tmp


def roundValuesInDict(dictio):
    for k, v in dictio.items():
        dictio[k] = round(v, 3)
    return dictio


def calcSiteDistribution(cats_per_oxy_dict):
    print("TO BE IMPLEMENTED")


def changeKeys(dictionary, old_key, new_key):
    print(dictionary)
    for k, v in dictionary.items():
        print("keys ", k)
        print("value ", v)

        new_key = "Fe2"
        old_key = "FeO"
        dictionary[new_key] = dictionary[old_key]
        del dictionary[old_key]
        print(dictionary)
        for k, v in dictionary.items():
            print("keys ", k)
            print("value ", v)
    return dictionary


def changeALLKeys(cats_dict):
    # module to change labels in cation dict because it now uses same as oxides
    print("cats_dict before...")
    print(cats_dict)

    for key in cats_dict.keys() & cation_labels.keys():
        print("changeALLKeys found: ", key)

        new_key = cation_labels[key]
        old_key = key
        cats_dict[new_key] = cats_dict[old_key]
        del cats_dict[old_key]
    print("cats_dict after...")
    print(cats_dict)
    return cats_dict


def extract_check_calc_specific_sites(recalc_data_oxides_cats_OX_list):
    print("\n\tFORMULA=> extract_check_calc_specific_sites(recalc_data_oxides_cats_OX__list)")

    print("\t\tDEVO SEPARARE PER LISTE DI MINERALE")
    print("\t\t\tPER OGNI LISTA DI MINERALE FARE I CALCOLI")
    print("\t\t\t\tRITORNARE LISTE DI LISTE DI MINERALI CON specific sites")
    print()

    a_args = []

    print(recalc_data_oxides_cats_OX_list)

    lista = []
    for each_analysis in recalc_data_oxides_cats_OX_list:
        lista.append(each_analysis)
    print("LISTA ", lista)

    for l in lista:
        print("l: ", l)
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

        print("\nmineral group = ", mine, 'is: ', value)
        global zzz
        zzz = 100.00001

        if mine == 'grt':
            # GARNET#
            for single in value:
                alm = single['Fe2'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                py = single['Mg'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                gr = single['Ca'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                sps = single['Mn'] / (single['Fe2'] + single['Mg'] + single['Ca'] + single['Mn'])
                XFe = single['Fe2'] / (single['Fe2'] + single['Mg'])
                XMg = single['Mg'] / (single['Fe2'] + single['Mg'])
                XCa = single['Ca'] / (single['Fe2'] + single['Mg'] + single['Ca'])
                '''
                Fe3+ = 2*X*(1-T/S)
                X=>oxigens in formula
                T=>ideal number of cations
                S=>observed cations
                '''
                if 'Fe3' in single:
                    print("good to know")
                    pass
                else:
                    print("CATIONI SUM GRT: ", single['SUMcat'])
                    Fe3 = 2 * 12 * (1 - 8 / single['SUMcat'])
                    single.update({'Fe3': round(Fe3, 3)})
                    pass
                single.update({'alm': round(alm, 3)})
                single.update({'py': round(py, 3)})
                single.update({'gr': round(gr, 3)})
                single.update({'sps': round(sps, 3)})
                single.update({'XFe': round(XFe, 3)})
                single.update({'XMg': round(XMg, 3)})

                print("every mineral analysis: ", single, "")
                TempK = 873  # 600 Celsius
                R = scipy.constants.R
                a = 0
                b = 0
                c = 0
                P_grt = (-8904.5+24.542*TempK+0.45*R*TempK*math.log(XCa/XFe)+0.15*TempK*a+0.15*c)/(1-0.15*b)/1000   ## Minerals 2019, 9(9), 540; https://doi.org/10.3390/min9090540
                single.update({'P_grt(kbar@600°C)-doi.org/10.3390/min9090540': round(P_grt, 3)})



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
