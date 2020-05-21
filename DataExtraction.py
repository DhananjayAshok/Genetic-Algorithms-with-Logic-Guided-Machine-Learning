import os
import math
import pandas as pd
import numpy as np
from Equations import *



def extract_data(equation_id):
    """
    Depreciated: Made to load from text files
    Return dataframe and series with data and output targets

    Parameters
    ----------
    equation_id : string
        The ID of an equation in the dataset. Must be a valid one

    Returns
    -------
    pd.DataFrame, pd.Series
    """
    master_file = "FeynmanEquations.csv"
    data_root = "data"
    directory = pd.read_csv(master_file)
    for i, filename in enumerate(directory['Filename']):
        if filename != equation_id:
            pass
        else:
            no_vars = directory['nvariables'][i]
            lst = []
            target = []
            with open(os.path.join(data_root, filename), 'r') as f:
                for j, line in enumerate(f):
                    vals = [float(no) for no in line.strip().split(" ")]
                    lst.append(vals[:-1])
                    target.append(vals[-1])
                return pd.DataFrame(lst, columns =[f"X{j}" for j in range(no_vars)]), pd.Series(target)
    raise ValueError(f"Error: equation i.d {equation_id} not found in the list of equation of FeynmanEquations.csv")




def create_dataset(equation_id, no_samples=1000, input_range=(-100, 100), path=None, save=False, load=False, master_file="FeynmanEquations.csv"):
    """
    Return dataframe with data columns and target column

    Prerequisites:
        The Equations.py file must have a function to return the target given inputs of this equation - let us call this function f
        The equation_dict in Utility.py should have a key value pair key: equation_id, value: f

    Parameters
    ----------
    equation_id : string
        The ID of an equation in the dataset. Must be a valid one
    no_samples: int
        The number of samples you want to generate
    input_range: tuple(float, float)
        The minimum and maximum values of all input parameters
    save_path: string path
        The path to where you wish the save this dataframe
    save: boolean
        Saves file to save_path iff True
    load: boolean
        If true then looks for file in save_path and loads it preemptively if it is there
    master_file : str
            The path to the master file of equations. This csv file must at least contain the following columns - "Filename"(equation ids), "Formula"(string readable), "nvariables(int readable that matches number of variables of the equation on that line)"

    Returns
    -------
    pd.DataFrame
    """
    if load:
        if path is None:
            print("Please Provide Save path for saving and loading")
        elif equation_id + ".csv" in os.listdir(path):
            
            return pd.read_csv(os.path.join(path, equation_id+".csv"))
    else:
        print("CSV file not found in save_path, generating new dataset")

    directory = pd.read_csv(master_file)
    for i, filename in enumerate(directory['Filename']):
        if filename != equation_id:
            pass
        else:
            no_vars = directory['nvariables'][i]
            inputs = np.random.default_rng().uniform(input_range[0] ,input_range[1], (no_samples, no_vars))
            if equation_id not in equation_dict.keys():
                raise ValueError(f"Equation {equation_id} does not seem to be defined in equation_dict (of Equations.py)")
            target = np.reshape(equation_dict[equation_id](inputs), (-1, 1))
            df =  pd.DataFrame(np.append(inputs, target, axis=1), columns=[f"X{j}" for j in range(no_vars)] + ["target"])
            if save:
                if path is None:
                    print("Please Provide Save path for saving and loading")
                else:
                    df.to_csv(os.path.join(path, equation_id + ".csv"))
            return df
    raise ValueError(f"Error: equation i.d {equation_id} not found in the list of equation of FeynmanEquations.csv")
