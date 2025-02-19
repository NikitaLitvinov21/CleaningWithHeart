const form = document.getElementById("bookingForm");
const addressInput = form.querySelector("#addressInput");
const addressesSuggestions = form.querySelector("#addressesSuggestions");
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

addressInput.addEventListener("input", () => {
    const value = addressInput.value;

    if (value) {
        const params = new URLSearchParams({
            search: value,
        });

        fetch(`${urlBase}/api/addresses?${params}`)
            .then((response) => response.json())
            .then((json) => {
                addressesSuggestions.innerHTML = ``;
                let index = 0;
                json.addresses.forEach((address) => {
                    addressesSuggestions.insertAdjacentHTML(
                        "beforeend", `
                        <div class="address-suggestion" onclick="selectAddressesSuggestion(this.innerText)" style="top: ${index * 50}px">${address}</div>
                    `
                    );
                    index++;
                });
            });
    } else {
        addressesSuggestions.innerHTML = ``;
    }
});

addressInput.addEventListener("blur", () => {
    setTimeout(() => {
        addressesSuggestions.innerHTML = ``;
    }, 1000);
})

function selectAddressesSuggestion(suggestion) {
    addressInput.value = suggestion;
    addressesSuggestions.innerHTML = ``;
}

function saveBooking(event) {
    event.preventDefault();

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
