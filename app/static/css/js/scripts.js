document.getElementById('todo-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const task = document.getElementById('task').value;
    const date = document.getElementById('date').value;
    const priority = document.getElementById('priority').value;

    const todoData = {
        task: task,
        date: date,
        priority: priority
    };

    // Send a POST request to add the new todo
    fetch('/todos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(todoData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Todo added:', data);
        fetchTasks();  // Fetch updated list of todos after adding the new one
    })
    .catch(error => console.error('Error:', error));
});
