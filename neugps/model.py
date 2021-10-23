# Module that includes the classification models used by the application.
#
# Author: Fernando García Gutiérrez
# Email: fegarc05@ucm.es
#
import os
from .tree import Tree, Level

PATH_TO_DATA = os.path.join('.', 'neugps', 'data')

DIAGNOSTIC_COLUMN = 'Diagnostic'

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%% Alzheimer's disease vs Healthy control decision tree %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
AD_HC_TREE_DATA = os.path.join(PATH_TO_DATA, 'ADvsHC.parquet')
ad_hc_level0a = Level('FCSRT (lt)', 8.64)
ad_hc_level0b = Level('ROCF (type 3 copy)', 0.64)
ad_hc_level1a = Level('ACE-III (attention)', 17.48, None, ad_hc_level0a)
ad_hc_level1b = Level('ACE-III (fluency)', 7.81, None, ad_hc_level0b)
ad_hc_level2a = Level('ROCF (30min)', 7.43, ad_hc_level1a, ad_hc_level1b)
ad_hc_level3 = Level('FCSRT (lt)', 11.27, ad_hc_level2a, None)
AD_HC_TREE = Tree(data=AD_HC_TREE_DATA, initial_level=ad_hc_level3, diagnosis_col=DIAGNOSTIC_COLUMN)

# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%% Frontotemporal dementia vs Healthy control decision tree %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
FTD_HC_TREE_DATA = os.path.join(PATH_TO_DATA, 'bvFTDvsHC.parquet')
ftd_hc_level0a = Level('ACE-III (fluency)', 5.54)
ftd_hc_level0b = Level('ACE-III (fluency)', 10.10)
ftd_hc_level1a = Level('VOSP (object decision)', 10.5, None, ftd_hc_level0a)
ftd_hc_level1b = Level('VOSP (object decision)', 7.63, ftd_hc_level0b, None)
ftd_hc_level2 = Level('ACE-III (fluency)', 8.55, ftd_hc_level1a, ftd_hc_level1b)
FTD_HC_TREE = Tree(data=FTD_HC_TREE_DATA, initial_level=ftd_hc_level2, diagnosis_col=DIAGNOSTIC_COLUMN)


# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%% Alzheimer's disease + bvFTD vs Healthy control decision tree %%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
# %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% #
NEU_HC_TREE_DATA = os.path.join(PATH_TO_DATA, 'NEUvsHC.parquet')
neu_level0a = Level('TMT (a)', 10.56)
neu_level1a = Level('TMT (a)', 3.17, None, neu_level0a)
neu_level0b = Level('ROCF (type 4 3min)', 0.5)
neu_level0c = Level('ROCF (30min)', 9.02)
neu_level1b = Level('FCSRT (lt)', 2.98, neu_level0b, neu_level0c)
neu_level0d = Level('ACE-III (fluency)', 11.44)
neu_level0e = Level('Education years', 5.54)
neu_level1c = Level('ROCF (30min)', 6.50, neu_level0d, neu_level0e)
neu_level2 = Level('FCSRT (lt)', 6.95, neu_level1b, neu_level1c)
neu_level3 = Level('ACE-III (fluency)', 7.98, neu_level1a, neu_level2)
NEU_HC_TREE = Tree(data=NEU_HC_TREE_DATA, initial_level=neu_level3, diagnosis_col=DIAGNOSTIC_COLUMN)


MODELS = {
    'AD vs HC': AD_HC_TREE,
    'bvFTD vs HC': FTD_HC_TREE,
    'bvFTD/AD vs HC': NEU_HC_TREE
}
