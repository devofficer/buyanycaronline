from datetime import datetime, timedelta

from models.vehicle_model import Car
from common.utils import IDGenerator
timestamp = 1620907226.34748
dt_object = datetime.fromtimestamp(timestamp)

print("dt_object =", dt_object)
print("type(dt_object) =", type(dt_object))

date_and_time = datetime.now()
print(date_and_time)


time_change = timedelta(minutes=5)
new_time = datetime.now() + timedelta(minutes=5)

print(new_time.timestamp())

now = datetime.now()

print(IDGenerator.generate_ID())

car = Car()
carDict = car.__dict__

print(car)