document.getElementById('editTaskModal').addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;

    const form = document.getElementById('editTaskForm');
    form.action = button.getAttribute('data-action');

    const get = (attr) => (button.getAttribute(attr) || '').trim();

    form.elements['title'].value = get('data-title');
    form.elements['priority'].value = get('data-priority');
    form.elements['status'].value = get('data-status');

    const dueVal = get('data-due'); // must be 'YYYY-MM-DD' or ''
    const dueInput = form.elements['due_date'];
    if (dueInput) {
    if (dueVal) {
        dueInput.value = dueVal;

        if (!dueInput.value) {
        const [y,m,d] = dueVal.split('-').map(Number);
        // valueAsDate wants 0-based months
        const local = new Date(y, m - 1, d);
        if (!isNaN(local)) dueInput.valueAsDate = local;
        }
    } else {
        dueInput.value = '';
    }
    }

    form.elements['comment'].value      = get('data-comment');
    form.elements['delivered_to'].value = get('data-delivered_to');
});