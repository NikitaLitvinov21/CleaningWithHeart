const form = document.getElementById("bookingForm");
const addressInput = form.querySelector("#addressInput");
const addressesSuggestions = form.querySelector("#addressesSuggestions");
const phoneInput = document.getElementById("phone_number")
const urlBase = location.protocol + "//" + location.host;
form.addEventListener("submit", saveBooking);

document.addEventListener("DOMContentLoaded", () => {
    const now = new Date();
    const year = now.getFullYear();
    const month = new String(now.getMonth() + 1).padStart(2, "0");
    const day = new String(now.getDate()).padStart(2, "0");
    const hours = new String(now.getHours()).padStart(2, "0");
    const minutes = new String(now.getMinutes()).padStart(2, "0");
    const currentDateTime = `${year}-${month}-${day} ${hours}:${minutes}`;
    const dateTimeInput = form.querySelector('input[name="start_datetime"]');
    dateTimeInput.min = currentDateTime;
});

const mask = new IMask(phoneInput,{
    mask:"+{1}(000)000-0000"
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
                    addressesSuggestions.style.display = "block"; // Показываем список

                    json.addresses.forEach((address) => {
                        const li = document.createElement("li");
                        li.textContent = address;
                        li.addEventListener("click", () => selectAddressesSuggestion(address));
                        addressesSuggestions.appendChild(li);
                    });
                } else {
                    addressesSuggestions.style.display = "none"; // Скрываем, если пусто
                }
            });
    } else {
        addressesSuggestions.style.display = "none";
    }
});

// Закрываем список при потере фокуса
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

    const firstName = document.querySelector("input[name='first_name']").value;
    const lastName = document.querySelector("input[name='last_name']").value;
    const phoneNumber = mask.masked.unmaskedValue;
    const email = document.querySelector("input[name='email']").value;
    const street = document.querySelector("input[name='street']").value;
    const startDatetime = document.querySelector("input[name='start_datetime']").value;
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
