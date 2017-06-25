import subprocess
import os
from celery import shared_task
from .models import Submission
from . import constants


@shared_task
def dispatch_submission(submission_id):
    submission = Submission.objects.filter(pk=submission_id).first()
    command = ['timeout', '-t', '20', 'docker-compose', 'run',
               '--service-ports',
               '-e', 'SUBMISSION_ID=' + str(submission_id),
               '--rm', 'worker']
    run_failed = False
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT)
        if output == 'ok':
            submission.Status.TIME_LIMIT_EXCEEDED
    except subprocess.CalledProcessError as e:
        run_failed = True
        if e.returncode == 124:
            submission.status = constants.Status.TIME_LIMIT_EXCEEDED
        else:
            submission.status = constants.Status.ERROR
        print(str(e))
    except Exception as e:
        run_failed = True
        print(str(e))
        submission.status = constants.Status.ERROR
    finally:
        if run_failed is True:
            submission.save()


def judge_submission():
    print(os.environ)
    submission_id = int(os.environ.get('SUBMISSION_ID', '-1'))
    submission = Submission.objects.filter(pk=submission_id).first()
    print('Submission id is: ' + str(submission_id))

    try:
        output = extract_output(submission)
        if output[0] == output[1]:
            submission.status = constants.Status.TESTS_PASSED
        else:
            submission.status = constants.Status.WRONG_ANSWER
    except subprocess.CalledProcessError as e:
        output = e.output
        submission.status = constants.Status.ERROR
        print(output)
    except Exception as e:
        submission.status = constants.Status.ERROR
        print(str(e))

    submission.save()


def extract_output(submission):
    result = ['Empty1', 'Empty2']

    if submission:
        source_file = submission.source_file
        source_file = source_file.storage.open(source_file.name)
        source_path = source_file.name

        testcase = submission.problem.testcase.input_data_file
        testcase = testcase.storage.open(testcase.name)
        testcase_path = testcase.name

        submission_language = submission.language

        result[0] = process_source(source_path, 'source_output',
                                   testcase_path, submission_language).rstrip()

        result[1] = submission.problem.testcase.output.rstrip()

        submission.source_output = result[0]
        submission.save()

        # free resources
        source_file.close()
        testcase.close()

    return result


def process_source(source_path, source_output, testcase_path, source_language):
    processing_script_path = 'core/scripts/'

    if source_language == constants.Language.CPP:
        processing_script_path += 'process_cpp.sh'
    elif source_language == constants.Language.PYTHON:
        processing_script_path += 'process_python.sh'

    args = [processing_script_path, source_path, source_output,
            testcase_path]
    output = subprocess.check_output(args, stderr=subprocess.STDOUT)
    if output:
        return output.decode('utf-8')

    output = subprocess.check_output(['cat', source_output],
                                     stderr=subprocess.STDOUT)

    return output.decode('utf-8')
