# This file contains classes related to package objects
class Package:
    def __init__(self, package_id, address, city, state, zipcode, delivery_deadline,
                 weight_kilo, note, status='AT HUB'):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zipcode = zipcode
        self.delivery_deadline = delivery_deadline
        self.weight_kilo = weight_kilo
        self.note = note
        self.status = status
        self.left_hub = None
        self.delivery_time = None
        self.truck = None

    def get_id(self):
        return self.package_id

    def get_address(self):
        return self.address

    def get_city(self):
        return self.city

    def get_state(self):
        return self.state

    def get_zipcode(self):
        return self.zipcode

    def get_deadline(self):
        return self.delivery_deadline

    def get_weight(self):
        return self.weight_kilo

    def get_note(self):
        return self.note

    def get_status(self):
        return self.status

class PackageList:
    def __init__(self):
        self.list = []

    def add_package(self, package):
        self.list.append(package)
