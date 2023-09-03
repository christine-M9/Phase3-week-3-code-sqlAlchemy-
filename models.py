from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///my_database.db')
Session = sessionmaker(bind=engine)

class Restaurant(Base):
    __tablename__ = 'restaurants'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    reviews = relationship('Review', back_populates='restaurant')
    customers = relationship('Customer', secondary='reviews', back_populates='restaurants')

    @classmethod
    def fanciest(cls):
        return session.query(cls).order_by(cls.price.desc()).first()

    def all_reviews(self):
        return [f"Review for {self.name} by {customer.full_name()}: {review.star_rating} stars." for review in self.reviews]

    def reviews(self):
        return [review for review in self.reviews]

    def customers(self):
        return [customer for customer in self.customers]

class Customer(Base):
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)

    reviews = relationship('Review', back_populates='customer')
    restaurants = relationship('Restaurant', secondary='reviews', back_populates='customers')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def favorite_restaurant(self):
        return session.query(Restaurant).filter(
            Restaurant.reviews.any(customer=self)
        ).order_by(Restaurant.price.desc()).first()

    def add_review(self, restaurant, rating):
        review = Review(star_rating=rating, restaurant=restaurant, customer=self)
        session.add(review)

    def delete_reviews(self, restaurant):
        session.query(Review).filter(Review.restaurant == restaurant, Review.customer == self).delete()

    def reviews(self):
        return [review for review in self.reviews]

    def restaurants(self):
        return [restaurant for restaurant in self.restaurants]

class Review(Base):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    star_rating = Column(Integer, nullable=False)
    restaurant_id = Column(Integer, ForeignKey('restaurants.id'), nullable=False)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)

    restaurant = relationship('Restaurant', back_populates='reviews')
    customer = relationship('Customer', back_populates='reviews')

    def full_review(self):
        return f"Review for {self.restaurant.name} by {self.customer.full_name()}: {self.star_rating} stars."

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    Session().close()
