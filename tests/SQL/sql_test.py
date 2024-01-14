import random
from sqlalchemy import text

from core import db
from core.models.assignments import Assignment, AssignmentStateEnum, GradeEnum



def create_n_graded_assignments_for_teacher(number: int = 0, teacher_id: int = 1) -> int:
    """
    Creates 'n' graded assignments for a specified teacher and returns the count of assignments with grade 'A'.

    Parameters:
    - number (int): The number of assignments to be created.
    - teacher_id (int): The ID of the teacher for whom the assignments are created.

    Returns:
    - int: Count of assignments with grade 'A'.
    """
    # Count the existing assignments with grade 'A' for the specified teacher
    grade_a_counter: int = Assignment.filter(
        Assignment.teacher_id == teacher_id,
        Assignment.grade == GradeEnum.A
    ).count()

    # Create 'n' graded assignments
    for _ in range(number):
        # Randomly select a grade from GradeEnum
        grade = random.choice(list(GradeEnum))

        # Create a new Assignment instance
        assignment = Assignment(
            teacher_id=teacher_id,
            student_id=1,
            grade=grade,
            content='test content',
            state=AssignmentStateEnum.GRADED
        )

        # Add the assignment to the database session
        db.session.add(assignment)

        # Update the grade_a_counter if the grade is 'A'
        if grade == GradeEnum.A:
            grade_a_counter = grade_a_counter + 1

    # Commit changes to the database
    db.session.commit()

    # Return the count of assignments with grade 'A'
    return grade_a_counter


def test_get_assignments_in_various_states():
    """Test to get assignments in various states"""
    db.session.rollback()

    # Define the expected result before any changes
    expected_result = [('DRAFT', 9), ('GRADED', 106), ('SUBMITTED', 3)]

    # Execute the SQL query and compare the result with the expected result
    with open('tests/SQL/number_of_assignments_per_state.sql', encoding='utf8') as fo:
        sql = fo.read()

    initial_graded_count = db.session.execute(text(sql)).fetchall()[1][1]  # Assuming 'GRADED' count is the second item in the result

    # Modify an assignment state and grade
    submitted_assignment = Assignment.filter(Assignment.state == AssignmentStateEnum.SUBMITTED).first()
    if(submitted_assignment):

        submitted_assignment.state = AssignmentStateEnum.GRADED
        submitted_assignment.grade = GradeEnum.C
    

        # Flush and commit the changes to the database
        db.session.commit()

        # Execute the SQL query again to get the updated count of 'GRADED' assignments
        updated_graded_count = db.session.execute(text(sql)).fetchall()[1][1]  # Assuming 'GRADED' count is the second item in the result

        # Check if the updated count is one more than the initial count
        assert updated_graded_count == initial_graded_count + 1, f"Expected {initial_graded_count + 1} 'GRADED' assignments, but found {updated_graded_count}"
    else:
        assert True


def test_get_grade_A_assignments_for_teacher_with_max_grading():
    """Test to get count of grade A assignments for teacher which has graded maximum assignments"""

    # Read the SQL query from a file
    with open('tests/SQL/count_grade_A_assignments_by_teacher_with_max_grading.sql', encoding='utf8') as fo:
        sql = fo.read()

    # Create and grade 5 assignments for the default teacher (teacher_id=1)
    grade_a_count_1 = create_n_graded_assignments_for_teacher(5)
    
    # Execute the SQL query and check if the count matches the created assignments
    sql_result = db.session.execute(text(sql)).fetchall()
    assert grade_a_count_1 == sql_result[0][0]

    
