import subprocess
from celery import shared_task
from .models import Submission
from . import constants


@shared_task
def judge_submission(submission_id):
    submission = Submission.objects.filter(pk=submission_id).first()

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
        source_path = source_file.storage.open(source_file.name).name

        solution_file = submission.problem.solution_source_file
        solution_path = solution_file.storage.open(solution_file.name).name

        testcase = submission.problem.testcase.input_data_file
        testcase_path = testcase.storage.open(testcase.name).name

        submission_language = submission.language
        solution_language = submission.problem.solution_language

        result[0] = process_source(source_path, 'source_output',
                                   testcase_path, submission_language)
        result[1] = process_source(solution_path, 'solution_output',
                                   testcase_path, solution_language)

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
    return output
