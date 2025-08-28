from os import path
from matlab_helper import *
from matlab_feedback import *
import json
import datetime

def main():

    # get setup variables
    with open('/grade/data/data.json', 'r') as f:
        data = json.loads(f.read())
    
    vars_for_user = [var['name'] for var in data['params']['names_for_user']]
    print('variables for user: ' + str(vars_for_user))

    fname_student = data['params']['student_code_file'] if 'student_code_file' in data['params'] else 'user_code.m'
    _, extension = path.splitext(fname_student)
    if extension == '.ipynb':
        write_code("/grade/run/user_code.m", extract_ipynb_contents(fname_student))

    # add timestamp
    add_timestamp()
    
    # run setup code, store setup code variable, add lines to read setup code variable
    run_setup(*vars_for_user)
    prepare_code()

    f = Feedback()

    success, output = run_user()
    f.set_output(output)

    if not success:
        f.fail()
    else:
        f.run_tests()
    f.save_results()

# add timestamp to setup, user, ref to avoid function filename error
def add_timestamp():
    timestamp = f'timestamp = \"{str(datetime.datetime.now())}\";\n\n'

    user_code = read_code('/grade/run/user_code.m')
    if not user_code:
        user_code = timestamp
    else:
        user_code = timestamp + user_code
    write_code('/grade/run/user_code.m', user_code)

    ref_code = read_code('/grade/run/ref.m')
    if not ref_code:
        ref_code = timestamp
    else:
        ref_code = timestamp + ref_code
    write_code('/grade/run/ref.m', ref_code)


    setup_code = read_code('/grade/run/setup_code.m')
    if not setup_code:
        setup_code = timestamp
    else:
        setup_code = timestamp + setup_code
    write_code('/grade/run/setup_code.m', setup_code)

if __name__ == '__main__':
    main()