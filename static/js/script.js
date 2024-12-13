const scrollTopButton = document.getElementById("scroll-top");
const firstSection = document.getElementById("aboutId");

window.addEventListener("scroll", () => {
    const firstSectionBottom = firstSection.getBoundingClientRect().top;

    if (firstSectionBottom < -150) {
        scrollTopButton.classList.add("show");
    } else {
        scrollTopButton.classList.remove("show");
    }
});

scrollTopButton.addEventListener("click", () => {
    document.body.scrollIntoView({
        behavior: "smooth",
    });
});

function onEntry(entry) {
    entry.forEach(change => {
        if (change.isIntersecting) {
            change.target.classList.add("element-show");
        }
    });
}

let options = {
    threshold: [0.5],
};
let observer = new IntersectionObserver(onEntry, options);
let elements = document.querySelectorAll(".element-animation");

for (let elm of elements) {
    observer.observe(elm);
}

const tracks = document.querySelectorAll(".testimonial-track");

tracks.forEach(track => {
    track.addEventListener("mouseover", () => {
        track.style.animationPlayState = "paused";
    });

    track.addEventListener("mouseout", () => {
        track.style.animationPlayState = "running";
    });
});

let modal = null;

document.addEventListener("DOMContentLoaded", function () {
    const modalEl = document.querySelector("#bookingModal");
    modal = modalEl ? new bootstrap.Modal(modalEl) : null;
});

const bookingButtons = document.querySelectorAll(".booking");
bookingButtons.forEach(button => {
    button.addEventListener("click", openCreateModal);
});

function openCreateModal() {
    const form = document.getElementById("bookingForm");
    document.getElementById("modalTitle").innerText = "Book a Service";

    const now = new Date();

    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, "0");
    const day = String(now.getDate()).padStart(2, "0");
    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");
    const currentDateTime = `${year}-${month}-${day} ${hours}:${minutes}`;
    const dateTimeInput = form.querySelector('input[name="datetime_local"]');
    dateTimeInput.min = currentDateTime;
    modal.show();
}

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
