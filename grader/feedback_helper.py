import subprocess
import scipy.io
import numpy as np

from matlab_helper import *

# --------------------------------------------------------
# helper functions for tests
# --------------------------------------------------------

def check_scalar(name, st, ref, atol = 1e-8, rtol = 1e-5):

    if st is None:
        return 0, f'{name} is None or not defined'
    
    if not isinstance(st, (complex, float, int, np.number)):
        try:
            if not st.is_number:
                return 0, f'{name} is not a number'
        except AttributeError:
            return 0, f'{name} is not a number'
        
    if rtol is not None and abs(ref - st) < abs(ref) * rtol:
        return 1, f'{name} looks good'
    if atol is not None and abs(ref - st) < atol:
        return 1, f'{name} looks good'
    return 0, f'{name} is inaccurate'

def check_numpy_array_features(name, st, ref):

    if st is None:
        return 0, f'{name} is None or not defined'
    
    if not isinstance(st, np.ndarray):
        return 0, f'{name} is not a numpy array'

    if isinstance(st, np.matrix):
        return 0, f'{st} is a numpy matrix. Do not use those. \nbit.ly/array-vs-matrix'
        
    if ref.shape != st.shape:
        return 0, f'{name} does not have correct shape--got: {st.shape}, expected: {ref.shape}'
    
    if ref.dtype.kind != st.dtype.kind:
        return 0, f'{name} does not have correct data type--got: {st.dtype}, expected: {ref.dtype}'
    
    return 1, None

def check_numpy_array_allclose(name, st, ref, atol = 1e-8, rtol = 1e-5):
    
    feature_res, feature_feedback = check_numpy_array_features(name, st, ref)
    if not feature_res:
        return 0, feature_feedback
    
    if np.allclose(ref, st, rtol=rtol, atol=atol):
        return 1, f'{name} looks good'
    else:
        return 0, f'{name} is inaccurate'

def get_user_var(variable_name):
    
    user_code = read_code('/grade/run/user_code.m')
    
    # add command for storing variable
    var_store_command = f'\nsave -v7 /grade/run/check_variable.mat {variable_name};'
    user_code += var_store_command

    write_code('/grade/run/user_code_cp.m', user_code)

    # run script
    process = subprocess.Popen(['octave', '--silent', '/grade/run/user_code_cp.m'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        raise Exception(error.decode("utf-8"))
    if output:
        print(output.decode("utf-8"))
    
    variable = scipy.io.loadmat('/grade/run/check_variable.mat', simplify_cells = True)[variable_name]
    return variable

def call_user_function(function_name, *inputs):

    user_code = read_code('/grade/run/user_code.m')

    # add variable definition for function inputs
    var_def_command = ''
    input_vars = []
    for i in range(len(inputs)):
        var_def_command += f'input_{i}={inputs[i]};'
        input_vars.append(f'input_{i}')
    var_def_command += '\n'
    user_code = var_def_command + user_code

    # run variable using given inputs
    inputs = ', '.join(input_vars)
    fnc_run_command = f'\nfunction_output = {function_name}({inputs});'
    user_code += fnc_run_command

    # add command for storing variable
    var_store_command = '\nsave -v7 /grade/run/check_variable.mat function_output;'
    user_code += var_store_command

    write_code('/grade/run/user_code_cp.m', user_code)

    # run script
    process = subprocess.Popen(['octave', '--silent', '/grade/run/user_code_cp.m'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        raise Exception(error.decode("utf-8"))
    if output:
        print(output.decode("utf-8"))
    
    variable = scipy.io.loadmat('/grade/run/check_variable.mat', simplify_cells = True)['function_output']
    return variable

def get_ref_var(variable_name):

    ref_code = read_code('/grade/run/ref.m')
    
    # add command for storing variable
    var_store_command = f'\nsave -v7 /grade/run/ref_variable.mat {variable_name};'
    ref_code += var_store_command

    write_code('/grade/run/ref_cp.m', ref_code)

    # run script
    process = subprocess.Popen(['octave', '--silent', '/grade/run/ref_cp.m'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()

    if error:
        raise Exception(error.decode("utf-8"))
    if output:
        print(output.decode("utf-8"))
    
    variable = scipy.io.loadmat('/grade/run/ref_variable.mat', simplify_cells = True)[variable_name]
    return variable

def call_ref_function(function_name, *inputs):

    ref_code = read_code('/grade/run/ref.m')

    # add variable definition for function inputs
    var_def_command = ''
    input_vars = []
    for i in range(len(inputs)):
        var_def_command += f'input_{i}={inputs[i]};'
        input_vars.append(f'input_{i}')
    var_def_command += '\n'
    ref_code = var_def_command + ref_code

    # run variable using given inputs
    inputs = ', '.join(input_vars)
    fnc_run_command = f'\nfunction_output = {function_name}({inputs});'
    ref_code += fnc_run_command

    # add command for storing variable
    var_store_command = '\nsave -v7 /grade/run/ref_variable.mat function_output;'
    ref_code += var_store_command

    write_code('/grade/run/ref_cp.m', ref_code)

    # run script
    process = subprocess.Popen(['octave', '--silent', '/grade/run/ref_cp.m'], 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    
    if error:
        raise Exception(error.decode("utf-8"))
    if output:
        print(output.decode("utf-8"))
    
    variable = scipy.io.loadmat('/grade/run/ref_variable.mat', simplify_cells = True)['function_output']
    return variable