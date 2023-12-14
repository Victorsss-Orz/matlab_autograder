import json
from inspect import getmembers, isfunction
import test

class Feedback:

    def __init__(self):

        self.results = {'tests': [], 
                   'score': 0.0, 
                   'succeeded': True, 
                   'gradable': True, 
                   'max_points': 0.0, 
                   'output': '', 
                   'images': []}

        tests = getmembers(test, isfunction)
        tests = [t for t in tests if t[0] != 'points' and t[0] != 'name']
        self.tests = tests

    def run_tests(self):

        for test_name, f in self.tests:
            print(f'[grader] running test {test_name}')
            try:
                score, feedback = f()
            except Exception as e:
                score = 0
                feedback = str(e)
            if score < 0:
                score = 0
            if score > 1:
                score = 1

            point = 1. * score * f.__dict__['points']
            max_point = f.__dict__['points']
            self.results['score'] += point
            self.results['max_points'] += max_point

            test_info = {'name': f.__dict__['name'], 
                         'max_points': max_point, 
                         'filename': test_name, 
                         'points': point, 
                         'files': [], 
                         'message': feedback}

            self.results['tests'].append(test_info)

    def save_results(self):
        self.results['score'] /= self.results['max_points']
        with open('/grade/results/results.json', 'w+') as f:
            f.write(json.dumps(self.results, indent = 4))
    
    def set_output(self, output):
        self.results['output'] = output

    def fail(self):
        self.results['score'] = 0.
        self.results['max_points'] = 1.
        self.results['succeeded'] = False