import subprocess
import os

# --------------------------------------------------------
# helper functions not needed in tests
# --------------------------------------------------------


def extract_ipynb_contents(file_name):
    with open(file_name, "r") as f:
        from IPython.core.interactiveshell import InteractiveShell  # type: ignore
        from nbformat import read  # type: ignore

        """
        Extract all cells from a ipynb notebook that start with a given
        delimiter
        """

        nb = read(f, 4)
        shell = InteractiveShell.instance()
        content = ""
        for cell in nb.cells:
            if cell["cell_type"] == "code":
                code = shell.input_transformer_manager.transform_cell(cell.source)
                if code.strip().startswith("#grade"):
                    content += code
        return content


def run_user():
    """
    run user_code.m
    return error message if an error occurred
    return stdout outputs if no error occurred
    """
    process = subprocess.Popen(
        ["octave", "--silent", "user_code.m"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output, error = process.communicate()

    if error:
        # need to write to output
        feedback = error.decode("utf-8")
        return 0, feedback
    else:
        feedback = output.decode("utf-8")
        return 1, feedback


def read_code(file_name):
    try:
        with open(file_name, "r") as f:
            code = f.read()
            return code
    except FileNotFoundError:
        print(f"{file_name} can' be found")
        return ""


def write_code(file_name, code):
    with open(file_name, "w+") as f:
        f.write(code)


# get run setup code and store provided variables in setup_variable.mat
def run_setup(*inputs):
    print("[grader] running setup code")

    var_store_command = "\nsave -v7 /grade/run/setup_variable.mat"

    for var in inputs:
        var_store_command += " "
        var_store_command += var

    var_store_command += ";\n"

    setup_code = read_code("/grade/run/setup_code.m")
    if not setup_code:
        return
    setup_code += var_store_command
    write_code("/grade/run/setup_code.m", setup_code)

    process = subprocess.Popen(
        ["octave", "--silent", "/grade/run/setup_code.m"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    output, error = process.communicate()


# load setup variables to reference and student answer
def prepare_code():
    # if there are no setup variables, don't add lines to load variables
    if not os.path.isfile("/grade/run/setup_variable.mat"):
        return

    # prompt to read variable
    var_read_command = "load setup_variable.mat;\n"
    fnc_read_command = 'source("setup_code.m");\n'

    user_code = read_code("/grade/run/user_code.m")
    user_code = var_read_command + fnc_read_command + user_code
    write_code("/grade/run/user_code.m", user_code)

    ref_code = read_code("/grade/run/ref.m")
    ref_code = var_read_command + fnc_read_command + ref_code
    write_code("/grade/run/ref.m", ref_code)


def points(points):
    """
    Set the number of points that a test case should award.
    """

    def decorator(f):
        f.__dict__["points"] = points
        return f

    return decorator


def name(name):
    """
    Set the name of the test that will appear in results.
    """

    def decorator(f):
        f.__dict__["name"] = name
        return f

    return decorator


def not_repeated():
    """
    Set the test to be run only once
    """

    def decorator(f):
        f.__dict__["repeated"] = False
        return f

    return decorator
