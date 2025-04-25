const form = document.getElementById("bookingForm");
const addressInput = form.querySelector("#addressInput");
const addressesSuggestions = form.querySelector("#addressesSuggestions");
const phoneInput = document.getElementById("phone_number")
const urlBase = location.protocol + "//" + location.host;
form.addEventListener("submit", saveBooking);

$(document).ready(() => {
    const $dateInput = $('#booking_date');
    const $timeInput = $('#booking_time');
    const DateTime = luxon.DateTime;

    // Загружаем недоступные даты
    let blockedDatesSet = new Set();

    fetch('/api/unavailable-dates')
        .then(res => res.json())
        .then(unavailableDates => {
            unavailableDates.forEach(entry => {
                const start = DateTime.fromISO(entry.startDatetime, { zone: 'America/Toronto' }).startOf('day');
                const end = DateTime.fromISO(entry.finishDatetime, { zone: 'America/Toronto' })
                    .minus({ milliseconds: 1 })
                    .startOf('day');

                for (let date = start; date <= end; date = date.plus({ days: 1 })) {
                    blockedDatesSet.add(date.toISODate());
                }
            });

            flatpickr("#booking_date", {
                dateFormat: "Y-m-d",
                minDate: "today",
                maxDate: new Date().fp_incr(60),
                disable: [
                    function (date) {
                        const iso = DateTime.fromJSDate(date).toISODate();
                        return (date.getDay() === 0 || date.getDay() === 6 || blockedDatesSet.has(iso));
                    }
                ],
                onChange: function (selectedDates, dateStr) {
                    $dateInput.val(dateStr).trigger('change');
                }
            });
        });

    $dateInput.on('change', function () {
        const selectedDate = $(this).val();
        $timeInput.val('').prop('disabled', true);
        $('#start_datetime').val('');

        if (!selectedDate) return;

        fetch(`/api/booked-intervals?date=${selectedDate}`)
            .then(res => res.json())
            .then(data => {
                const disabledRanges = [];

                if (data.intervals) {
                    data.intervals.forEach(interval => {
                        const from = DateTime.fromISO(interval.from, { zone: 'America/Toronto' });
                        const to = DateTime.fromISO(interval.to, { zone: 'America/Toronto' });

                        if (from.toISODate() === selectedDate) {
                            disabledRanges.push([
                                from.toFormat('HH:mm'),
                                to.toFormat('HH:mm')
                            ]);
                        }
                    });
                }

                $timeInput.timepicker('remove');

                $timeInput.timepicker({
                    timeFormat: 'H:i',
                    step: 30,
                    minTime: '09:00',
                    maxTime: '14:00',
                    disableTimeRanges: disabledRanges
                });

                $timeInput.prop('disabled', false);
            });
    });

    $timeInput.on('change', function () {
        const selectedTime = $(this).val();
        const selectedDate = $dateInput.val();

        if (selectedDate && selectedTime) {
            const [hour, minute] = selectedTime.split(':');
            const start = DateTime.fromObject({
                year: parseInt(selectedDate.split('-')[0]),
                month: parseInt(selectedDate.split('-')[1]),
                day: parseInt(selectedDate.split('-')[2]),
                hour: parseInt(hour),
                minute: parseInt(minute)
            }, { zone: 'America/Toronto' });

            $('#start_datetime').val(start.toISO());
        }
    });
    
});

const mask = new IMask(phoneInput, {
    mask: "+{1}(000)000-0000"
})

addressInput.addEventListener("input", () => {
    const value = addressInput.value.trim();

    if (value) {
        const params = new URLSearchParams({ search: value });

        fetch(`${urlBase}/api/addresses?${params}`)
            .then((response) => response.json())
            .then((json) => {
                addressesSuggestions.innerHTML = ``;

                if (json.addresses.length > 0) {
                    addressesSuggestions.style.display = "block";

                    json.addresses.forEach((address) => {
                        const li = document.createElement("li");
                        li.textContent = address;
                        li.addEventListener("click", () => selectAddressesSuggestion(address));
                        addressesSuggestions.appendChild(li);
                    });
                } else {
                    addressesSuggestions.style.display = "none";
                }
            });
    } else {
        addressesSuggestions.style.display = "none";
    }
});

document.addEventListener("click", (e) => {
    if (!addressInput.contains(e.target) && !addressesSuggestions.contains(e.target)) {
        addressesSuggestions.style.display = "none";
    }
});

function selectAddressesSuggestion(suggestion) {
    addressInput.value = suggestion;
    addressesSuggestions.style.display = "none";
}

addressInput.addEventListener("blur", () => {
    setTimeout(() => {
        addressesSuggestions.innerHTML = ``;
    }, 1000);
})

function saveBooking(event) {
    event.preventDefault();

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const startDatetime = document.querySelector("input[name='start_datetime']").value;
    const firstName = document.querySelector("input[name='first_name']").value;
    const lastName = document.querySelector("input[name='last_name']").value;
    const phoneNumber = mask.masked.unmaskedValue;
    const email = document.querySelector("input[name='email']").value;
    const street = document.querySelector("input[name='street']").value;
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

    const saveBooking = {
        firstName: firstName,
        lastName: lastName,
        phoneNumber: phoneNumber,
        email: email,
        street: street,
        startDatetime: startDatetime,
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
        body: JSON.stringify(saveBooking),
    })
        .then(async (response) => {
            if (response.ok) {
                return response.json();
            } else {
                const responseWithError = await response.text();
                throw new Error(responseWithError);
            }
        })
        .then((responseData) => {
            console.log(responseData);
            document.querySelector("#fleshes").innerHTML = `
                <div class="alert alert-success">${responseData.message}</div>
            `;
            document.querySelector("#saveButton").remove();
            document.querySelector("#returnButton").classList.remove("d-none");
        })
        .catch((error) => {
            console.error(JSON.parse(error.message));
        });
}

