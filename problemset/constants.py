class Status:
    ERROR = 0
    PENDING = 1
    TESTS_PASSED = 2
    WRONG_ANSWER = 3

    CHOICES = (
        (ERROR, 'Error'),
        (PENDING, 'Pending'),
        (TESTS_PASSED, 'Tests passed'),
        (WRONG_ANSWER, 'Wrong answer'),
    )


class Language:
    CPP = 0
    PYTHON = 1
    CHOICES = (
        (CPP, 'C++'),
        (PYTHON, 'Python')
    )
