document.addEventListener('DOMContentLoaded', () => {
    const urlBase = location.protocol + '//' + location.host;
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
                eventMaxStack: 3,
            },
        },
        headerToolbar: {
            start: "dayGridMonth,timeGridWeek,timeGridDay,listWeek",
            center: "title",
            end: "prev,next today",
        },
        initialView: "timeGridWeek",
        eventColor: "#2c3e50",
        events: `${urlBase}/api/events`,
        eventClick: function (info) {
            fetch(`/api/booking/${info.event.id}`)
                .then(response => response.json())
                .then(data => showPopover(info.el, info.event, data))
                .catch(error => console.error("Error loading booking", error));
        },
        select: function (info) {
            openSaveModal(info);
        },
        eventDrop: function (info) {
            patchBooking(info.event);
        },
        eventResize: function (info) {
            patchBooking(info.event);
        }
    });

    calendar.render();

    function formatPhoneNumber(phoneNumber) {
        return phoneNumber.replace(/(\d{1})(\d{3})(\d{3})(\d{4})/, "+$1 ($2) $3-$4");
    }

    function showPopover(element, event, bookingData) {
        if (currentPopover) {
            currentPopover.dispose();
            currentPopover = null;
        }

        const popoverTitle = `
        <div class="d-flex justify-content-between align-items-center">
            <span>${event.title}</span>
            <span class="close-popover icon">
                <img src="/static/images/svg/close-icon.svg" alt="close-icon"
                    class="close-icon-popover icon-button"></span>
        </div>
    `;

        const popoverContent = `
        <div>
            <p><strong>Master:</strong> ${bookingData.cleaningMasterName || "-"}</p>
            <p><strong>Address:</strong> ${bookingData.customer.street || "-"}</p>
            <p><strong>Phone number:</strong> ${formatPhoneNumber(bookingData.customer.phoneNumber) || "-"}</p>
            <p><strong>Email:</strong> ${bookingData.customer.email || "-"}</p>
            <p><strong>Start:</strong> ${event.start.toLocaleString()}</p>
            <p><strong>End:</strong> ${event.end.toLocaleString()}</p>
            <div class="d-flex justify-content-end">
                <span>
                    <img src="/static/images/svg/edit-icon.svg" alt="edit-icon"
                        class="edit-icon icon-button">
                    <img src="/static/images/svg/delete-icon.svg" alt="delete-icon" 
                        class="delete-icon icon-button">
                </span>
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

    const phoneInput = document.getElementById("phone_number")
    const mask = new IMask(phoneInput, {
        mask: "+{1}(000)000-0000"
    })

    const form = document.getElementById("bookingForm");

    function openSaveModal(info) {
        closePopover();
        form.reset();

        document.getElementById('modalTitle').innerText = 'SAVE BOOKING';
        const saveButton = document.querySelector('#saveButton');
        const editButton = document.querySelector('#editButton');
        saveButton?.classList.remove('d-none');
        editButton?.classList.add('d-none');

        const startDatetimeInput = document.querySelector("input[name='start_datetime']");
        if (startDatetimeInput) {
            const localDatetime = new Date(info.start.getTime() - info.start.getTimezoneOffset() * 60000)
                .toISOString()
                .slice(0, 16);
            startDatetimeInput.value = localDatetime;
        }

        new bootstrap.Modal(document.getElementById('bookingModal')).show();
    }

    function openEditModal(event) {
        closePopover();

        document.getElementById('modalTitle').innerText = 'EDIT BOOKING';
        const saveButton = document.querySelector('#saveButton');
        const editButton = document.querySelector('#editButton');
        editButton?.classList.remove('d-none');
        saveButton?.classList.add('d-none')

        fetch(`/api/booking/${event.id}`)
            .then(response => response.json())
            .then(booking => {
                document.querySelector("input[name='first_name']").value = booking.customer.firstName;
                document.querySelector("input[name='last_name']").value = booking.customer.lastName;
                mask.value = booking.customer.phoneNumber;
                document.querySelector("input[name='email']").value = booking.customer.email;
                document.querySelector("input[name='street']").value = booking.customer.street;
                document.querySelector("input[name='start_datetime']").value = booking.startDatetime;
                document.querySelector("input[name='master']").value = booking.cleaningMasterName;
                document.querySelector("input[name='end_datetime']").value = booking.finishDatetime;
                document.querySelector("select[name='selected_service']").value = booking.selectedService;
                document.querySelector("select[name='building']").value = booking.building;
                document.querySelector("input[name='rooms_number']").value = booking.roomsNumber;
                document.querySelector("input[name='square_feet']").value = booking.squareFeet;
                document.querySelector("select[name='use_equipment']").value = booking.hasOwnEquipment;
                document.querySelector("input[name='clean_windows']").checked = booking.hasCleanWindows;
                document.querySelector("input[name='clean_oven']").checked = booking.hasCleanOven;
                document.querySelector("input[name='clean_basement']").checked = booking.hasCleanBasement;
                document.querySelector("input[name='move_in_cleaning']").checked = booking.hasMoveInCleaning;
                document.querySelector("input[name='move_out_cleaning']").checked = booking.hasMoveOutCleaning;
                document.querySelector("input[name='clean_fridge']").checked = booking.hasCleanFridge;
                document.getElementById("customerId").value = booking.customer.id;
                editButton.setAttribute("data-booking-id", booking.id);
                new bootstrap.Modal(document.getElementById("bookingModal")).show();
            })
            .catch(error => console.error("Error loading booking data:", error));
    }

    function openDeleteModal(event) {
        closePopover();
        document.querySelector("#delete-button").setAttribute("data-booking-id", event.id);
        const modal = new bootstrap.Modal(document.getElementById('deleteModal'));
        modal.show();
    }

    document.querySelector("#saveButton").addEventListener("click", function () {
        saveBooking();
    });

    function saveBooking() {

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const firstName = document.querySelector("input[name='first_name']").value;
        const lastName = document.querySelector("input[name='last_name']").value;
        const phoneNumber = mask.masked.unmaskedValue;
        const email = document.querySelector("input[name='email']").value;
        const street = document.querySelector("input[name='street']").value;
        const startDatetime = document.querySelector("input[name='start_datetime']").value;
        const cleaningMasterName = document.querySelector("input[name='master']").value;
        const finishDatetime = document.querySelector("input[name='end_datetime']").value;
        const selectedService = document.querySelector("select[name='selected_service']").value;
        const building = document.querySelector("select[name='building']").value;
        const roomsNumber = document.querySelector("input[name='rooms_number']").value;
        const squareFeet = document.querySelector("input[name='square_feet']").value;
        const hasOwnEquipment = document.querySelector("select[name='use_equipment']").value;
        const hasCleanWindows = document.querySelector("input[name='clean_windows']").checked;
        const hasCleanOven = document.querySelector("input[name='clean_oven']").checked;
        const hasCleanBasement = document.querySelector("input[name='clean_basement']").checked;
        const hasMoveInCleaning = document.querySelector("input[name='move_in_cleaning']").checked;
        const hasMoveOutCleaning = document.querySelector("input[name='move_out_cleaning']").checked;
        const hasCleanFridge = document.querySelector("input[name='clean_fridge']").checked;

        const booking = {
            firstName: firstName,
            lastName: lastName,
            phoneNumber: phoneNumber,
            email: email,
            street: street,
            startDatetime: startDatetime,
            cleaningMasterName: cleaningMasterName,
            finishDatetime: finishDatetime,
            selectedService: selectedService,
            building: building,
            roomsNumber: roomsNumber,
            squareFeet: squareFeet,
            hasOwnEquipment: hasOwnEquipment,
            hasCleanWindows: hasCleanWindows,
            hasCleanOven: hasCleanOven,
            hasCleanBasement: hasCleanBasement,
            hasMoveInCleaning: hasMoveInCleaning,
            hasMoveOutCleaning: hasMoveOutCleaning,
            hasCleanFridge: hasCleanFridge,
        };

        fetch("/api/booking", {
            method: "POST",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify(booking),
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
                return responseData;
            })
            .catch(error => {
                console.error(JSON.parse(error.message));
            });
    }

    document.querySelector("#delete-button").addEventListener("click", function () {
        const bookingId = this.getAttribute("data-booking-id");
        deleteBooking(bookingId);
    });

    function deleteBooking(bookingId) {
        fetch(`/api/booking/${bookingId}`, {
            method: "DELETE",
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
            .catch(error => {
                console.error(JSON.parse(error.message));
            });
    }

    function patchBooking(event) {
        const patchedData = {
            start: event.start.toISOString(),
            end: event.end.toISOString()
        };

        fetch(`/api/booking/${event.id}`, {
            method: "PATCH",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(patchedData)
        })
            .then(async response => {
                if (response.ok) {
                    return response.json();
                } else {
                    const responseWithError = await response.text();
                    throw new Error(responseWithError);
                }
            })
            .catch(error => {
                console.error(JSON.parse(error.message));
            });
    }

    document.querySelector("#editButton").addEventListener("click", function () {
        const bookingId = this.getAttribute("data-booking-id");
        editBooking(bookingId);
    });

    function editBooking(bookingId) {

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const customerId = document.getElementById("customerId").value;
        const firstName = document.querySelector("input[name='first_name']").value;
        const lastName = document.querySelector("input[name='last_name']").value;
        const phoneNumber = mask.masked.unmaskedValue;
        const email = document.querySelector("input[name='email']").value;
        const street = document.querySelector("input[name='street']").value;
        const startDatetime = document.querySelector("input[name='start_datetime']").value;
        const cleaningMasterName = document.querySelector("input[name='master']").value;
        const finishDatetime = document.querySelector("input[name='end_datetime']").value;
        const selectedService = document.querySelector("select[name='selected_service']").value;
        const building = document.querySelector("select[name='building']").value;
        const roomsNumber = document.querySelector("input[name='rooms_number']").value;
        const squareFeet = document.querySelector("input[name='square_feet']").value;
        const hasOwnEquipment = document.querySelector("select[name='use_equipment']").value;
        const hasCleanWindows = document.querySelector("input[name='clean_windows']").checked;
        const hasCleanOven = document.querySelector("input[name='clean_oven']").checked;
        const hasCleanBasement = document.querySelector("input[name='clean_basement']").checked;
        const hasMoveInCleaning = document.querySelector("input[name='move_in_cleaning']").checked;
        const hasMoveOutCleaning = document.querySelector("input[name='move_out_cleaning']").checked;
        const hasCleanFridge = document.querySelector("input[name='clean_fridge']").checked;

        const booking = {
            customerId: customerId,
            firstName: firstName,
            lastName: lastName,
            phoneNumber: phoneNumber,
            email: email,
            street: street,
            startDatetime: startDatetime,
            cleaningMasterName: cleaningMasterName,
            finishDatetime: finishDatetime,
            selectedService: selectedService,
            building: building,
            roomsNumber: roomsNumber,
            squareFeet: squareFeet,
            hasOwnEquipment: hasOwnEquipment,
            hasCleanWindows: hasCleanWindows,
            hasCleanOven: hasCleanOven,
            hasCleanBasement: hasCleanBasement,
            hasMoveInCleaning: hasMoveInCleaning,
            hasMoveOutCleaning: hasMoveOutCleaning,
            hasCleanFridge: hasCleanFridge,
        };

        fetch(`/api/booking/${bookingId}`, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json;charset=utf-8",
            },
            body: JSON.stringify(booking),
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
                return responseData;
            })
            .catch(error => {
                console.error(JSON.parse(error.message));
            });
    }
});

