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

    const formData = new FormData(form);

    const body = {};

    for (const [key, value] of formData.entries()) {
        body[key] = value;
    }

    console.log(body);

    fetch("/api/booking", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify(body),
    })
        .then(async response => {
            if (response.ok) {
                // window.location.href = "/";  // ???
                return response.json();
            } else {
                const responseWithError = await response.json();
                throw new Error(responseWithError);
            }
        })
        .then(responseData => {
            console.log(JSON.parse(responseData));
        })
        .catch(error => {
            console.error(JSON.parse(error.message));
        });
}
