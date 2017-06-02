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
            source_path = source_file.storage.open(source_file.name).name

            solution_file = submission.problem.solution_source_file
            solution_path = solution_file.storage.open(solution_file.name).name

            testcase = submission.problem.testcase.input_data_file
            testcase_path = testcase.storage.open(testcase.name).name

            args = ['core/scripts/process_cpp.sh', source_path, 'source_output',
                    solution_path, 'solution_output', testcase_path]

            try:
                output = subprocess.check_output(['pwd'], stderr=subprocess.STDOUT)
                print(output)
                output = subprocess.check_output(args,
                                                 stderr=subprocess.STDOUT)
                if output:
                    print(output)

                source_output =\
                    subprocess.check_output(['cat', 'source_output'],
                                            stderr=subprocess.STDOUT)
                solution_output =\
                    subprocess.check_output(['cat', 'solution_output'],
                                            stderr=subprocess.STDOUT)

                if source_output == solution_output:
                    submission.status = constants.Status.TESTS_PASSED
                else:
                    submission.status = constants.Status.WRONG_ANSWER
            except subprocess.CalledProcessError as e:
                output = e.output
                submission.status = constants.Status.ERROR
                print(output)

            #process_cpp(submission, source_path, solution_path, testcase_path)
            submission.save()


def process_cpp(submission, source_path, solution_path, testcase_path):
    try:
        output = subprocess.check_output(['g++', source_path,
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
