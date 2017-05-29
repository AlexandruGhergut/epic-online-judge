import subprocess
from celery import shared_task
from .models import Submission
from . import constants

@shared_task
def judge_submission(submission_id):
    submission = Submission.objects.filter(pk=submission_id).first()

    if submission:
        language = submission.get_language_display()
        if language == 'C++':
            source_file = submission.source_file
            source_path = source_file.storage.open(source_file.name)
            source_name = source_path.name

            solution_file = submission.problem.solution_source_file
            solution_path = solution_file.storage.open(solution_file.name).name

            testcase = submission.problem.testcase.input_data_file
            testcase_path = testcase.storage.open(testcase.name).name

            try:
                output = subprocess.check_output(['g++', source_name,
                                                  '-o', 'source'],
                                                 stderr=subprocess.STDOUT)
                if output:
                    print(output)

                output = subprocess.check_output(['g++', solution_path,
                                                 '-o', 'solution'],
                                                 stderr=subprocess.STDOUT)

                if output:
                    print(output)

                test_content = subprocess.check_output(['cat', testcase_path],
                                                       stderr=subprocess.STDOUT
                                                       )
                source_output = subprocess.check_output(['./source'],
                                                        input=test_content)
                solution_output = subprocess.check_output(['./solution'],
                                                          input=test_content)

                if source_output == solution_output:
                    submission.status = constants.Status.TESTS_PASSED
                else:
                    submission.status = constants.Status.WRONG_ANSWER
            except subprocess.CalledProcessError as e:
                output = e.output
                submission.status = constants.Status.ERROR
                print(output)
                
            submission.save()

            # subprocess.Popen(['echo', 'test', '|', 'tee', 'start'], shell=True)
            # subprocess.Popen(['cat', testcase_path, '|', './source',
            #                   '>', '/tmp/source_output'], shell=True)
            # subprocess.Popen(['cat', testcase_path, '|', './solution',
            #                   '>', '/tmp/source_output'], shell=True)
            # pipe = subprocess.Popen(['cat', '/tmp/source_output'], stdout=subprocess.PIPE)
            # result = pipe.communicate()[0]
            # print(result)
