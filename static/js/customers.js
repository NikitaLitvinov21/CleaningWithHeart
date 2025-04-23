document.addEventListener("DOMContentLoaded", function () {
    fetchCustomers();
});

document.getElementById("itemsPerPage").addEventListener("change", function () {
    fetchCustomers();
});

function fetchCustomers(page = 1) {
    const itemsPerPage = document.getElementById("itemsPerPage").value;
    currentPage = page;

    const params = new URLSearchParams({
        page: currentPage,
        limit: itemsPerPage
    });

    const url = `${location.protocol}//${window.location.host}/api/customers?${params.toString()}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const totalEvents = data.count;
            const totalPages = itemsPerPage ? Math.ceil(totalEvents / itemsPerPage) : 1;

            updateCustomersTable(data.customers);
            updatePagination(totalPages);

            if (data.customers.length === 0 && currentPage > 1) {
                currentPage -= 1;
                fetchCustomers(currentPage);
            }
        })
        .catch(error => console.error("Error fetching table data:", error));
}

function updatePagination(totalPages) {
    const pagination = document.getElementById("pagination");
    pagination.innerHTML = "";

    if (totalPages === 0) {
        pagination.innerHTML = `
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Назад" data-page="1"><span aria-hidden="true"><</span></a>
            </li>
            <li class="page-item active">
                <a class="page-link" href="#" data-page="1">1</a>
            </li>
            <li class="page-item disabled">
                <a class="page-link" href="#" aria-label="Вперед" data-page="1"><span aria-hidden="true">></span></a>
            </li>
        `;
        return;
    }

    const prevClass = currentPage === 1 ? "disabled" : "";
    pagination.innerHTML += `
        <li class="page-item ${prevClass}">
            <a class="page-link" href="#" aria-label="Назад" data-page="${currentPage - 1}"><span aria-hidden="true"><</span></a>
        </li>
    `;

    let startPage = Math.max(1, currentPage - 2);
    let endPage = Math.min(totalPages, currentPage + 2);

    if (totalPages > 5) {
        if (currentPage <= 3) {
            endPage = 5;
        } else if (currentPage + 2 >= totalPages) {
            startPage = totalPages - 4;
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        const activeClass = i === currentPage ? "active" : "";
        pagination.innerHTML += `
            <li class="page-item ${activeClass}">
                <a class="page-link" href="#" data-page="${i}">${i}</a>
            </li>
        `;
    }

    const nextClass = currentPage === totalPages ? "disabled" : "";
    pagination.innerHTML += `
        <li class="page-item ${nextClass}">
            <a class="page-link" href="#" aria-label="Вперед" data-page="${currentPage + 1}"><span aria-hidden="true">></span></a>
        </li>
    `;

    pagination.querySelectorAll("a").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            const selectedPage = parseInt(this.dataset.page);
            if (!isNaN(selectedPage) && selectedPage >= 1 && selectedPage <= totalPages) {
                currentPage = selectedPage;
                fetchCustomers(currentPage);
            }
        });
    });
}

function formatPhoneNumber(phoneNumber) {
    return phoneNumber.replace(/(\d{1})(\d{3})(\d{3})(\d{4})/, "+$1 ($2) $3-$4");
}

function updateCustomersTable(customers) {
    const tbody = document.querySelector(".customers-table tbody");
    tbody.innerHTML = "";
    customers.forEach(customer => {
        const row = document.createElement("tr");
        row.classList.add("table-row");
        row.innerHTML = `
            <td class="expand-column text-center">${customer.firstName}</td>
            <td class="expand-column text-center">${customer.lastName}</td>
            <td class="expand-column text-center">${formatPhoneNumber(customer.phoneNumber)}</td>
            <td class="expand-column text-center">${customer.email}</td>
            <td class="expand-column text-center">${customer.street}</td>
            <td class="expand-column text-center">${customer.specialNotes || "-"}</td>
            <td class="expand-column text-center">
                <span class="ceil-text text-nowrap">
                    <img src="/static/images/svg/edit-icon.svg" alt="edit-icon" 
                        class="edit-icon icon-button" data-customer-id="${customer.id}">
                    <img src="/static/images/svg/delete-icon.svg" alt="delete-icon" 
                        class="delete-icon icon-button" data-customer-id="${customer.id}">
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });

    document.querySelectorAll(".edit-icon").forEach(icon => {
        icon.addEventListener("click", function () {
            const customerId = this.dataset.customerId;
            openEditModal(customerId);
        });
    });

    document.querySelectorAll(".delete-icon").forEach(icon => {
        icon.addEventListener("click", function () {
            const customerId = this.dataset.customerId;
            openDeleteModal(customerId);
        });
    });
}

const phoneInput = document.getElementById("phone_number")
const mask = new IMask(phoneInput, {
    mask: "+{1}(000)000-0000"
})

function openEditModal(customerId) {
    fetch(`/api/customers/${customerId}`)
        .then(response => response.json())
        .then(customer => {
            document.querySelector("input[name='first_name']").value = customer.firstName;
            document.querySelector("input[name='last_name']").value = customer.lastName;
            mask.value = customer.phoneNumber;
            document.querySelector("input[name='email']").value = customer.email;
            document.querySelector("input[name='street']").value = customer.street;
            document.querySelector("textarea[name='notes']").value = customer.specialNotes || "";
            document.querySelector("#edit-button").setAttribute("data-customer-id", customerId);

            new bootstrap.Modal(document.getElementById("customerModal")).show();
        })
        .catch(error => console.error("Error loading customer data:", error));
}


function openDeleteModal(customerId) {
    document.querySelector("#delete-button").setAttribute("data-customer-id", customerId);
    new bootstrap.Modal(document.getElementById("deleteModal")).show();
}

document.querySelector("#edit-button").addEventListener("click", function () {
    const customerId = this.getAttribute("data-customer-id");
    editCustomer(customerId);
});

document.querySelector("#delete-button").addEventListener("click", function () {
    const customerId = this.getAttribute("data-customer-id");
    deleteCustomer(customerId);
});

function editCustomer(customerId) {
    const form = document.getElementById("customerForm");

    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }

    const firstName = document.querySelector("input[name='first_name']").value;
    const lastName = document.querySelector("input[name='last_name']").value;
    const phoneNumber = mask.masked.unmaskedValue;
    const email = document.querySelector("input[name='email']").value;
    const street = document.querySelector("input[name='street']").value;
    const specialNotes = document.querySelector("textarea[name='notes']").value;

    const updatedCustomer = {
        firstName: firstName,
        lastName: lastName,
        phoneNumber: phoneNumber,
        email: email,
        street: street,
        specialNotes: specialNotes,
    };

    fetch(`/api/customers/${customerId}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify(updatedCustomer),
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
            console.log(responseData);
            return responseData;
        })
        .catch(error => {
            console.error(JSON.parse(error.message));
        });
}

function deleteCustomer(customerId) {
    fetch(`/api/customers/${customerId}`, {
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