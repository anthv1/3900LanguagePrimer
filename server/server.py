from flask import Flask, jsonify, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

groups = [
    {
        "id": 1,
        "groupName": "Group 1",
        "members": [1, 2, 3],
    },
    {
        "id": 2,
        "groupName": "Group 2",
        "members": [4, 5],
    },
]

students = [
    {"id": 1, "name": "Alice"},
    {"id": 2, "name": "Bob"},
    {"id": 3, "name": "Charlie"},
    {"id": 4, "name": "David"},
    {"id": 5, "name": "Eve"},
]

@app.route('/api/groups', methods=['GET'])
def get_groups():
    """
    Route to get all groups
    return: Array of group objects
    """
    return jsonify(groups), 200

@app.route('/api/students', methods=['GET'])
def get_students():
    """
    Route to get all students
    return: Array of student objects
    """
    return jsonify(students), 200

@app.route('/api/groups', methods=['POST'])
def create_group():
    """
    Route to add a new group
    param groupName: The name of the group (from request body)
    param members: Array of member names (from request body)
    return: The created group object
    """

    # Getting the request body (DO NOT MODIFY)
    group_data = request.json
    group_name = group_data.get("groupName")
    group_members = group_data.get("members")

    new_group_id = max([group["id"] for group in groups], default=0) + 1
    member_ids = []
    # TODO: EDGE - CASE, having duplicated student names when creating a group.
    for member in set(group_members):
        try:
            # if member existed
            existing_member = next(stu for stu in students if stu["name"] == member)
            member_ids.append(existing_member["id"])
        except:
            newStu_id = max([student["id"] for student in students], default=0) + 1
            students.append({"id": newStu_id, "name": member})
            member_ids.append(newStu_id)
            continue

    new_group = {
        "id": new_group_id,
        "groupName": group_name,
        "members": member_ids,
    }
    groups.append(new_group)
    return jsonify(new_group), 201

@app.route('/api/groups/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """
    Route to delete a group by ID
    param group_id: The ID of the group to delete
    return: Empty response with status code 204
    """
    for group in groups:
        if group["id"] == group_id:
            groups.remove(group)
            return '', 204  # Return 204 (do not modify this line)
        else:
            continue
    return jsonify({"error": "Group not found"}), 404

@app.route('/api/groups/<int:group_id>', methods=['GET'])
def get_group(group_id):
    """
    Route to get a group by ID (for fetching group members)
    param group_id: The ID of the group to retrieve
    return: The group object with member details
    """
    # create list
    studentList = []
    try:
        # get group from group ID
        target_group =next((group for group in groups if group["id"] == group_id))
        # get group name
        group_name = target_group["groupName"]
        member_list = target_group["members"]
        # for each member in members
        for member in member_list:
            # if member (ID) in students:
            try:
                # add student into list
                studentList.append(next(stu for stu in students if stu["id"] == member))
            except:
                print("student ID not found")
                continue
        return jsonify({
            "id": group_id,
            "groupName": group_name,
            "members": studentList,
        }), 200
    except:
        abort(404, "Group not found")

if __name__ == '__main__':
    app.run(port=3902, debug=True)
