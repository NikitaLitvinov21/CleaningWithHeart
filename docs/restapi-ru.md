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

Ответ:

`bookings` - все Booking-и в рамках страницы.

`count` - общее количество всех Booking-ов.

### Получение Booking-а по ID

![GetBookingByID](./images/Get%20booking%20by%20id.png)

### Создание Booking-а

![CreateBooking](./images/POST%20booking.png)

Также, можно просто писать сам id клиента:

![CreateBookingWithCustomerID](./images/POST%20booking%20with%20customer%20id.png)

![CreateBookingWithCustomerID2](./images/POST%20booking%20with%20customer%20id%202.png)

### Обновление Booking-а

![UpdateBooking](./images/Update%20booking.png)

Также, можно обновить только даты при помощи **PATCH-запроса**:

![UpdateBooking](./images/Update%20booking%20range.png)

### Удаление Booking-а

![DeleteBooking](./images/Delete%20booking.png)

## Сущность Customer

### Получение массива Customer-ов

Параметры запроса:

`limit` - сколько выводить на страницу (default - 20)

`page` - какая страница (page - 1)

`only_names` - логический параметр, что указывает на получении только имён и id.

Можно использовать `URLSearchParams` в JavaScript для построения запроса.

![GetCustomers](./images/Get%20customers.png)

![GetCustomersWithParamsOnlyNames](./images/Get%20customers%20only%20names.png)

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

![CreateCustomerIncorrectEmail](./images/POST%20customer%20incorrect%20email.png)

Не верный номер телефона.

![CreateCustomerIncorrectPhone](./images/POST%20customer%20incorrect%20phone.png)

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

## Масив адресов

### Получение массива адресов

Параметры запроса:

`search` - сам поисковой запрос, что вводит пользователь.

![GetAddresses](./images/Get%20addresses.png)

![GetAddresses2](./images/Get%20addresses%202.png)

![GetAddresses3](./images/Get%20addresses%203.png)

Пример кода:

```javascript
const urlBase = location.protocol + "//" + location.host;

const params = new URLSearchParams({
    search: value,
});

fetch(`${urlBase}/api/addresses?${params}`).
//... existing code ...
```
