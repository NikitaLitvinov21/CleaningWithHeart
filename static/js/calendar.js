document.addEventListener('DOMContentLoaded', () => {
    const calendarEl = document.getElementById('calendar');
    const modal = document.getElementById('bookingModal');
     const calendar = new FullCalendar.Calendar(calendarEl, {
         editable: true,
         selectable: true,
         headerToolbar: {
             start: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
             center: 'title',
             end: 'prev,next today',
         },
         events: [
             {
                 id: '1',
                 title: 'Event 1',
                 start: '2025-01-10T14:00:00',
                 end: '2025-01-10T16:00:00',
             },
             {
                 id: '2',
                 title: 'Event 2',
                 start: '2025-01-11T10:00:00',
                 end: '2025-01-11T11:00:00',
             },
         ],
         eventContent: function (arg) {
             const title = document.createElement('span');
             title.innerText = arg.event.title
             const deleteIcon = document.createElement('span');
             deleteIcon.innerHTML = '❌';
             deleteIcon.style.cursor = 'pointer';
             deleteIcon.style.marginLeft = '10px';
             deleteIcon.style.color = 'red'
             deleteIcon.addEventListener('click', (e) => {
                 e.stopPropagation();
                 if (confirm(`Вы хотите удалить событие "${arg.event.title}"?`)) {
                     arg.event.remove();
                     alert('Событие удалено!');
                 }
             })
             const editIcon = document.createElement('span');
             editIcon.innerHTML = '✏️';
             editIcon.className = 'edit-icon';
             editIcon.style.cursor = 'pointer';
             editIcon.style.marginLeft = '10px';
             editIcon.style.color = 'blue'
             editIcon.addEventListener('click', () => openEditModal(arg.event));
             const container = document.createElement('div');
             container.appendChild(title);
             container.appendChild(editIcon);
             container.appendChild(deleteIcon)
             return { domNodes: [container] };
         },
     })
     calendar.render();

    function openEditModal(event) {
        const modal = new bootstrap.Modal(document.getElementById('bookingModal'));
        modal.show();
    }
});