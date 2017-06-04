from celery import shared_task
from core.tasks import process_source
from .models import Problem


@shared_task
def judge_problem_solution(problem_id):
    problem = Problem.objects.filter(pk=problem_id).first()

    solution_file = problem.solution_source_file
    solution_file = solution_file.storage.open(solution_file.name)
    solution_path = solution_file.name

    testcase = problem.testcase.input_data_file
    testcase = testcase.storage.open(testcase.name)
    testcase_path = testcase.name

    solution_language = problem.solution_language
    try:
        output = process_source(solution_path, 'source_output', testcase_path,
                                solution_language)
        problem.testcase.output = output
        problem.testcase.save()
    except Exception as e:
        print(str(e))
