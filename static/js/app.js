document.addEventListener('DOMContentLoaded', function() {
    const refreshBtn = document.getElementById('refresh-btn');
    if (refreshBtn) {
        refreshBtn.addEventListener('click', function() {
            loadTasks();
        });
    }
});

function loadTasks() {
    fetch('/api/tasks')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(tasks => {
            renderTasks(tasks);
        })
        .catch(error => {
            console.error('Error loading tasks:', error);
            showAlert('Error loading tasks. Please try again.', 'danger');
        });
}

function renderTasks(tasks) {
    const container = document.getElementById('tasks-container');
    
    if (tasks.length === 0) {
        container.innerHTML = `
            <div class="alert alert-info">
                <h4>No tasks found</h4>
                <p>You don't have any tasks yet. <a href="/add">Add your first task!</a></p>
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
                <h2 class="mb-0">Your Tasks</h2>
                <span class="badge bg-secondary">${tasks.length} tasks</span>
            </div>
            <ul class="list-group list-group-flush">
    `;
    
    tasks.forEach(task => {
        const createdDate = new Date(task.created_at).toLocaleString();
        const updatedDate = task.updated_at !== task.created_at ? 
            ` | Updated: ${new Date(task.updated_at).toLocaleString()}` : '';
        
        html += `
            <li class="list-group-item ${task.completed ? 'completed-task' : ''}">
                <div class="d-flex justify-content-between align-items-start">
                    <div>
                        <h4>${task.title}</h4>
                        ${task.description ? `<p>${task.description}</p>` : ''}
                        <small class="text-muted">
                            Created: ${createdDate}${updatedDate}
                        </small>
                    </div>
                    <div class="d-flex gap-2">
                        <a href="/toggle/${task.id}" 
                           class="btn btn-sm ${task.completed ? 'btn-warning' : 'btn-success'}">
                            ${task.completed ? 'Reopen' : 'Complete'}
                        </a>
                        <a href="/edit/${task.id}" class="btn btn-warning btn-sm">Edit</a>
                        <form method="POST" action="/delete/${task.id}" 
                              onsubmit="return confirm('Are you sure you want to delete this task?');">
                            <button type="submit" class="btn btn-danger btn-sm">Delete</button>
                        </form>
                    </div>
                </div>
            </li>
        `;
    });
    
    html += `
            </ul>
        </div>
    `;
    
    container.innerHTML = html;
    
    // Re-attach event listener to the new refresh button
    const newRefreshBtn = document.getElementById('refresh-btn');
    if (newRefreshBtn) {
        newRefreshBtn.addEventListener('click', function() {
            loadTasks();
        });
    }
}

function showAlert(message, type) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}
