from flask import Flask, jsonify, request
from models.task import Task
app = Flask(__name__)


tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():

  global task_id_control

  data = request.get_json()
  new_task = Task(id=task_id_control, title=data.get("title"), description=data.get("description", ""))

  task_id_control += 1
  tasks.append(new_task)
  print(tasks)

  return jsonify({"message": "Nova tarefa criada com sucesso 🎉"})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    
    task_list = [task.to_dict() for task in tasks]

    output = {
      "tasks": task_list,
      "total_tasks": len(task_list)
    }
    return jsonify(output)

@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for t in tasks:
      if t.id == id:
         return jsonify(t.to_dict())
    return jsonify({"message": "Não foi possível encontar a atividade 😵‍💫"}), 404

@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    task = None
    for t in tasks:
      if t.id == id:
         task = t

    if task == None:
      return jsonify({"message": "Não foi possível encontar a atividade 😵‍💫"}), 404

    data = request.get_json()
    task.title = data.get("title")
    task.description = data.get("description")
    task.completed = data.get("completed")

    return jsonify({"message": "Tarefa atualizada com sucesso 😎"})

# Modo recomendado apenas para o desenvolvimento local.
if __name__ == "__main__":
    app.run(debug=True)
