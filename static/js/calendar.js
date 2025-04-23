document.addEventListener('DOMContentLoaded', () => {
    const urlBase = location.protocol + '//' + location.host;
    const calendarEl = document.getElementById('calendar');
    let currentPopover = null;

    const calendar = new FullCalendar.Calendar(calendarEl, {
        timeZone: 'America/Toronto',
        editable: true,
        selectable: true,
        navLinks: true,
        nowIndicator: true,
        dayMaxEventRows: true,
        allDaySlot: false,
        nowIndicator: true,
        businessHours: {
            daysOfWeek: [1, 2, 3, 4, 5],
            startTime: '9:00',
            endTime: '18:00',
        },
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
            <p><strong>Start:</strong> ${event.start.toLocaleString('en-CA', { timeZone: 'UTC' })}</p>
            <p><strong>End:</strong> ${event.end.toLocaleString('en-CA', { timeZone: 'UTC' })}</p>
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

    const customerSelect = document.getElementById("customerSelect");
    const customerButton = document.getElementById("customerButton");
    const newCustomerFields = document.getElementById("newCustomerFields");
    const customerIdInput = document.getElementById("customerId");

    customerButton.addEventListener("click", function (e) {
        e.preventDefault();
        const isUsingNew = !newCustomerFields.classList.contains("d-none");

        newCustomerFields.classList.toggle("d-none");

        const allFields = ["first_name", "last_name", "phone_number", "email", "street"];
        const requiredFields = ["first_name", "phone_number", "email", "street"];

        if (isUsingNew) {
            customerButton.classList.remove("new-customer");
            customerButton.textContent = "ADD NEW CUSTOMER";

            allFields.forEach(name => {
                const field = document.querySelector(`[name="${name}"]`);
                if (field) {
                    field.value = "";
                    field.removeAttribute("required");
                }
            });
        } else {
            customerSelect.value = "";
            customerIdInput.value = "";
            customerButton.classList.add("new-customer");
            customerButton.textContent = "CANCEL NEW CUSTOMER";

            allFields.forEach(name => {
                const field = document.querySelector(`[name="${name}"]`);
                if (field) field.value = "";
            });

            requiredFields.forEach(name => {
                const field = document.querySelector(`[name="${name}"]`);
                if (field) field.setAttribute("required", "required");
            });
        }
    });

    customerSelect.addEventListener("change", function () {
        if (customerSelect.value) {
            newCustomerFields.classList.add("d-none");
            ["first_name", "last_name", "phone_number", "email", "street"].forEach(name => {
                document.querySelector(`[name="${name}"]`).value = "";
            });
            customerIdInput.value = customerSelect.value;
        }
    });

    function loadCustomerOptions(selectedCustomerId = null) {
        const placeholderOption = customerSelect.querySelector("option[value='']");
        customerSelect.innerHTML = "";

        if (placeholderOption) {
            customerSelect.appendChild(placeholderOption);
        }

        fetch("/api/customers")
            .then(res => res.json())
            .then(data => {
                const customers = data.customers;
                customers.forEach(customer => {
                    const option = document.createElement("option");
                    option.value = customer.id;
                    option.textContent = `${customer.firstName} ${customer.lastName}`;
                    customerSelect.appendChild(option);
                });

                if (selectedCustomerId) {
                    customerSelect.value = selectedCustomerId;
                }
            })
            .catch(err => console.error("Error loading customers:", err));
    }

    function openSaveModal(info) {
        closePopover();
        form.reset();

        document.getElementById('modalTitle').innerText = 'SAVE BOOKING';
        document.getElementById("customerId").value = "";

        newCustomerFields.classList.add("d-none");
        customerButton.classList.remove("new-customer");
        customerButton.textContent = "ADD NEW CUSTOMER";

        const saveButton = document.querySelector('#saveButton');
        const editButton = document.querySelector('#editButton');
        saveButton?.classList.remove('d-none');
        editButton?.classList.add('d-none');

        const startDatetimeInput = document.querySelector("input[name='start_datetime']");
        if (startDatetimeInput) {
            const localDatetime = new Date(info.start.getTime()).toISOString().slice(0, 16);
            startDatetimeInput.value = localDatetime;
        }

        loadCustomerOptions();
        new bootstrap.Modal(document.getElementById('bookingModal')).show();
    }

    function openEditModal(event) {
        closePopover();

        document.getElementById('modalTitle').innerText = 'EDIT BOOKING';

        const saveButton = document.querySelector('#saveButton');
        const editButton = document.querySelector('#editButton');
        editButton?.classList.remove('d-none');
        saveButton?.classList.add('d-none');

        newCustomerFields.classList.add("d-none");
        customerButton.classList.remove("new-customer");
        customerButton.textContent = "ADD NEW CUSTOMER";

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

                loadCustomerOptions(booking.customer.id);

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
        const saveButton = document.querySelector('#saveButton');
        saveButton.disabled = true; 

        const booking = getFormData();
        const startDateTimeObj = new Date(booking.startDatetime);
        const finishDateTimeObj = new Date(booking.finishDatetime);

        const finishDatetimeInput = document.querySelector("input[name='end_datetime']");
        finishDatetimeInput.addEventListener('input', function () {
            const finishDatetime = finishDatetimeInput.value;
            const finishDateTimeObj = new Date(finishDatetime);
            validateFinishDatetime(startDateTimeObj, finishDateTimeObj, finishDatetimeInput);
        });

        validateFinishDatetime(startDateTimeObj, finishDateTimeObj, finishDatetimeInput);

        if (!form.checkValidity()) {
            form.reportValidity();
            saveButton.disabled = false;
            return;
        }

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
            })
            .finally(() => {
                saveButton.disabled = false;
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
        const timeZone = 'UTC';

        const patchedData = {
            start: event.start.toLocaleString('sv-SE', { timeZone, hour12: false }).replace(' ', 'T'),
            end: event.end.toLocaleString('sv-SE', { timeZone, hour12: false }).replace(' ', 'T')
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
        const editButton = document.querySelector('#editButton');
        editButton.disabled = true;

        const booking = getFormData();
        const startDateTimeObj = new Date(booking.startDatetime);
        const finishDateTimeObj = new Date(booking.finishDatetime);

        const finishDatetimeInput = document.querySelector("input[name='end_datetime']");
        finishDatetimeInput.addEventListener('input', function () {
            const finishDatetime = finishDatetimeInput.value;
            const finishDateTimeObj = new Date(finishDatetime);
            validateFinishDatetime(startDateTimeObj, finishDateTimeObj, finishDatetimeInput);
        });

        validateFinishDatetime(startDateTimeObj, finishDateTimeObj, finishDatetimeInput);

        if (!form.checkValidity()) {
            form.reportValidity();
            editButton.disabled = false;
            return;
        }

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
            })
            .finally(() => {
                editButton.disabled = false;
            });
    }

    function getFormData() {
        return {
            customerId: document.getElementById("customerId").value,
            firstName: document.querySelector("input[name='first_name']").value,
            lastName: document.querySelector("input[name='last_name']").value,
            phoneNumber: mask.masked.unmaskedValue,
            email: document.querySelector("input[name='email']").value,
            street: document.querySelector("input[name='street']").value,
            startDatetime: document.querySelector("input[name='start_datetime']").value,
            cleaningMasterName: document.querySelector("input[name='master']").value,
            finishDatetime: document.querySelector("input[name='end_datetime']").value,
            selectedService: document.querySelector("select[name='selected_service']").value,
            building: document.querySelector("select[name='building']").value,
            roomsNumber: document.querySelector("input[name='rooms_number']").value,
            squareFeet: document.querySelector("input[name='square_feet']").value,
            hasOwnEquipment: document.querySelector("select[name='use_equipment']").value,
            hasCleanWindows: document.querySelector("input[name='clean_windows']").checked,
            hasCleanOven: document.querySelector("input[name='clean_oven']").checked,
            hasCleanBasement: document.querySelector("input[name='clean_basement']").checked,
            hasMoveInCleaning: document.querySelector("input[name='move_in_cleaning']").checked,
            hasMoveOutCleaning: document.querySelector("input[name='move_out_cleaning']").checked,
            hasCleanFridge: document.querySelector("input[name='clean_fridge']").checked,
        };
    }
    
    function validateFinishDatetime(startDateTimeObj, finishDateTimeObj, finishDatetimeInput) {
        if (finishDateTimeObj < startDateTimeObj) {
            finishDatetimeInput.setCustomValidity("End time cannot be earlier than start time.");
        } else {
            finishDatetimeInput.setCustomValidity("");
        }
    }
});
