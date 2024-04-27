#!/usr/bin/env python

# Modules
import numpy as np

# Functions
def calculate(lst: list) -> dict:
  '''Calculates basic statistical values based on a list of nine numbers, that are split in three groups.

  :param lst: list that contains nine numbers.
  :return: dictionary with mean, variance, standard deviation, maximum, minimum, and sum of each group an all numbers.''' 
  
    if len(lst) != 9:
        raise ValueError("List must contain nine numbers.")

    arr = np.array(lst) 
    arr.shape = (3, len(lst)//3)

    dct = {
    'mean': ['NaN', 'NaN', 'NaN'],
    'variance': ['NaN', 'NaN', 'NaN'],
    'standard deviation': ['NaN', 'NaN', 'NaN'],
    'max': ['NaN', 'NaN', 'NaN'],
    'min': ['NaN', 'NaN', 'NaN'],
    'sum': ['NaN', 'NaN', 'NaN']
    }

    axis1 = 0
    axis2 = 1
    flattened = 2

    dct['mean'][axis2] = [ arr[ i ].mean() for i in range( arr.shape[0] ) ]
    dct['mean'][axis1] = [ arr[:, i].mean() for i in range( arr.shape[0] ) ]
    dct['mean'][flattened] = arr.mean()

    dct['variance'][axis2] = [ arr[ i ].var() for i in range( arr.shape[0] ) ]
    dct['variance'][axis1] = [ arr[:, i].var() for i in range( arr.shape[0] ) ]
    dct['variance'][flattened] = arr.var()

    dct['standard deviation'][axis2] = [ arr[ i ].std() for i in range( arr.shape[0] ) ]
    dct['standard deviation'][axis1] = [ arr[:, i].std() for i in range( arr.shape[0] ) ]
    dct['standard deviation'][flattened] = arr.std()

    dct['max'][axis2] = [ arr[ i ].max() for i in range( arr.shape[0] ) ]
    dct['max'][axis1] = [ arr[:, i].max() for i in range( arr.shape[0] ) ]
    dct['max'][flattened] = arr.max()

    dct['min'][axis2] = [ arr[ i ].min() for i in range( arr.shape[0] ) ]
    dct['min'][axis1] = [ arr[:, i].min() for i in range( arr.shape[0] ) ]
    dct['min'][flattened] = arr.min()

    dct['sum'][axis2] = [ arr[ i ].sum() for i in range( arr.shape[0] ) ]
    dct['sum'][axis1] = [ arr[:, i].sum() for i in range( arr.shape[0] ) ]
    dct['sum'][flattened] = arr.sum()


    return dct
