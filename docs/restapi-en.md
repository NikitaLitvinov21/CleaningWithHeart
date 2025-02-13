# Description of all API capabilities.

## Booking Entity

### Getting an array of Bookings

Request parameters (If not specified - default value will be used):

`limit` - how many items to display per page (default - 20)

`page` - which page to display (default - 1)

You can use `URLSearchParams` in JavaScript to build the query.

![GetBookings](./images/Get%20bookings.png)

![GetBookingsWithParams](./images/Get%20bookings%20with%20params.png)

![GetBookingsWithPage](./images/Get%20booking%20with%20page.png)

![GetBookingsWithMaster](./images/Get%20booking%20with%20master.png)

Response:

`bookings` - all Bookings within the page.

`count` - total number of all Bookings.

### Getting a Booking by ID

![GetBookingByID](./images/Get%20booking%20by%20id.png)

### Creating a Booking

When creating a Booking, all its parameters should be passed as strings, and they are written in `snake_case`, which is probably a violation of the standard.

This is related to the implementation of request functionality in `booking.js`:

```javascript
const formData = new FormData(form);

const body = {};

for (const [key, value] of formData.entries()) {
    body[key] = value;
}
```

This passes the values of all form fields by `name` as strings to the `body` for the request.
And since all `name`s are in `snake_case` - this is how it turns out.

![CreateBooking](./images/POST%20booking.png)

Examples of some erroneous requests.

Incorrect email address.

![CreateBookingIncorrectEmail](./images/POST%20customer%20incorrect%20email.png)

Incorrect phone number.

![CreateBookingIncorrectPhone](./images/POST%20customer%20incorrect%20phone.png)

### Updating a Booking

![UpdateBooking](./images/Update%20booking.png)

Examples of some erroneous requests.

Incorrect email address.

![UpdateBookingIncorrectEmail](./images/Update%20Booking%20Incorrect%20email.png)

Incorrect phone number.

![UpdateBookingIncorrectPhone](./images/Update%20Booking%20Incorrect%20phone.png)

If you pass `use_equipment` as `true`, it will ultimately be treated as `false`. This is due to the implementation features described in the "Creating a Booking" section. For now, you should pass it as `"true"` or not pass it at all to have it as `false`.

![UpdateBookingWithBoolean](./images/Update%20booking%20with%20boolean.png)

### Deleting a Booking

![DeleteBooking](./images/Delete%20booking.png)

## Customer Entity

### Getting an array of Customers

Request parameters:

`limit` - how many items to display per page (default - 20)

`page` - which page to display (default - 1)

You can use `URLSearchParams` in JavaScript to build the query.

![GetCustomers](./images/Get%20customers.png)

![GetCustomersWithParams](./images/Get%20customers%20with%20params.png)

![GetCustomersWithParamsCount](./images/Get%20customers%20with%20params%20count.png)

Response:

`customers` - all Customers within the page.

`count` - total number of all Customers.

### Getting a Customer by ID

![GetCustomer](./images/Get%20customer%20by%20id.png)

If the Customer is not found - there will be a corresponding error.

![CustomerNotFound](./images/Get%20customer%20not%20found.png)

### Creating a Customer

![CreateCustomer](./images/POST%20customer.png)

`lastName` is optional. If not provided, it will simply be `""`.

`specialNotes` is optional. If not provided, it will be `null`.

Examples of some erroneous requests.

Incorrect email address.

![CreateBookingIncorrectEmail](./images/POST%20customer%20incorrect%20email.png)

Incorrect phone number.

![CreateBookingIncorrectPhone](./images/POST%20customer%20incorrect%20phone.png)

### Updating a Customer

![UpdateCustomer](./images/Update%20customer.png)

`lastName` is optional. If not provided, it will simply be `""`.

`specialNotes` is optional. If not provided, it will be `null`.

### Deleting a Customer

![DeleteCustomer](./images/Delete%20customer.png)

## Event Pseudo-entity

`Events` are formed from `Bookings` and serve as a convenience for displaying them on the calendar. There is currently **no Event entity in the database**.

### Getting an array of Events

Request parameters:

`start` - start datetime

`end` - end datetime

You can use `URLSearchParams` in JavaScript to build the query.

![GetEvents](./images/Get%20Events.png)

Response:

`events` - all Events within the page.

`count` - total number of all Bookings.
