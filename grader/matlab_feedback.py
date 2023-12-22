import json
from inspect import getmembers, isfunction
from test import Test

class Feedback:

    def __init__(self):

        print(f'[grader] Total points: {Test.get_total_points()}')

        self.results = {'tests': [], 
                   'score': 0.0, 
                   'succeeded': True, 
                   'gradable': True, 
                   'max_points': Test.get_total_points(), 
                   'output': '', 
                   'images': []}

        test_cases = Test()
        tests = [
                (func, getattr(test_cases, func))
                for func in dir(test_cases) 
                if callable(getattr(test_cases, func)) 
                and func.startswith("test_")
                ]
        self.tests = sorted(tests, key = lambda f: f[0])

    def run_tests(self):

        num_iters = Test.total_iters

        for test_name, f in self.tests:
            print(f'[grader] running test {test_name}')

            test_iter = num_iters
            if not f.__dict__.get('repeated', True):
                test_iter = 1

            scores = []
            all_feedback = ''

            for iter_num in range(1, 1 + test_iter):
                all_feedback += f'Feedback from test iteration {iter_num}\n'

                # run the test
                try:
                    score, feedback = f()
                except Exception as e:
                    score = 0
                    feedback = str(e)

                # cap score to between 0 and 1
                if score < 0:
                    score = 0
                if score > 1:
                    score = 1

                scores.append(score)
                all_feedback += feedback
                all_feedback += '\n'

            point = sum(scores) * f.__dict__['points']
            max_point = f.__dict__['points'] * test_iter
            self.results['score'] += point

            test_info = {'name': f.__dict__['name'], 
                         'max_points': max_point, 
                         'filename': test_name, 
                         'points': point, 
                         'files': [], 
                         'message': all_feedback}

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