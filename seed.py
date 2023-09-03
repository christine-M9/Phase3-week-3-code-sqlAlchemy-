from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Restaurant, Customer, Review
from faker import Faker 

# Creating an SQLite database engine
engine = create_engine('sqlite:///database.db')

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()

# Initialize Faker
fake = Faker()

# Creating some fake restaurants
for _ in range(5):
    restaurant = Restaurant(name=fake.company(), price=fake.random_int(min=1, max=5))
    session.add(restaurant)

# Creating some fake customers
for _ in range(10):
    customer = Customer(first_name=fake.first_name(), last_name=fake.last_name())
    session.add(customer)

# Creating some fake reviews
for _ in range(20):
    review = Review(star_rating=fake.random_int(min=1, max=5),
                    restaurant=fake.random_element(elements=session.query(Restaurant).all()),
                    customer=fake.random_element(elements=session.query(Customer).all()))
    session.add(review)

# Committing the changes to the database
session.commit()

# Closing the session
session.close()

