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

    fetch("/api/booking", {
        method: "POST",
        headers: {
            "Content-Type": "application/json;charset=utf-8",
        },
        body: JSON.stringify(body),
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
