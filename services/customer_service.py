from typing import List, Optional

from sqlalchemy.orm import Session

from common.exceptions.entity_not_found_exception import EntityNotFoundException
from database.connector import get_session
from models.customer import Customer


class CustomerService:

    def retrieve_customers(
        self,
        limit: int,
        page: int,
        session: Session = get_session(),
    ) -> List[Customer]:
        offset_value = (page - 1) * limit

        customers: List[Customer] = (
            session.query(Customer)
            .limit(
                limit=limit,
            )
            .offset(offset_value)
            .all()
        )
        return customers

    def retrieve_customer_by_id(
        self,
        customer_id: int,
        session: Session = get_session(),
    ) -> Customer:
        customer: Optional[Customer] = (
            session.query(Customer).filter(Customer.id == customer_id).first()
        )
        if customer:
            return customer
        else:
            raise EntityNotFoundException("Customer not found!")

    def retrieve_customer_count(
        self,
        session: Session = get_session(),
    ) -> int:
        return session.query(Customer).count()

    def create_customer(
        self,
        first_name: str,
        last_name: Optional[str],
        phone_number: str,
        email: str,
        street: str,
        special_notes: Optional[str],
        session: Session = get_session(),
    ) -> None:
        customer = Customer(
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            email=email,
            street=street,
            special_notes=special_notes,
        )
        session.add(customer)
        session.commit()
        session.close()

    def update_customer(
        self,
        customer_id: int,
        first_name: str,
        last_name: Optional[str],
        phone_number: str,
        email: str,
        street: str,
        special_notes: Optional[str],
        session: Session = get_session(),
    ) -> None:
        customer: Optional[Customer] = self.retrieve_customer_by_id(
            customer_id=customer_id,
            session=session,
        )
        if customer:
            customer.first_name = first_name
            customer.last_name = last_name
            customer.phone_number = phone_number
            customer.email = email
            customer.street = street
            customer.special_notes = special_notes
            session.commit()
            session.close()
        else:
            raise EntityNotFoundException("Customer not found!")

    def delete_customer(
        self,
        customer_id: int,
        session: Session = get_session(),
    ) -> None:
        customer: Optional[Customer] = self.retrieve_customer_by_id(
            customer_id=customer_id,
            session=session,
        )
        if customer:
            session.delete(customer)
            session.commit()
            session.close()
        else:
            raise EntityNotFoundException("Customer not found!")
