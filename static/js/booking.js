const form = document.getElementById("bookingForm");
form.addEventListener("submit", saveBooking);

document.addEventListener("DOMContentLoaded", () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const currentDateTime = `${year}-${month}-${day} ${hours}:${minutes}`;
    const dateTimeInput = form.querySelector('input[name="start_datetime"]');
    dateTimeInput.min = currentDateTime;
});

function saveBooking(event) {
    event.preventDefault();

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const firstName = document.querySelector("input[name='first_name']").value;
    const lastName = document.querySelector("input[name='last_name']").value;
    const phoneNumber = document.querySelector("input[name='phone_number']").value;
    const email = document.querySelector("input[name='email']").value;
    const street = document.querySelector("input[name='street']").value;
    const startDatetime = document.querySelector("input[name='start_datetime']").value;
    const selectedService = document.querySelector("select[name='selected_service']").value;
    const building = document.querySelector("select[name='building']").value;
    const roomsNumber = document.querySelector("input[name='rooms_number']").value;
    const squareFeet = document.querySelector("input[name='square_feet']").value;
    const useEquipment = document.querySelector("select[name='use_equipment']").value;
    const cleanWindows = document.querySelector("input[name='clean_windows']").checked;
    const cleanOven = document.querySelector("input[name='clean_oven']").checked;
    const cleanBasement = document.querySelector("input[name='clean_basement']").checked;
    const moveInCleaning = document.querySelector("input[name='move_in_cleaning']").checked;
    const moveOutCleaning = document.querySelector("input[name='move_out_cleaning']").checked;
    const cleanFridge = document.querySelector("input[name='clean_fridge']").checked;

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
        useEquipment: useEquipment,
        cleanWindows: cleanWindows,
        cleanOven: cleanOven,
        cleanBasement: cleanBasement,
        moveInCleaning: moveInCleaning,
        moveOutCleaning: moveOutCleaning,
        cleanFridge: cleanFridge,
    };

    fetch("/api/booking", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify(saveBooking),
    })
        .then(async response => {
            if (response.ok) {
                return response.json();
            } else {
                const responseWithError = await response.text();
                throw new Error(responseWithError);
            }
        })
        .then(responseData => {
            console.log(responseData);
            document.querySelector("#fleshes").innerHTML = `
                <div class="alert alert-success">${responseData.message}</div>
            `;
            document.querySelector("#saveButton").remove()
            document.querySelector("#returnButton").classList.remove("d-none")
        })
        .catch(error => {
            console.error(JSON.parse(error.message));
        });
}
