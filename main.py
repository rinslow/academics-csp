from constraint import *
import itertools

s23c = 0
s24a = 1
s24b = 2
s24c = 3
s25a = 4
s25b = 5
s25c = 6
semesters = [s23c, s24a, s24b, s24c, s25a, s25b, s25c]

semester_names = ['2023c', '2024a', '2024b', '2024c', '2025a', '2025b', '2025c']

algorithms = "algorithms"
logic = "logic"
os = "os"
programming_languages = "programming-languages"
theory_of_computation = "theory-of-computation"
linear_algebra_2 = "linear-algebra-2"
biological_computation = "biological-computation"
networking = "networking"
ai_seminar = "ai-seminar"
biological_computation_seminar = "biological-computation-seminar"
courses = [algorithms, logic, os, programming_languages, theory_of_computation, linear_algebra_2,
           biological_computation, networking, ai_seminar, biological_computation_seminar]
courses_amount = len(courses)

difficulties = {
    algorithms: 3,
    logic: 1,
    os: 2,
    programming_languages: 2,
    theory_of_computation: 4,
    linear_algebra_2: 5,
    biological_computation: 2,
    networking: 1,
    ai_seminar: 3,
    biological_computation_seminar: 3
}

# Map each course to the semesters in which it can be taken
course_semesters = {
    algorithms: [s24a, s24b, s25a, s25b],
    logic: [s24a, s24b, s25a, s25b],
    os: [s24a, s24b, s25a, s25b],
    programming_languages: [s24b, s25b],
    theory_of_computation: [s24b],
    linear_algebra_2: [s23c, s24a, s24b, s24c, s25a, s25b, s25c],
    biological_computation: [s24a, s25a],
    networking: [s23c, s24b, s24c, s25b, s25c],
    ai_seminar: [s23c, s24a, s24b, s24c, s25a, s25b, s25c],
    biological_computation_seminar: [s23c, s24c, s25c],
}

# -------------COEFFICEINTS -------------
maximum_difficulty_per_semester = 7
last_semester_to_study = s24c
# -------------COEFFICEINTS -------------


# Map each semester to the courses that can be taken in that semester
semester_courses = {semester: [] for semester in semesters}
for course, course_semesters in course_semesters.items():
    for semester in course_semesters:
        semester_courses[semester].append(course)

# Generate all possible combinations of courses for each semester
semester_domains = {}
amount_of_combinations_to_examine = 0  # Counter
for semester, courses in semester_courses.items():
    semester_domains[semester] = []
    semester_domains[semester].append([])  # The possibility of not studying at a semester
    amount_of_combinations_to_examine += 1

    for r in range(1, len(courses) + 1):
        for combination in itertools.combinations(courses, r):
            amount_of_combinations_to_examine += 1
            if sum(difficulties[course] for course in combination) <= maximum_difficulty_per_semester:
                semester_domains[semester].append(combination)

problem = Problem()
for semester, domain in semester_domains.items():
    problem.addVariable(semester, domain)


# -------------CONSTRAINTS -------------

def course_can_only_be_learned_once(courses_in_a, courses_in_b):
    for course_a in courses_in_a:
        if course_a in courses_in_b:
            return False

    return True


def all_courses_must_be_learned(*_semesters):
    sum_of_courses_learned = sum(map(len, _semesters))
    return sum_of_courses_learned == courses_amount


def dependency_between_courses(sem_before, sem_after):
    return not (biological_computation in sem_after and biological_computation_seminar in sem_before)


# Courses can only be learned once
for semester1 in semesters:
    for semester2 in semesters:
        if semester1 == semester2: continue
        problem.addConstraint(course_can_only_be_learned_once, [semester1, semester2])

# All courses must be learned
for course in courses:
    problem.addConstraint(all_courses_must_be_learned, semesters)

# Some courses have dependencies in order
for i in range(len(semesters)):
    for j in range(i, len(semesters)):
        semester_before = semesters[i]
        semester_after = semesters[j]
        problem.addConstraint(dependency_between_courses, [semester_before, semester_after])

# Study every semester until last semester
for i in range(last_semester_to_study + 1):
    semester = semesters[i]
    problem.addConstraint(lambda s: 0 < len(s), [semester])

# Don't study anymore after last semester
for i in range(last_semester_to_study + 1, len(semesters)):
    semester = semesters[i]
    problem.addConstraint(lambda s: 0 == len(s), [semester])

solutions = problem.getSolutions()
print(
    f"Found {len(solutions)} solutions for study plans with {maximum_difficulty_per_semester} maximum difficulty per semester and learning up to {semester_names[last_semester_to_study]}")


def sorted_solution(s):
    return dict((semester_names[k], s[k]) for k in sorted(s.keys()))


print(sorted_solution(solutions[0]))
print(sorted_solution(solutions[1]))
pass
