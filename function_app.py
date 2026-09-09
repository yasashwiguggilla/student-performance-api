import azure.functions as func
import json


app = func.FunctionApp(
    http_auth_level=func.AuthLevel.ANONYMOUS
)


# In-memory storage
students = {}


# POST - Create a student
@app.route(route="students", methods=["POST"])
def create_student(req: func.HttpRequest) -> func.HttpResponse:

    try:
        data = req.get_json()

        student_id = len(students) + 1

        student = {
            "id": student_id,
            "name": data["name"],
            "age": data["age"],
            "marks": data["marks"],
            "attendance": data["attendance"]
        }

        students[student_id] = student

        return func.HttpResponse(
            json.dumps({
                "message": "Student created successfully",
                "student": student
            }),
            status_code=201,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                "error": str(e)
            }),
            status_code=400,
            mimetype="application/json"
        )


# GET - Get all students
@app.route(route="students", methods=["GET"])
def get_students(req: func.HttpRequest) -> func.HttpResponse:

    return func.HttpResponse(
        json.dumps({
            "students": list(students.values())
        }),
        status_code=200,
        mimetype="application/json"
    )


# GET - Get student by ID
@app.route(route="students/{student_id}", methods=["GET"])
def get_student(req: func.HttpRequest) -> func.HttpResponse:

    student_id = int(req.route_params.get("student_id"))

    if student_id not in students:
        return func.HttpResponse(
            json.dumps({
                "error": "Student not found"
            }),
            status_code=404,
            mimetype="application/json"
        )

    return func.HttpResponse(
        json.dumps(students[student_id]),
        status_code=200,
        mimetype="application/json"
    )


# PUT - Update student
@app.route(route="students/{student_id}", methods=["PUT"])
def update_student(req: func.HttpRequest) -> func.HttpResponse:

    student_id = int(req.route_params.get("student_id"))

    if student_id not in students:
        return func.HttpResponse(
            json.dumps({
                "error": "Student not found"
            }),
            status_code=404,
            mimetype="application/json"
        )

    try:
        data = req.get_json()

        updated_student = {
            "id": student_id,
            "name": data["name"],
            "age": data["age"],
            "marks": data["marks"],
            "attendance": data["attendance"]
        }

        students[student_id] = updated_student

        return func.HttpResponse(
            json.dumps({
                "message": "Student updated successfully",
                "student": updated_student
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({
                "error": str(e)
            }),
            status_code=400,
            mimetype="application/json"
        )


# DELETE - Delete student
@app.route(route="students/{student_id}", methods=["DELETE"])
def delete_student(req: func.HttpRequest) -> func.HttpResponse:

    student_id = int(req.route_params.get("student_id"))

    if student_id not in students:
        return func.HttpResponse(
            json.dumps({
                "error": "Student not found"
            }),
            status_code=404,
            mimetype="application/json"
        )

    deleted_student = students.pop(student_id)

    return func.HttpResponse(
        json.dumps({
            "message": "Student deleted successfully",
            "student": deleted_student
        }),
        status_code=200,
        mimetype="application/json"
    )