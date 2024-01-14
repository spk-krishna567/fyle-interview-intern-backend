from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment
from core.models.teachers import Teacher
from .schema import AssignmentSchema,TeacherSchema, AssignmentGradeSchema


principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    principal_assignments=Assignment.getsubmitted_and_gradedassignments()
    principal_assignments_dump = AssignmentSchema().dump(principal_assignments, many=True)
    return APIResponse.respond(data=principal_assignments_dump)

@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    all_teachers=Teacher.get_all_teachers()
    all_teachers_dump=TeacherSchema().dump(all_teachers,many=True)
    return APIResponse.respond(data=all_teachers_dump)

@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def update_assignment_grade(p,incoming_payload):
    """Grade or re-grade an assignment"""
    grade_assignment_payload=AssignmentGradeSchema().load(incoming_payload)
    updated_assignment=Assignment.update_grade(_id=grade_assignment_payload.id,grade=grade_assignment_payload.grade)
    db.session.commit()
    updated_assignment_dump=AssignmentSchema().dump(updated_assignment)
    return APIResponse.respond(data=updated_assignment_dump)