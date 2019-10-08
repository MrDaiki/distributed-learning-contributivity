# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 14:49:54 2019

Implement contributivity measurements

@author: @bowni
"""

from __future__ import print_function

import numpy as np
from itertools import combinations

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
    fl_train = fl_train_eval.fl_train
    
    for coalition in coalitions:
        coalition_nodes = list(node_list[i] for i in coalition)
        print('\nComputing characteristic function on coalition ', coalition)
        characteristic_function.append(fl_train(coalition_nodes)[1])
    print('\nValue of characteristic function for all coalitions: ', characteristic_function)
    
    # Compute Shapley Value for each node
    # We are using this python implementation: https://github.com/susobhang70/shapley_value
    list_shapley_value = sv.main(nodes_count, characteristic_function)
    
    # Return SV of each node
    return list_shapley_value


# =============================================================================
# # Naive Shapley Value for 3 partners
# def compute_SV_3partners(node_index, node_list):
#     
#     # Check that there are 3 nodes
#     assert(len(node_list) == 3)
#     
#     # By definition node_A is the node which index has been passed as argument
#     node_A = node_list[node_index]
#     # Other definitions of nodes and list of nodes
#     all_nodes = node_list
#     other_nodes = list(all_nodes)
#     other_nodes.remove(node_A)
#     node_B = other_nodes[0]
#     node_C = other_nodes[1]
#     nodes_A_B = [node_A, node_B]
#     nodes_A_C = [node_A, node_C]
#     
#     # Compute characteristic function
#     print('\n### Starting computation of SV for node n°' + str(node_index))
#     fl_train = fl_train_eval.fl_train
#     single_train = fl_train_eval.single_train
#     print('\n #### FL training on all nodes:')
#     cf_all_nodes = fl_train(all_nodes)[1]
#     print('\n #### FL training on other nodes (all but node n°' + str(node_index) + ' in scenario defined):')
#     cf_other_nodes = fl_train(other_nodes)[1]
#     print('\n #### FL training on nodes A and B (A being n°' + str(node_index) + ' in scenario defined):')
#     cf_A_B = fl_train(nodes_A_B)[1]
#     print('\n #### FL training on nodes A and C (A being n°' + str(node_index) + ' in scenario defined):')
#     cf_A_C = fl_train(nodes_A_C)[1]
#     print('\n #### Training on node B (A being n°' + str(node_index) + ' in scenario defined):')
#     cf_B = single_train(node_B)[1]
#     print('\n #### Training on node C (A being n°' + str(node_index) + ' in scenario defined):')
#     cf_C = single_train(node_C)[1]
#     
#     # Compute Shapley Value
#     shapley_value = 1/6 * (   2 * (cf_all_nodes - cf_other_nodes)
#                             + 2 * (cf_A_B - cf_B)
#                             + 2 * (cf_A_C - cf_C) )
#     
#     return shapley_value
# 
# 
# # Naive Shapley Value for 4 partners
# def compute_SV_4partners(node_index, node_list):
#     
#     # Check that there are 3 nodes
#     assert(len(node_list) == 4)
#     
#     # By definition node_A is the node passed as argument
#     node_A = node_list[node_index]
#     # Other definitions of nodes and list of nodes
#     all_nodes = node_list
#     other_nodes = all_nodes.remove(node_A)
#     node_B = other_nodes[0]
#     node_C = other_nodes[1]
#     node_D = other_nodes[2]
#     nodes_A_B = [node_A, node_B]
#     nodes_A_C = [node_A, node_C]
#     nodes_A_D = [node_A, node_D]
#     nodes_B_C = [node_B, node_C]
#     nodes_B_D = [node_B, node_D]
#     nodes_C_D = [node_C, node_D]
#     nodes_A_B_C = [node_A, node_B, node_C]
#     nodes_A_B_D = [node_A, node_B, node_C]
#     nodes_A_C_D = [node_A, node_C, node_D]
#     
#     # Compute characteristic function
#     fl_train = fl_train_eval.fl_train
#     single_train = fl_train_eval.single_train
#     cf_all_nodes = fl_train(all_nodes)[1]
#     cf_other_nodes = fl_train(other_nodes)[1]
#     cf_A_B = fl_train(nodes_A_B)[1]
#     cf_A_C = fl_train(nodes_A_C)[1]
#     cf_A_D = fl_train(nodes_A_D)[1]
#     cf_B = single_train(node_B)[1]
#     cf_C = single_train(node_C)[1]
#     cf_D = single_train(node_D)[1]
#     cf_A_B_C = fl_train(nodes_A_B_C)[1]
#     cf_A_B_D = fl_train(nodes_A_B_D)[1]
#     cf_A_C_D = fl_train(nodes_A_C_D)[1]
#     cf_B_C = fl_train(nodes_B_C)[1]
#     cf_B_D = fl_train(nodes_B_D)[1]
#     cf_C_D = fl_train(nodes_C_D)[1]
#     
#     # Compute Shapley Value
#     shapley_value = 1/24 * (  6 * (cf_all_nodes - cf_other_nodes)
#                             + 2 * (cf_A_B_C - cf_B_C)
#                             + 2 * (cf_A_B_D - cf_B_D)
#                             + 2 * (cf_A_C_D - cf_C_D)
#                             + 2 * (cf_A_B - cf_B)
#                             + 2 * (cf_A_C - cf_C)
#                             + 2 * (cf_A_D - cf_D) )
#     
#     return shapley_value
# 
# =============================================================================
