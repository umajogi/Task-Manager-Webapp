

from flask import Flask, render_template, request, redirect
import json, os
from datetime import datetime

app = Flask(__name__)
DATA_FILE = 'data/tasks.json'

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

def save_tasks(tasks):
    with open(DATA_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        tasks = load_tasks()
        new_task = {
            "id": len(tasks) + 1,
            "name": request.form['name'],
            "priority": request.form['priority'],
            "due_date": request.form['due_date'],
            "completed": False
        }
        tasks.append(new_task)
        save_tasks(tasks)
        return redirect('/')
    return render_template('add_task.html')

@app.route('/complete/<int:task_id>')
def complete_task(task_id):
    tasks = load_tasks()  # Load the tasks from the file

    # Find the task by its ID and mark it as completed
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True  # Mark as completed
            break  # Stop once the task is found and updated

    save_tasks(tasks)  # Save the updated task list to the file
    return redirect('/')  # Redirect back to the home page


@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task["id"] != task_id]
    save_tasks(tasks)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
