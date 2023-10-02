# This file contains the Truck class
class Truck:
    def __init__(self, mileage, starting_packages, current_location, current_time, truck_number, package_limit=16, speed=18):
        self.mileage = mileage
        self.starting_packages = starting_packages[:package_limit]
        self.current_location = current_location
        self.current_time = current_time
        self.package_limit = package_limit
        self.speed = speed
        self.packages = []
        self.truck_number = truck_number

    def change_location(self, address):
        self.current_location = address
