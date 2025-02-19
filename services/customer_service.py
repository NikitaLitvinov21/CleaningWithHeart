from typing import List, Optional

from sqlalchemy.orm import Session

from common.exceptions.entity_not_found_exception import EntityNotFoundError
from common.utils.transaction import transaction
from database.connector import get_session
from models.customer import Customer


class CustomerService:

    @transaction
    def retrieve_customers(
        self,
        limit: int,
        page: int,
        session: Session,
        only_names: bool = False,
    ) -> List[Customer]:
        offset_value = (page - 1) * limit

        if only_names:
            query = session.query(
                Customer.id,
                Customer.first_name,
                Customer.last_name,
            )
        else:
            query = session.query(Customer)

        customers: List[Customer] = (
            query.limit(
                limit=limit,
            )
            .offset(offset_value)
            .all()
        )
        return customers

    def retrieve_customer_by_id(
        self,
        customer_id: int,
        session: Optional[Session] = None,
    ) -> Customer:
        is_session_created_here: bool = False
        if session is None:
            session = get_session()
            is_session_created_here = True

        try:
            customer: Optional[Customer] = (
                session.query(Customer)
                .filter(
                    Customer.id == customer_id,
                )
                .first()
            )
            if customer:
                return customer
            else:
                raise EntityNotFoundError("Customer not found!")
        finally:
            if is_session_created_here:
                session.close()

    @transaction
    def retrieve_customer_count(
        self,
        session: Session,
    ) -> int:
        return session.query(Customer).count()

    @transaction
    def retrieve_customer_id_by_phone_number(
        self,
        phone_number: str,
        session: Session,
    ) -> Optional[int]:
        return (
            session.query(Customer.id)
            .filter(Customer.phone_number == phone_number)
            .scalar()
        )

    @transaction
    def create_customer(
        self,
        first_name: str,
        last_name: Optional[str],
        phone_number: str,
        email: str,
        street: str,
        session: Session,
        special_notes: Optional[str] = None,
    ) -> Customer:
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            street=street,
            special_notes=special_notes,
        )
        session.add(customer)
        return customer

    @transaction
    def update_customer(
        self,
        customer_id: int,
        first_name: str,
        last_name: Optional[str],
        phone_number: str,
        email: str,
        street: str,
        session: Session,
        special_notes: Optional[str] = None,
    ) -> None:
        customer: Customer = self.retrieve_customer_by_id(
            customer_id=customer_id,
            session=session,
        )
        customer.first_name = first_name
        customer.last_name = last_name
        customer.phone_number = phone_number
        customer.email = email
        customer.street = street
        customer.special_notes = special_notes

    @transaction
    def delete_customer(
        self,
        customer_id: int,
        session: Session,
    ) -> None:
        customer: Customer = self.retrieve_customer_by_id(
            customer_id=customer_id,
            session=session,
        )
        session.delete(customer)
