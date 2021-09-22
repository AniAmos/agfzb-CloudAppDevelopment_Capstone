from django.db import models
from django.utils.timezone import now
from django.conf import settings
import uuid
import sys

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False,max_length=1000)
    description = models.CharField(max_length=3000)
    def __str__(self):
        return "Name: " + self.name + ", " + \
               "Description: " + self.description

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    carmake = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(null=False,max_length=1000)
    dealer_id = models.IntegerField()
    SEDAN = 'sedan'
    SUV = 'SUV'
    WAGON = 'wagon'
    HATCHBACK = 'hatchback'
    type_choices = [(SEDAN, 'Sedan'),(SUV, 'SUV'),(WAGON, 'Wagon'),(HATCHBACK, 'Hatchback')]
    car_type = models.CharField(null=False,choices=type_choices,max_length=1000)
    year = models.DateField()
    def __str__(self):
        return "Name: " + self.name + ", " + "Type: " + self.car_type + ', ' + 'Year: ' + str(self.year)

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip
    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, car_make, car_model, car_year, dealership, name, purchase, purchase_date, review, sentiment):
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.purchase_date = purchase_date
        self.review = review
        self.sentiment = sentiment
    def __str__(self):
        return "Name: " + self.name