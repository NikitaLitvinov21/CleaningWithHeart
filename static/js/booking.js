document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("bookingForm");
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const currentDateTime = `${year}-${month}-${day} ${hours}:${minutes}`;
    const dateTimeInput = form.querySelector('input[name="datetime_local"]');
    dateTimeInput.min = currentDateTime;
    
});

function saveBooking() {
    const form = document.getElementById("bookingForm");

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
        .then(response => {
            if (response.ok) {
                window.location.href = "/";
                return response.json();
            } else {
                throw new Error(response.status);
            }
        })
        .then(responseData => {
            console.log(responseData);
            return responseData;
        })
        .catch(error => {
            console.error("Error requesting - " + error);
        });
}
