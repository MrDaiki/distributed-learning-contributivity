# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:49:54 2019

Implement contributivity measurements

@author: @bowni
"""

from __future__ import print_function

import numpy as np
from itertools import combinations

from scipy.special import softmax

import fl_train_eval

import shapley_value.shapley as sv


# Contributivity measures functions

# Generalization of Shapley Value computation (WIP)

def compute_SV(node_list):
    
    print('\n### Launching computation of Shapley Value of all nodes')
    
    # Initialize list of all players (nodes) indexes
    nodes_count = len(node_list)
    nodes_idx = np.arange(nodes_count)
    print('All players (nodes) indexes: ', nodes_idx)
    
    # Define all possible coalitions of players
    coalitions = [list(j) for i in range(len(nodes_idx)) for j in combinations(nodes_idx, i+1)]
    print('All possible coalitions of players (nodes): ', coalitions)
    
    # For each coalition, obtain value of characteristic function...
    # ... i.e.: train and evaluate model on nodes part of the given coalition
    characteristic_function = []
    fl_train_score = fl_train_eval.fl_train_score
    
    for coalition in coalitions:
        coalition_nodes = list(node_list[i] for i in coalition)
        print('\nComputing characteristic function on coalition ', coalition)
        characteristic_function.append(fl_train_score(coalition_nodes)[1])
    print('\nValue of characteristic function for all coalitions: ', characteristic_function)
    
    # Compute Shapley Value for each node
    # We are using this python implementation: https://github.com/susobhang70/shapley_value
    # It requires coalitions to be ordered - see README of https://github.com/susobhang70/shapley_value
    list_shapley_value = sv.main(nodes_count, characteristic_function)
    
    # Return SV of each node
    return list_shapley_value


# Compute independent performance scores of models trained independently on each node
    
def compute_independent_scores(node_list, target_score):
    
    # Initialize a list of performance scores
    performance_scores = []
    
    # Train models independently on each node and append perf. score to list of perf. scores
    for node in node_list:
        performance_scores.append(fl_train_eval.single_train_score(node)[1])
        
    # Compute 'regularized' values of performance scores so that they are additive and their sum amount to the target performance score
    additive_scores = softmax(performance_scores) * target_score
    additive_scores = additive_scores.tolist()
    
    # Return both raw performance scores and the regularized values
    return [performance_scores, additive_scores]