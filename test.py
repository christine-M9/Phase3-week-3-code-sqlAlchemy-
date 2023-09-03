from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import unittest

# Create a SQLAlchemy engine to connect to an in-memory SQLite database
engine = create_engine('sqlite:///:memory:', echo=True)

# Create a session factory
SessionFactory = sessionmaker(bind=engine)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define your models
class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)

    # Define the relationship with reviews
    reviews = relationship("Review", back_populates="restaurant")
    customers = relationship("Customer", secondary="reviews", back_populates="restaurants")

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

    # Define the relationship with reviews
    reviews = relationship("Review", back_populates="customer")
    restaurants = relationship("Restaurant", secondary="reviews", back_populates="customers")

    def add_review(self, restaurant, rating):
        # Create a new review and add it to the session
        review = Review(restaurant=restaurant, customer=self, star_rating=rating)
        self.reviews.append(review)

    def delete_reviews(self, restaurant):
        # Delete all reviews for a given restaurant
        self.reviews = [review for review in self.reviews if review.restaurant != restaurant]

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'))
    customer_id = Column(Integer, ForeignKey('customers.id'))
    star_rating = Column(Integer)

    # Define the relationship with restaurant and customer
    restaurant = relationship("Restaurant", back_populates="reviews")
    customer = relationship("Customer", back_populates="reviews")

# Create the tables in the database
Base.metadata.create_all(engine)

# test examples.
class TestRestaurantReviewMethods(unittest.TestCase):

    def setUp(self):
        # Creating a new session for each test
        self.session = SessionFactory()

        # Creating some test data
        restaurant = Restaurant(name="Hilton Restaurant", price=1)
        customer = Customer(first_name="Christine", last_name="Juma")

        # Adding  the data to the session
        self.session.add(restaurant)
        self.session.add(customer)
        self.session.commit()

    def tearDown(self):
        # Closing the session after each test
        self.session.close()

    def test_add_review_for_customer(self):
        restaurant = self.session.query(Restaurant).filter_by(name="Hilton Restaurant").first()
        customer = self.session.query(Customer).filter_by(first_name="Christine").first()

        # Adding a review for the customer
        customer.add_review(restaurant, 4)

        # Verifying that the review has been added
        self.assertEqual(len(customer.reviews), 1)
        self.assertEqual(customer.reviews[0].star_rating, 4)

    def test_delete_review_for_customer(self):
        restaurant = self.session.query(Restaurant).filter_by(name="Hilton Restaurant").first()
        customer = self.session.query(Customer).filter_by(first_name="Christine").first()

        # Adding a review for the customer
        customer.add_review(restaurant, 4)

        # Deleting the review for the customer
        customer.delete_reviews(restaurant)

        # Verifying that the review has been deleted
        self.assertEqual(len(customer.reviews), 0)

if __name__ == '__main__':
    unittest.main()



