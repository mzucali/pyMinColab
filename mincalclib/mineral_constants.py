# http://www.lenntech.com/calculators/molecular/molecular-weight-calculator.htm
#

#phonebook = {'Andrew Parson':8806336, \
#'Emily Everett':6784346, 'Peter Power':7658344, \
#'Lewis Lame':1122345}

molecular_weights = {'SiO2' : 60.08,
                     'Al2O3' : 101.96,
                     'FeO' : 71.85,
                     'Na2O' : 61.98,
                     'MgO' : 40.32,
                     'Fe2O3' : 159.69,
                     'K2O' : 94.20,
                     'TiO2' : 79.87,
                     'MnO' : 70.94,
                     'Mn2O3' : 157.87,
                     'CaO' : 56.08,
                     'Cr2O3' : 151.99,
                     'ZnO' : 81.39,
                     'P2O5' : 141.94,
                     'SrO' : 103.62,
                     'NiO' : 74.7094,
                     'B2O3': 69.6202,
                     'V2O3' : 149.8812
                     }


oxydes_by_formula = {'SiO2' : 2,
                     'Al2O3': 3 ,
                     'FeO' : 1,
                     'Na2O' : 1,
                     'MgO' : 1,
                     'Fe2O3' : 3,
                     'K2O' : 1,
                     'TiO2' : 2,
                     'MnO' : 1,
                     'Mn2O3' : 3,
                     'CaO' : 1,
                     'Cr2O3' : 3,
                     'ZnO' : 1,
                     'P2O5' : 5,
                     'SrO' : 1,
                     'NiO' : 1,
                     'B2O3':3,
                    'V2O3' : 3
                     }

cations_by_formula = {'SiO2' : 0.5,
                     'Al2O3': 0.666667 ,
                     'FeO' : 1.0,
                     'Na2O' : 2.0,
                     'MgO' : 1.0,
                     'Fe2O3' : 0.666667,
                     'K2O' : 2,
                     'TiO2' : 0.5,
                     'MnO' : 1.0,
                     'Mn2O3' : 0.666667,
                     'CaO' : 1.0,
                     'Cr2O3' : 0.666667,
                     'ZnO' : 1.0,
                     'P2O5' : 0.4,
                     'SrO' : 1.0,
                     'NiO' : 1.0,
                     'B2O3': 0.666667,
                    'V2O3' : 0.666667
                    }

#!/usr/bin/env python
#
#  chemweight.py
#
#import re
mass = {
  "H":	1.00794,
  "He":	4.002602,
  "Li":	6.941,
  "Be":	9.012182,
  "B":	10.811,
  "C":	12.011,
  "N":	14.00674,
  "O":	15.9994,
  "F":	18.9984032,
  "Ne":	20.1797,
  "Na":	22.989768,
  "Mg":	24.3050,
  "Al":	26.981539,
  "Si":	28.0855,
  "P":	30.973762,
  "S":	32.066,
  "Cl":	35.4527,
  "Ar":	39.948,
  "K":	39.0983,
  "Ca":	40.078,
  "Sc":	44.955910,
  "Ti":	47.88,
  "V":	50.9415,
  "Cr":	51.9961,
  "Mn":	54.93805,
  "Fe":	55.847,
  "Co":	58.93320,
  "Ni":	58.6934,
  "Cu":	63.546,
  "Zn":	65.39,
  "Ga":	69.723,
  "Ge":	72.61,
  "As":	74.92159,
  "Se":	78.96,
  "Br":	79.904,
  "Kr":	83.80,
  "Rb":	85.4678,
  "Sr":	87.62,
  "Y":	88.90585,
  "Zr":	91.224,
  "Nb":	92.90638,
  "Mo":	95.94,
  "Tc":	98,
  "Ru":	101.07,
  "Rh":	102.90550,
  "Pd":	106.42,
  "Ag":	107.8682,
  "Cd":	112.411,
  "In":	114.82,
  "Sn":	118.710,
  "Sb":	121.757,
  "Te":	127.60,
  "I":	126.90447,
  "Xe":	131.29,
  "Cs":	132.90543,
  "Ba":	137.327,
  "La":	138.9055,
  "Ce":	140.115,
  "Pr":	140.90765,
  "Nd":	144.24,
  "Pm":	145,
  "Sm":	150.36,
  "Eu":	151.965,
  "Gd":	157.25,
  "Tb":	158.92534,
  "Dy":	162.50,
  "Ho":	164.93032,
  "Er":	167.26,
  "Tm":	168.93421,
  "Yb":	173.04,
  "Lu":	174.967,
  "Hf":	178.49,
  "Ta":	180.9479,
  "W":	183.85,
  "Re":	186.207,
  "Os":	190.2,
  "Ir":	192.22,
  "Pt":	195.08,
  "Au":	196.96654,
  "Hg":	200.59,
  "Tl":	204.3833,
  "Pb":	207.2,
  "Bi":	208.98037,
  "Po":	209,
  "At":	210,
  "Rn":	222,
  "Fr":	223,
  "Ra":	226.0254,
  "Ac":	227,
  "Th":	232.0381,
  "Pa":	213.0359,
  "U":	238.0289,
  "Np":	237.0482,
  "Pu":	244,
  "Am":	243,
  "Cm":	247,
  "Bk":	247,
  "Cf":	251,
  "Es":	252,
  "Fm":	257,
  "Md":	258,
  "No":	259,
  "Lr":	260,
  "Rf":	261,
  "Db":	262,
  "Sg":	263,
  "Bh":	262,
  "Hs":	265,
  "Mt":	266,
}

mineral_oxigens = {

    "amph": 23,
    "amph23":23,
    "amph23.5":23.5,

##GARNET

#garnet 2
    "grt": 12,


#pyroxene 3
    "px" : 6,

#allumosilicates 4

    "als" : 20,
#biotite 5
    "bt": 22,
    #"bt22": 22,
    #"bt11": 11,


#white mica 18
    "wm": 11,
    "wm11": 11,
    "wm22": 22,

#chlorite 6
    "chl": 28,
#cordierite 7
    "crd" : 18,

#chloritoid 8
    "ctd" : 12,
#calcite/carb/dol 9
    "cc":14,
#clinohumite 10
    "chum":18,

#corindone 11
    "cor": 3,

#epidote 12
    "ep":25,
    
#feldspar&plagioclase 13

    "fsp":8,
#ilmenite 14
    "ilm":3,
    
# rutile 15
    "rt": 2, 
#SPINEL 16
    "sp": 4,
    
#PUMPELLYITE 17
    "pump" : 14,
    
    
    "op" : 14,
#olivine 19
    "ol" : 4,
#titanite 20 
    "ttn": 5,
#melilite 21
    "mel": 14,
    
#zircon 22
    'zrc': 16,
#turmaline
    'tur': 31,

#UNKNOWN 
    "xx" : 10,

}

mineral_labels = {
#amphibole
    'am' : 'amph', "AMP": 'amph',"amp": 'amph',
    "Amp" : 'amph', "a" : 'amph', "amph": 'amph',
    "amphibole": 'amph',
    "gln": 'amph',
    "act": 'amph',
    "Oam" : 'amph',
    "OAm" : 'amph',
    "Gln" : 'amph',
    "g" : 'amph',
    "gl" : 'amph',
    "AM" : 'amph',
    "gedrite" : 'amph',
    "ged" : 'amph',
    
#amph=['AMP' , 'Amp' , 'amp' , 'am' , 'a' , 'amph' , 'Amph' , 'Oam' , 'OAm','gln','g','glau', 'amphibole','act']
    
#garnet
    "grt": 'grt',
    "GT": 'grt',
    "gr":'grt',
    "g":'grt',
    'gt':'grt',
    'GRT':'grt',
#garnet=['grt','Gt','gt','g','gr','GRT']

#pyroxene
    "px" : 'px',
    "PX" : 'px',
    "Px" : 'px',
    "cpx" : 'px',
    "CPX" : 'px',
    "CPx" : 'px',
    "pyroxene" : 'px',
    "jd" : 'px',
    "JD" : 'px',
    "omp" : 'px',
    "om" : 'px',
    "omph" : 'px',
    "acm" : 'px',
    "aeg" : 'px',
    "agt" : 'px',
    "augite" : 'px',
    "acmite" : 'px',
    'OPX' : 'px' ,
    'opx' : 'px',
    'Opx' : 'px' ,
    'OPx' : 'px',
#px=['px' , 'PX' , 'Px','CPX' , 'Cpx' , 'CPx', 'cpx', 'Jd' , 'jd' , 'JD' , 'OPX' ,'opx' ,'Opx' , 'OPx']

#allumosilicates
    "ky" : 'als',
    "and" : 'als',
    "sill" : 'als',
    "sil" : 'als',
    "als" : 'als',
    "al2sio5": 'als',
    "And": 'als',
    "Sil" : 'als',
    "Sill": 'als',
    "AS" : 'als',
    "as" : 'als',
    
#al2sio5=['al2sio5', 'ky', 'sill', 'and','And','AND','Sill' , 'Sil','Ky' , 'k','als']

#biotite
    "bt": 'bt',
    "bt11": 'bt',
    "bio": 'bt',
    "bi" : 'bt',
    "BT" : 'bt',
    "b" : 'bt',
    "BI" : 'bt',
#bio=['BI', 'BT', 'Bt','Bio','b','bt']


#white mica
    "WM" : 'wm',
    "Wm" : 'wm',
    "mica": 'wm',
    "phn" : 'wm',
    "phen": 'wm',
    "pg" : 'wm',
    
#mica=['WM','Wm', 'wm', 'w','mica'] 

#chlorite
    "chl": 'chl',
    "ch": 'chl',
    "CHL": 'chl',
    "chlorite":'chl',
    "CH": 'chl',
    "Chl" : 'chl',
#chl=['chl', 'CHL','CH', 'Chl', 'chlorite']

#cordierite
    "cd" : 'crd',
    "crd" : 'crd',
    "CD" : 'crd',

#chloritoid
    "ctd" : 'ctd',
    "cld" : 'ctd',
    "ct" : 'ctd',
    "Ctd" : 'ctd',
    "Cld" : 'ctd',

#ctd= ['Ctd', 'Cld', 'ctd', 'cld']

#staurolite
    "st": 'st',
    "St": 'st',
    "staurolite": 'st',
    "Stau" : 'st',
    "stau" : 'st',
    "ST" : 'st',
    
#stau=['St', 'st', 'staurolite', 'Stau','stau']

#calcite/carb/dol
    "cc":'cc',
    "cal":'cc',
    "calcite":'cc',
    "CC" : 'cc',
    "DOL": 'cc',
    "Dol": 'cc',
    "dol" : 'cc',
    "Ank" : 'cc',
    "ank": 'cc',

#cc=['CC', 'DOL','Do', 'dol' , 'd' , 'Cc' , 'cal' , 'Cal' , 'Ank' ,'ank']

#clinohumite
    "chum":'chum',

#corindone
    "cor": 'cor',
    "co":'cor',

#epidote
    "ep":'ep',
    "zo":'ep',
    "czo":'ep',
    "fe-ep":'ep',
    "epidote":'ep',
    "e" : 'ep',
    "Zo" : 'ep',
    "aln":'aln',
    "all":'aln',
    "allanite" : 'aln',
    "Aln" : 'aln',
    "EP" : 'ep',
    
#ep=['aln' , 'all' , 'allanite' , 'Aln','epidote','ep','e', 'cz' , 'czo']

#feldspar&plagioclase
    "ab":'fsp',
    "Ab" : 'fsp',
    "an":'fsp',
    "An" : 'fsp',
    "pl":'fsp',
    "Pl" : 'fsp',
    "fd":'fsp',
    "Fds" : 'fsp',
    "fds":'fsp',
    "feld":'fsp',
    "kfs":'fsp',
    "feldspar":'fsp',
    "albite":'fsp',
    "plagioclase":'fsp',
    "fp" : 'fsp',
    
#fds=['Fd', 'Kfs', 'Ab', 'An','ab','an','kfs','pl', 'Pl']

#ilmenite
    "il":'ilm',
    "ilm":'ilm',

#rutile
    "Rt": 'rt',
    "rt": 'rt',
    "Ru": 'rt',
    "rutile": 'rt',

#SPINEL
    "sp": 'sp',
    "spinel":'sp',
    "Sp":'sp',
    "spl":'sp',

#opaque
    "op": 'op',
    "opq":'op',
    "opaque": 'op',    

#monazite
    'mnz':'mnz',
    'MNZ': 'mnz',
    'Mnz': 'mnz',
    'monazite': 'mnz',

#zircon

    'Zrc' : 'zrc', 
    'zrc': 'zrc',
    'zrn':'zrc',
    'zr': 'zrc',
    'zircon': 'zrc',
    'ZC':'zrc',
    "zc" : 'zrc',
    

##PUMPELLYITE
    "pmp" : 'pump',
    "pump": 'pump',

## titanite/sphene
    "SE" : 'ttn',
    "ttn": 'ttn',
    "titanite": 'ttn',
    
#olivine
    "ol" : 'ol',
    "OL" : 'ol',
    "fo": 'ol',
    "fa": 'ol',
    
#melilite
    "ME": 'mel',
    "me": 'mel',

##tourmaline
    "tourmaline":'tur',
    "tur":'tur',
    "turm":'tur',
    "tormalina":'tur',
    "torm" : 'tur',
#unknown
    "xx" : 'xx',

}


#garnet=['grt','Gt','gt','g','gr','GRT']
#px=['px' , 'PX' , 'Px','CPX' , 'Cpx' , 'CPx', 'cpx', 'Jd' , 'jd' , 'JD' , 'OPX' ,'opx' ,'Opx' , 'OPx']
#ep=['aln' , 'all' , 'allanite' , 'Aln','epidote','ep','e', 'cz' , 'czo']
#amph=['AMP' , 'Amp' , 'amp' , 'am' , 'a' , 'amph' , 'Amph' , 'Oam' , 'OAm','gln','g','glau', 'amphibole','act']

#bio=['BI', 'BT', 'Bt','Bio','b','bt']
#mica=['WM','Wm', 'wm', 'w','mica']  

#al2sio5=['al2sio5', 'ky', 'sill', 'and','And','AND','Sill' , 'Sil','Ky' , 'k','als']
#stau=['St', 'st', 'staurolite', 'Stau','stau']
# chl=['chl', 'CHL','CH', 'Chl', 'chlorite']
# ctd= ['Ctd', 'Cld', 'ctd', 'cld']
#fds=['Fd', 'Kfs', 'Ab', 'An','ab','an','kfs','pl', 'Pl']

# mnz=['mnz','MNZ','Mnz','monazite']
# zrc=['Zrc', 'zrc','zrn','zr','zircon']
#cc=['CC', 'DOL','Do', 'dol' , 'd' , 'Cc' , 'cal' , 'Cal' , 'Ank' ,'ank']
#opaque=['op', 'opaq','ossido']
#spinel=['spinel','sp','Sp']
#ilm=['ilm','ilmenite']
#rt=['Rt','rt','ru','rutile']



cation_labels={'FeO':'Fe2',
               'Fe2O3':'Fe3',
               'MgO':'Mg',
               'SiO2':'Si',
               'Al2O3':'Al', 
               'TiO2':'Ti',
               'Na2O':'Na',
               'CaO':'Ca',
               'K2O': 'K',
               'MnO': 'Mn',
               'Th2O3':'Th',
               'PbO':'Pb',
               'UO2':'U',
               'Cr2O3':'Cr',
               'ZnO':'Zn',
               'NiO':'Ni',
               'P2O5':'P',
               'La2O3':'La',
               'Y2O3':'Y',
               'Ce2O3':'Ce',
               'Pr2O3':'Pr',
               'As2O5':'As',
               'Dy2O5':'Dy',
               'Gd2O3':'Gd'}


cations_order = ['Si', 'Ti', 'Al','AlVI','AlIV','Fe3','Fe2','Mn','Mg','Ca','Na','K',
                'Th','Pb','U','Cr','Zn','Ni','P','La','Y','Ce','Pr','As', 'Dy','Gd','SUMcat']



oxides_order = ['Sample','mineral','SiO2', 'TiO2', 'Al2O3','Fe2O3','FeO','MnO','MgO','CaO','Na2O','K2O',
                'Th2O3','PbO','UO2','Cr2O3','ZnO','NiO','P2O5','La2O3','Y2O3','Ce2O3','Pr2O3','As2O5', 'Dy2O5','Gd2O3','OxSum', 'OX'] 





