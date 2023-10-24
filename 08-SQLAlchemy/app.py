import os
import pandas as pd

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, drop_database, create_database

from models.model import Product, Base, Customers, Order

from config.config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASSWORD, DATABASE_USERNAME

engine = create_engine(f"mysql+pymysql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}/{DATABASE_NAME}")

if database_exists(engine.url):
    drop_database(engine.url)

# Database creation
create_database(engine.url)
print("was it create? ", database_exists(engine.url))

# Tables creation
Base.metadata.create_all(engine)

products = {
    "Produit_1" :{
        "name": "Produit_1",
        "price": 100
    },
    "Produit_2": {
        "name": "Produit_2",
        "price": 200
    }
}

customers = {
    "Customer_1": {
        "name": "user_1",
        "email": "u1@u.fr"
    },
    "Customer_2": {
        "name": "user_2",
        "email": "u2@u.fr"
    }
}

orders = {
    "order_1": {
        "customerid": 1,
        "productid": 1
    },
    "order_2": {
        "customerid": 2,
        "productid": 2
    }
}

def print_query():
    result = session.query(
        Product.name,
        Product.price,
        Customers.name,
        Customers.email
    ).join(Order, Product.id == Order.product_id).join(
        Customers, Order.customer_id == Customers.id).all()

    df = pd.DataFrame(result, columns=['product_name','product_price','customer_name','customer_email'])
    print(df)

# INSERT
Session = sessionmaker(bind=engine)
with Session.begin() as session:
    for key, product in products.items():
        new_product = Product(name=product['name'], price=product['price'])
        session.add(new_product)

    for key, customer in customers.items():
        new_customer = Customers(name=customer['name'], email=customer['email'])
        session.add(new_customer)
        
    for key, order in orders.items():
        new_order = Order(product_id=order['customerid'], customer_id=order['productid'])
        session.add(new_order)

print_query()

# UPDATE
with Session.begin() as session:
    update_product = session.query(Product).filter_by(id=2).first()

    if update_product:
        update_product.price =500
        session.add(update_product)

print_query()

# DELETE
with Session.begin() as session:
    delete_order = session.query(Order).filter_by(id=2).first()

    if delete_order:
        session.delete(delete_order)

print_query()