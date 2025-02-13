# Описание всех возможностей API.

## Сущность Booking

### Получение массива Booking-ов

Параметры запроса (Если не указан - будет значение по умолчанию):

`limit` - сколько выводить на страницу (default - 20)

`page` - какая страница (default - 1)

Можно использовать `URLSearchParams` в JavaScript для построения запроса.

![GetBookings](./images/Get%20bookings.png)

![GetBookingsWithParams](./images/Get%20bookings%20with%20params.png)

![GetBookingsWithPage](./images/Get%20booking%20with%20page.png)

![GetBookingsWithMaster](./images/Get%20booking%20with%20master.png)

Ответ:

`bookings` - все Booking-и в рамках страницы.

`count` - общее количество всех Booking-ов.

### Получение Booking-а по ID

![GetBookingByID](./images/Get%20booking%20by%20id.png)

### Создание Booking-а

При создание Booking-а все его параметры стоит передавать строками, а сами они написаны в `snake_case`, что, вероятно, является нарушением стандарта.

Это связано, с реализации функционала отправки на сервер в `booking.js`:

```javascript
const formData = new FormData(form);

const body = {};

for (const [key, value] of formData.entries()) {
    body[key] = value;
}
```

Это передаёт в `body` для запроса значения всех полей формы по `name` как строки.
А так как все `name`-ы в `snake_case` - выходит именно так.

![CreateBooking](./images/POST%20booking.png)

Примеры некоторых ошибочных запросов.

Не верный адрес почты.

![CreateBookingIncorrectEmail](./images/POST%20customer%20incorrect%20email.png)

Не верный номер телефона.

![CreateBookingIncorrectPhone](./images/POST%20customer%20incorrect%20phone.png)

### Обновление Booking-а

![UpdateBooking](./images/Update%20booking.png)

Примеры некоторых ошибочных запросов.

Не верный адрес почты.

![UpdateBookingIncorrectEmail](./images/Update%20Booking%20Incorrect%20email.png)

Не верный номер телефона.

![UpdateBookingIncorrectPhone](./images/Update%20Booking%20Incorrect%20phone.png)

Если передать `use_equipment` как `true`, то в конечном счёте он будет расценен как `false`. Это связано с особенностью реализации описных в пункте `Создание Booking-а`. Пока стоит передавать как `"true"` или не передавать вообще, чтобы было `false`.

![UpdateBookingWithBoolean](./images/Update%20booking%20with%20boolean.png)

### Удаление Booking-а

![DeleteBooking](./images/Delete%20booking.png)

## Сущность Customer

### Получение массива Customer-ов

Параметры запроса:

`limit` - сколько выводить на страницу (default - 20)

`page` - какая страница (page - 1)

Можно использовать `URLSearchParams` в JavaScript для построения запроса.

![GetCustomers](./images/Get%20customers.png)

![GetCustomersWithParams](./images/Get%20customers%20with%20params.png)

![GetCustomersWithParamsCount](./images/Get%20customers%20with%20params%20count.png)

Ответ:

`customers` - все Customer-ы в рамках страницы.

`count` - общее количество всех Customer-ов.

### Получение Customer-а по ID

![GetCustomer](./images/Get%20customer%20by%20id.png)

Если Customer не найден - будет соответствущая ошибка.

![CustomerNotFound](./images/Get%20customer%20not%20found.png)

### Создание Customer-а

![CreateCustomer](./images/POST%20customer.png)

`lastName` опционален. Если его не передать, то он будет просто `""`.

`specialNotes` опционален. Если его не передать, то он будет просто `null`.

Примеры некоторых ошибочных запросов.

Не верный адрес почты.

![CreateBookingIncorrectEmail](./images/POST%20customer%20incorrect%20email.png)

Не верный номер телефона.

![CreateBookingIncorrectPhone](./images/POST%20customer%20incorrect%20phone.png)

### Обновление Customer-а

![UpdateCustomer](./images/Update%20customer.png)

`lastName` опционален. Если его не передать, то он будет просто `""`.

`specialNotes` опционален. Если его не передать, то он будет просто `null`.

### Удаление Customer-а

![DeleteCustomer](./images/Delete%20customer.png)

## Псевдосущность Event

`Event` формируются из `Booking`-ов и служит удобством для отображения их на календаре. В базе данных **не существует сущности Event** на данный момент.

### Получение массива Event-ов

Параметры запроса:

`start` - start datetime

`end` - end datetime

Можно использовать `URLSearchParams` в JavaScript для построения запроса.

![GetEvents](./images/Get%20Events.png)

Ответ:

`events` - все Event-ы в рамках страницы.

`count` - общее количество всех Booking-ов.
