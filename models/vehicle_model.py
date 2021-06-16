from models.advertisement_model import Advertisement


class Vehicle(Advertisement):
    def __init__(self, adType: int = -1, owner: str = "", title: str = "", price: int = 0, decription: str = "",
                 make: int = 0, model: int = 0, features: list = [""], cylinder: int = 0, year: int = 0,
                 condition: int = 0, fuel: int = 0, color: str = "", warranty: bool = False, images: list = []):
        super().__init__(adType=adType,title=title, price=price, decription=decription, owner=owner)
        self.__make = make
        self.__model = model
        self.__features = features
        self.__color = color
        self.__cylinders = cylinder
        self.__year = year
        self.__condition = condition
        self.__fuelType = fuel
        self.__warranty = warranty
        self.__images = images

    def get_images(self):
        return self.__images

    def set_images(self, images: []):
        self.__images = images

    def get_color(self):
        return self.__color

    def set_color(self, val: str):
        self.__color = val

    def get_make(self):
        return self.__make

    def set_make(self, val: int):
        self.__make = val

    def get_model(self):
        return self.__model

    def set_model(self, val: int):
        self.__model = val

    def get_features(self):
        return self.__features

    def set_features(self, val: list):
        self.__features = val

    def get_cylinder(self):
        return self.__cylinders

    def set_cylinder(self, val: int):
        self.__cylinders = val

    def get_year(self):
        return self.__year

    def set_year(self, val: int):
        self.__year = val

    def get_condition(self):
        return self.__condition

    def set_condition(self, val: bool):
        self.__condition = val

    def get_fuelType(self):
        return self.__fuelType

    def set_fuelType(self, val: bool):
        self.__fuelType = val

    def get_warranty(self):
        return self.__warranty

    def set_warranty(self, val: bool):
        self.__warranty = val


class Car(Vehicle):
    def __init__(self, adType: int = -1, owner: str = "", title: str = "", price: int = 0, decription: str = "",
                 make: int = 0, model: int = 0, features: list = [""], cylinder: int = 0, year: int = 0,
                 condition: bool = False, fuel: int = 0, warranty: bool = False, region: int = 0,
                 distance: int = 0, body_type: int = 0, doors: int = 0,
                 trans: bool = False, hp: int = 0, color: str = ""):
        super().__init__(adType=adType, title=title, price=price, decription=decription,
                         make=make, owner=owner, model=model, features=features, cylinder=cylinder, year=year,
                         condition=condition, fuel=fuel, warranty=warranty, color=color)
        self.__region = region
        self.__distance = distance
        self.__bodyType = body_type
        self.__numOfDoors = doors
        self.__transmission = trans
        self.__hp = hp

    def get_region(self):
        return self.__region

    def set_region(self, val: str):
        self.__region = val

    def get_distance(self):
        return self.__distance

    def set_distance(self, val: int):
        self.__distance = val

    def get_body_type(self):
        return self.__bodyType

    def set_body_type(self, val: int):
        self.__bodyType = val

    def get_num_of_doors(self):
        return self.__numOfDoors

    def set_num_of_doors(self, val: int):
        self.__numOfDoors = val

    def get_transmission(self):
        return self.__transmission

    def set_transmission(self, val: bool):
        self.__transmission = val

    def get_hp(self):
        return self.__hp

    def set_hp(self, val: int):
        self.__hp = val


class HeavyVehicle(Vehicle):
    def __init__(self, adType: int = -1, owner: str = "", title: str = "", price: int = 0, decription: str = "",
                 make: int = 0, model: int = 0, features=None, cylinder: int = 0, year: int = 0,
                 condition: bool = False, fuel: bool = True, warranty: bool = False, distance: int = 0, hours: int = 0,
                 heavyType: int = 0, color: str = ""):
        super().__init__(adType=adType, title=title, price=price, decription=decription, owner=owner,
                         make=make, model=model, features=features, cylinder=cylinder, year=year,
                         condition=condition, fuel=fuel, warranty=warranty, color=color)
        self.__distance = distance
        self.__hours = hours
        self.__heavyType = heavyType

    def get_distance(self):
        return self.__distance

    def set_distance(self, val: int):
        self.__distance = val

    def get_hours(self):
        return self.__hours

    def set_hours(self, val: int):
        self.__hours = val

    def get_heavy_type(self):
        return self.__heavyType

    def set_heavy_type(self, val: int):
        self.__heavyType = val


class MotorCycle(Vehicle):
    def __init__(self, adType: int = -1, owner: str = "", title: str = "", price: int = 0, decription: str = "",
                 make: int = 0, model: int = 0, color: str = "", features: list = [""], cylinder: int = 0,
                 year: int = 0, condition: bool = False, fuel: bool = True, warranty: bool = False,
                 engine_size: int = 0, hours: int = 0):
        super().__init__(adType=adType, title=title, price=price, decription=decription, owner=owner,
                         make=make, model=model, features=features, cylinder=cylinder, year=year,
                         condition=condition, fuel=fuel, warranty=warranty, color=color)
        self.__engineSize = engine_size
        self.__hours = hours


class Boat(Vehicle):
    def __init__(self, adType: int = -1, owner: str = "", title: str = "", price: int = 0, decription: str = "",
                 make: int = 0, model: int = 0, color: str = "", features: list = [""], cylinder: int = 0,
                 year: int = 0, condition: bool = False, fuel: bool = True, warranty: bool = False, length: int = 0,
                 typed: int = 0, sub_type: int = 0, hours: int = 0):
        super().__init__(adType=adType, title=title, price=price, decription=decription, owner=owner,
                         make=make, model=model, features=features, cylinder=cylinder, year=year,
                         condition=condition, fuel=fuel, warranty=warranty, color=color)
        self.__length = length
        self.__type = typed
        self.__subType = sub_type
        self.hours = hours

