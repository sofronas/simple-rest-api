from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data (in-memory)
# to get data from database you need to create a function to retrieve them
# Step 1: connect to database
# Step 2: read data
# Step 3: close database connection
# Step 4: organize data structure
tasks = [
    {'id': 1, 'title': 'Task 1', 'description': 'Description 1', 'done': False},
    {'id': 2, 'title': 'Task 2', 'description': 'Description 2', 'done': False}
]


# GET all tasks
# via GET http method get all tasks from database/memory
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({'tasks': tasks})


# GET single task by id
# get specific task searched by task id
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if task:
        return jsonify({'task': task})
    else:
        return jsonify({'message': 'Task not found'}), 404


# POST a new task
# function to insert a new task to memory list
# if you have a database you need a different function to utilize it
@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.json or 'title' not in request.json:
        return jsonify({'message': 'Title is required'}), 400
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


# PUT (update) an existing task
# this function requires the task id needed to be updated and the task object to be changed
# if you have a database you need a different function to utilize it
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    if 'title' in request.json:
        task['title'] = request.json['title']
    if 'description' in request.json:
        task['description'] = request.json['description']
    if 'done' in request.json:
        task['done'] = request.json['done']
    return jsonify({'task': task})


# DELETE a task by id
# this function delete the specified task from memory
# if you have a database you need a different function to utilize it
# prefer to pass the specified task to a different database table instead of deleting
# e.x. Table deletedTasks
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = next((task for task in tasks if task['id'] == task_id), None)
    if not task:
        return jsonify({'message': 'Task not found'}), 404
    tasks.remove(task)
    return jsonify({'message': 'Task deleted'})


# host the flask app up to the server
if __name__ == '__main__':
    app.run(debug=True)  # debug purposes only
