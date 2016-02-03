# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 17:39:16 2016
Code to read in current weightings for each attribute and apply them to differently-normalised and thresholded versions of the network output weights.
Calculation of the weightings is based on parsing characters and assigning values:
For example, for usefulness, u=1, m=0, n=-1
For LUCAS top level landcover classes, the frequency of occurrence is used. - e.g., aa&g&c 
For 'why important' it's simply a direct 1/0 match on the labels 'bi', 'b', 'n', 'hf' and 'hl'
@author: bastinl
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Read in specified csv files of data (2)
sceneFile = 'C:/github/CitizenSensor/data/postprocessing_experiments/Paris_and_3k/3k_set_scene.csv'
semanticFile = 'C:/github/CitizenSensor/data/postprocessing_experiments/Paris_and_3k/3k_set_semantic.csv'
ParisSceneFile = 'C:/github/CitizenSensor/data/postprocessing_experiments/Paris_and_3k/paris_set_scene.csv'
ParisSemanticFile = 'C:/github/CitizenSensor/data/postprocessing_experiments/Paris_and_3k/paris_set_semantic.csv'
sceneWeightsFile = 'C:/github/CitizenSensor/data/Places_scene_attributes.csv'
semanticWeightsFile = 'C:/github/CitizenSensor/data/Places_semantic_attributes.csv'
# Read in specified csv files of data (2)
sceneData = pd.read_csv(sceneFile)
semanticData = pd.read_csv(semanticFile)
ParisSceneData = pd.read_csv(ParisSceneFile)
ParisSemanticData = pd.read_csv(ParisSemanticFile)
# Read in corresponding csv files of expert-specified weights (2)
sceneWeights = pd.read_csv(sceneWeightsFile)
semanticWeightsData = pd.read_csv(semanticWeightsFile)
# - online, these steps can be skipped and we go straight from memory

explorePDF = PdfPages('data_exploration.pdf')
# Generate a histogram for each of the attributes and view... for exploration
sceneAtts = sceneData.columns
semanticAtts = semanticData.columns
# Could well use these again later
gridSize = 4,4
for col in sceneAtts:
    if col != 'Filename':
        fig = plt.figure();
        plt.suptitle(col, fontsize=14, fontweight='bold')
        plt.subplot2grid(gridSize, (0,0), rowspan=2, colspan=4)
        sceneData[col].plot(kind='hist')
        
        plt.subplot2grid(gridSize, (2,0), rowspan=2, colspan=4)
        ParisSceneData[col].plot(kind='hist')
        explorePDF.savefig(fig)
        plt.close()
        
for col2 in semanticAtts:
    if col2 != 'Filename':
        fig = plt.figure();
        plt.suptitle(col2, fontsize=14, fontweight='bold')
        plt.subplot2grid(gridSize, (0,0), rowspan=2, colspan=4)
        semanticData[col2].plot(kind='hist')
        
        plt.subplot2grid(gridSize, (2,0), rowspan=2, colspan=4)
        ParisSemanticData[col2].plot(kind='hist')
        explorePDF.savefig(fig)
        plt.close()
        
explorePDF.close()

# Generate a data frame where every value is scaled linearly between the max and min
linear3kscene = sceneData
linear3kscene.drop(linear3kscene.columns('Filename'))
linear3kscene.apply(lambda x: (x-np.mean(x)) / (np.max(x) - np.min(x)))
# TODO - make this much more concise - currently just experimenting.

# Generate a data frame where values below 0 are ignored and the remainder are scaled linearly between min and max

# Generate a data frame where z-values are calculated across the full range of the weights for each attribute

# 
#

#
#
#
#
#
#

#
#
#
#
#
#

#
#
#
#
#
#

#
#
#
#
#
#