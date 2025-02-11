document.addEventListener('DOMContentLoaded', () => {
    const calendarEl = document.getElementById('calendar');
    let currentPopover = null;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        editable: true,
        selectable: true,
        navLinks: true,
        nowIndicator: true,
        dayMaxEventRows: true,
        allDaySlot: false,
        nowIndicator: true,
        views: {
            timeGrid: {
                eventMaxStack: 3
            }
        },
        headerToolbar: {
            start: 'dayGridMonth,timeGridWeek,timeGridDay,listWeek',
            center: 'title',
            end: 'prev,next today',
        },
        initialView: 'timeGridWeek',
        eventColor: '#2c3e50',
        events: [
            { id: '1', title: 'Event 1', start: '2025-01-10T14:00:00', end: '2025-01-10T16:00:00' },
            { id: '2', title: 'Event 2', start: '2025-01-11T10:00:00', end: '2025-01-11T11:00:00' },
            { id: '3', title: 'Event 3', start: '2025-01-11T10:00:00', end: '2025-01-11T11:00:00' },
            { id: '4', title: 'Event 4', start: '2025-01-11T10:00:00', end: '2025-01-11T11:00:00' },
            { id: '5', title: 'Event 5', start: '2025-01-11T10:00:00', end: '2025-01-11T11:00:00' },
            { id: '6', title: 'Event 6', start: '2025-01-11T10:00:00', end: '2025-01-11T11:00:00' }
        ],
        eventClick: function (info) {
            showPopover(info.el, info.event);
        },
        select: function (info) {
            openSaveModal(info);
        }
    });

    calendar.render();

    function showPopover(element, event) {
        if (currentPopover) {
            currentPopover.dispose();
            currentPopover = null;
        }

        const popoverTitle = `
            <div class="d-flex justify-content-between align-items-center">
                <span>${event.title}</span>
                <span class="close-popover icon">❌</span>
            </div>
        `;

        const popoverContent = `
            <div>
                <p><strong>Начало:</strong> ${event.start.toLocaleString()}</p>
                ${event.end ? `<p><strong>Конец:</strong> ${event.end.toLocaleString()}</p>` : ''}
                <div class="d-flex justify-content-end">
                    <span class="edit-icon icon">✏️</span>
                    <span class="delete-icon icon">🗑️</span>
                </div>
            </div>
        `;

        currentPopover = new bootstrap.Popover(element, {
            content: popoverContent,
            title: popoverTitle,
            html: true,
            placement: 'auto',
            trigger: 'manual',
            container: 'body'
        });

        currentPopover.show();

        const popoverElement = document.querySelector('.popover');
        if (popoverElement) {
            popoverElement.querySelector('.edit-icon').addEventListener('click', () => openEditModal(event));
            popoverElement.querySelector('.delete-icon').addEventListener('click', () => openDeleteModal(event));
            popoverElement.querySelector('.close-popover').addEventListener('click', closePopover);
        }

        document.addEventListener('click', closePopoverOnClickOutside, true);
    }

    function closePopover() {
        if (currentPopover) {
            currentPopover.dispose();
            currentPopover = null;
        }
        document.removeEventListener('click', closePopoverOnClickOutside, true);
    }

    function closePopoverOnClickOutside(event) {
        const popoverElement = document.querySelector('.popover');
        if (popoverElement && !popoverElement.contains(event.target) && !event.target.closest('.fc-event')) {
            closePopover();
        }
    }

    function openSaveModal(event) {
        closePopover();
        document.getElementById('modalTitle').innerText = 'SAVE BOOKING';

        const modal = new bootstrap.Modal(document.getElementById('bookingModal'));

        const saveButton = document.querySelector('#saveButton');
        const editButton = document.querySelector('#editButton');

        saveButton?.classList.remove('d-none');
        editButton?.classList.add('d-none')

        modal.show();
    }

    function openEditModal(event) {
        closePopover();
        document.getElementById('modalTitle').innerText = 'EDIT BOOKING';

        const modal = new bootstrap.Modal(document.getElementById('bookingModal'));

        const saveButton = document.querySelector('#saveButton');
        const editButton = document.querySelector('#editButton');

        editButton?.classList.remove('d-none');
        saveButton?.classList.add('d-none')

        modal.show();
    }

    function openDeleteModal(event) {
        closePopover();
        const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
        modal.show();
    }
});

const form = document.getElementById("bookingForm");

function saveBooking(event) {

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const formData = new FormData(form);

    const body = {};

    for (const [key, value] of formData.entries()) {
        body[key] = value;
    }

    fetch("/api/booking", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify(body),
    })
        .then(async response => {
            if (response.ok) {
                window.location.reload();
                return response.json();
            } else {
                const responseWithError = await response.text();
                throw new Error(responseWithError);
            }
        })
        .then(responseData => {
            console.log(responseData);
            return responseData;
        })
        .catch(error => {
            console.error(JSON.parse(error.message));
        });
}
