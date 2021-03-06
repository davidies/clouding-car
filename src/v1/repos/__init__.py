from typing import List
from ..models import Brand, Car, Customer, User

USER_TOKENS = []

BRANDS = [
    Brand(1, "Acura"),
    Brand(2, "Alfa Romeo"),
    Brand(3, "Bentley"),
    Brand(4, "BMW"),
    Brand(5, "Cadillac"),
    Brand(6, "Chevrolet"),
    Brand(7, "Dodge"),
    Brand(8, "Fiat"),
    Brand(9, "Ferrari"),
    Brand(10, "Hyundai")
]

CARS = [
    Car(1, "Integra", BRANDS[0]),
    Car(2, "Mito", BRANDS[1]),
    Car(3, "Continental", BRANDS[2]),
    Car(4, "Bentayga", BRANDS[2]),
    Car(5, "Serie 3", BRANDS[3]),
    Car(6, "Escalade", BRANDS[4]),
    Car(7, "Caprice Classic", BRANDS[5]),
    Car(8, "Suburban", BRANDS[5]),
    Car(9, "Venture", BRANDS[5]),
    Car(10, "Caravan", BRANDS[6]),
    Car(11, "Ram", BRANDS[6]),
    Car(12, "Ducato", BRANDS[7]),
    Car(13, "F-430", BRANDS[8]),
    Car(14, "Accent", BRANDS[9])
]

CUSTOMERS = [
    Customer(1, 'Moshe G Toney', [CARS[6]]),
    Customer(2, 'Kristine R Johnson', [CARS[0], CARS[2]]),
    Customer(3, 'Edmond H Castle', [CARS[1]]),
    Customer(4, 'Natasha H Turner', [CARS[3], CARS[8]]),
    Customer(5, 'Shannon R Mullins', CARS[5])
]

USERS = [
    User(1, 'donadoe', 'secretpassword', 'admin'),
    User(2, 'triticky', 'iamthebest', 'salesperson'),
    User(3, 'meberave', 'crazy4cars', 'mechanic')
]
