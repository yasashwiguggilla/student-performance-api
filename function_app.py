import azure.functions as func
import json
import os
from azure.storage.blob import BlobServiceClient


app = func.FunctionApp(
    http_auth_level=func.AuthLevel.ANONYMOUS
)


# Blob Storage connection
connection_string = os.environ["STUDENT_STORAGE_CONNECTION_STRING"]

blob_service_client = BlobServiceClient.from_connection_string(
    connection_string
)

# Container name
container_client = blob_service_client.get_container_client(
    "riskmanagementapiservice"
)

# Blob path inside the container
blob_client = container_client.get_blob_client(
    "students/students.json"
)


# Read students from Blob Storage
def read_students():
    data = blob_client.download_blob().readall()
    return json.loads(data)


# Write students to Blob Storage
def write_students(students):
    data = json.dumps(students, indent=2)

    blob_client.upload_blob(
        data,
        overwrite=True
    )


# --------------------------------------------------
# POST - Create a student
# --------------------------------------------------

@app.route(route="students", methods=["POST"])
def create_student(req: func.HttpRequest) -> func.HttpResponse:

    try:
        data = req.get_json()

        students = read_students()

        # Generate new ID
        if students:
            new_id = max(
                student["id"] for student in students
            ) + 1
        else:
            new_id = 1

        student = {
            "id": new_id,
            "name": data["name"],
            "age": data["age"],
            "marks": data["marks"],
            "attendance": data["attendance"]
        }

        students.append(student)

        # Save updated data to Blob
        write_students(students)

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


# --------------------------------------------------
# GET - Get all students
# --------------------------------------------------

@app.route(route="students", methods=["GET"])
def get_students(req: func.HttpRequest) -> func.HttpResponse:

    try:

        students = read_students()

        return func.HttpResponse(
            json.dumps({
                "students": students
            }),
            status_code=200,
            mimetype="application/json"
        )

    except Exception as e:

        return func.HttpResponse(
            json.dumps({
                "error": str(e)
            }),
            status_code=500,
            mimetype="application/json"
        )


# --------------------------------------------------
# GET - Get student by ID
# --------------------------------------------------

@app.route(route="students/{student_id}", methods=["GET"])
def get_student(req: func.HttpRequest) -> func.HttpResponse:

    try:

        student_id = int(
            req.route_params.get("student_id")
        )

        students = read_students()

        for student in students:

            if student["id"] == student_id:

                return func.HttpResponse(
                    json.dumps(student),
                    status_code=200,
                    mimetype="application/json"
                )

        return func.HttpResponse(
            json.dumps({
                "error": "Student not found"
            }),
            status_code=404,
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


# --------------------------------------------------
# PUT - Update student
# --------------------------------------------------

@app.route(route="students/{student_id}", methods=["PUT"])
def update_student(req: func.HttpRequest) -> func.HttpResponse:

    try:

        student_id = int(
            req.route_params.get("student_id")
        )

        students = read_students()

        data = req.get_json()

        for student in students:

            if student["id"] == student_id:

                student["name"] = data["name"]
                student["age"] = data["age"]
                student["marks"] = data["marks"]
                student["attendance"] = data["attendance"]

                # Save updated data to Blob
                write_students(students)

                return func.HttpResponse(
                    json.dumps({
                        "message": "Student updated successfully",
                        "student": student
                    }),
                    status_code=200,
                    mimetype="application/json"
                )

        return func.HttpResponse(
            json.dumps({
                "error": "Student not found"
            }),
            status_code=404,
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


# --------------------------------------------------
# DELETE - Delete student
# --------------------------------------------------

@app.route(route="students/{student_id}", methods=["DELETE"])
def delete_student(req: func.HttpRequest) -> func.HttpResponse:

    try:

        student_id = int(
            req.route_params.get("student_id")
        )

        students = read_students()

        for student in students:

            if student["id"] == student_id:

                students.remove(student)

                # Save updated data to Blob
                write_students(students)

                return func.HttpResponse(
                    json.dumps({
                        "message": "Student deleted successfully",
                        "student": student
                    }),
                    status_code=200,
                    mimetype="application/json"
                )

        return func.HttpResponse(
            json.dumps({
                "error": "Student not found"
            }),
            status_code=404,
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