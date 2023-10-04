# Student ID: 001500780
# Name: Samuel Buck

import csv
import truck
import hash_table
import packages
import datetime
from datetime import date

# Puts provided distance CSV content into a list
with open("WGUPSDistanceTable.csv") as distance_csv:
    reader = csv.reader(distance_csv)
    distance_list = list(reader)

# Puts provided package CSV content into a list
with open('WGUPSPackageFile.csv') as package_csv:
    reader = csv.reader(package_csv)
    package_list = list(reader)


# Used to find the distance between two vertices
# Complexity: Space O(1), Time O(1)
def find_distance(x, y):
    distance = distance_list[x][y + 2]
    if distance == '':
        reversed_distance = distance_list[y][x + 2]
        return float(reversed_distance)
    else:
        return distance


# Used to find the address' index in the distance table list
# Complexity: Space O(n), Time O(n)
def find_index_from_address(address):
    index = -1
    for list_row in distance_list:
        index += 1
        if address in list_row[1]:
            return index


# Adds a list of packages to a specified hash table
# Complexity: Space O(n), Time O(n)
def load_package_list_to_table(p_list, h_table):
    for package in p_list:
        new_package = packages.Package(package[0], package[1], package[2], package[3], package[4], package[5],
                                       package[6], package[7])
        h_table.add(package[0], new_package)


# Initializing truck objects
truck_1 = truck.Truck(0.0, [1, 13, 15, 14, 16, 19, 20, 34, 40, 30, 31, 4, 25, 7, 29], '4001 South 700 East',
                      datetime.datetime(date.today().year, date.today().month, date.today().day, 8, 0), 1)

truck_2 = truck.Truck(0.0, [3, 18, 36, 38, 6, 28, 32, 2, 10, 21, 22, 23, 24, 26, 37], '4001 South 700 East',
                      datetime.datetime(date.today().year, date.today().month, date.today().day, 9, 5), 2)

truck_3 = truck.Truck(0.0, [9, 17, 11, 12, 33, 35, 5, 39, 27, 8], '4001 South 700 East',
                      datetime.datetime(date.today().year, date.today().month, date.today().day, 10, 20), 3)

# Creating hash table
package_table = hash_table.HashTable(40)

# Inserts packages into hash table
load_package_list_to_table(package_list, package_table)


# Uses the nearest neighbor algorithm to order and deliver packages in a truck
# Complexity: Space O(n), Time O(n^2)
def nearest_neighbor(truck):
    # Creates a list to hold package objects that have not been delivered
    undelivered_packages = []

    # Gets truck start time to be used when updating package status
    truck_start = truck.current_time

    # Uses package IDs from truck to get the package object from the package hash table
    for p_id in truck.starting_packages:
        package = package_table.get(p_id)
        undelivered_packages.append(package)

    while len(undelivered_packages) >= 0:
        # Sets the initial next location distance higher than possible to ensure the algorithm can run
        distance_next_location = 999
        current_package = None

        # Returns the truck to WGU when packages are delivered, calculating distance and time
        if len(undelivered_packages) == 0:
            distance_to_wgu = float(find_distance(find_index_from_address(truck.current_location), 0))
            truck.mileage = truck.mileage + distance_to_wgu
            time_delta = datetime.timedelta(hours=(distance_to_wgu / truck.speed))
            truck.current_time = truck.current_time + time_delta
            truck.current_location = '4001 South 700 East'
            return
        else:
            for package in undelivered_packages:
                # Checks if package 9 is ready for its updated address
                if (package.package_id == 9 and truck.current_time >
                        datetime.datetime(date.today().year, date.today().month, date.today().day, 10, 20)):
                    package.address = '410 S. State St.'
                # Sets the distance between trucks current location and package address
                distance = float(find_distance(find_index_from_address(truck.current_location),
                                               find_index_from_address(package.address)))
                if distance <= distance_next_location:
                    distance_next_location = distance
                    current_package = package

            # The package added to the package list has its status changed to 'DELIVERED'
            # The package is also associated with a truck by the current truck's number
            current_package.status = 'DELIVERED'
            current_package.truck = truck.truck_number

            # Changes truck's time
            time_delta = datetime.timedelta(hours=(distance_next_location / truck.speed))
            truck.current_time = truck.current_time + time_delta

            # Adds the start and delivery times for a package
            current_package.left_hub = truck_start
            current_package.delivery_time = truck.current_time

            # Adds next package to the package list and removes the package from the undelivered list
            truck.packages.append(current_package)
            undelivered_packages.remove(current_package)

            # Calculates the sum of current mileage and distance of next location
            truck.mileage += distance_next_location

            # Changes the truck's current location to the next package's address
            truck.change_location(current_package.address)


# Sends the trucks on their routes using the nearest neighbor algorithm
nearest_neighbor(truck_1)
nearest_neighbor(truck_2)
nearest_neighbor(truck_3)

# Combines all delivered packages into a single list
ultimate_package_list = truck_1.packages + truck_2.packages + truck_3.packages

# Uses Python sort() to sort the list by package ID, which uses the Timsort algorithm and has the following complexities
# Complexity: Space O(n), Time O(n log n)
ultimate_package_list.sort(key=lambda x: int(x.package_id))

# Adds the mileage of the trucks to the total mileage
total_mileage = truck_1.mileage + truck_2.mileage + truck_3.mileage

# USER INTERFACE
print('WGUPS ROUTING PROGRAM')
print('TOTAL MILEAGE IS: ' + str(round(total_mileage, 2)))
print('TO SEE THE STATUS OF ALL PACKAGES TYPE "1", TO SEE STATUS OF INDIVIDUAL PACKAGES TYPE "2"')
user_input = input('INPUT: ')

# INTERFACE FOR ALL PACKAGES
# Complexity: Space O(n), Time O(n)
if user_input == '1':
    print('PLEASE TYPE A TIME IN THE FORMAT OF HH:MM')
    user_time_input = input('INPUT: ')
    try:
        (hour, minute) = user_time_input.split(':')
        user_datetime = datetime.datetime(date.today().year, date.today().month, date.today().day,
                                          int(hour), int(minute))
    except ValueError:
        print('TIME INVALID')
        exit()

    for package in ultimate_package_list:
        if package.delivery_time > user_datetime:
            package.status = 'EN ROUTE'

        if package.left_hub > user_datetime:
            package.status = 'AT HUB'

        if package.delivery_time > user_datetime:
            package.delivery_time_string = 'NOT DELIVERED'
        else:
            package.delivery_time_string = str(package.delivery_time)

    for package in ultimate_package_list:
        p_id = package.package_id
        address = package.address
        deadline = package.delivery_deadline
        status = package.status
        left_hub = package.left_hub
        delivery = package.delivery_time_string
        truck_num = package.truck
        city = package.city
        weight = package.weight_kilo
        zip = package.zipcode
        string_id = str(p_id)
        string_destination = str(address)
        string_deadline = str(deadline)
        string_status = str(status)
        string_truck = str(truck_num)
        string_delivery = str(delivery)

        print('ID: ' + string_id.ljust(10) + 'ON TRUCK: ' + string_truck.ljust(10) + 'DESTINATION: ' +
              string_destination.ljust(45) + 'CITY: ' + city.ljust(20) + 'WEIGHT: ' + str(weight).ljust(5) + 'ZIP: '
              + str(zip).ljust(15) + 'DEADLINE: ' + string_deadline.ljust(20) + 'STATUS: ' +
              string_status.ljust(20) + 'TIME OF DELIVERY: ' + string_delivery)

# INTERFACE FOR INDIVIDUAL PACKAGE
# Complexity: Space O(n), Time O(n)
if user_input == '2':
    print('PLEASE TYPE A PACKAGE ID')
    user_id_input = input('INPUT: ')

    try:
        if int(user_id_input) <= 0 or int(user_id_input) > len(ultimate_package_list):
            print('INVALID PACKAGE ID')
            exit()
    except ValueError:
        print('INVALID PACKAGE ID')
        exit()

    print('PLEASE TYPE A TIME IN THE FORMAT OF HH:MM')
    user_time_input = input('INPUT: ')

    try:
        (hour, minute) = user_time_input.split(':')
        user_datetime = datetime.datetime(date.today().year, date.today().month, date.today().day,
                                          int(hour), int(minute))
    except ValueError:
        print('TIME INVALID')
        exit()

    for package in ultimate_package_list:
        if int(package.package_id) == int(user_id_input):
            if package.delivery_time > user_datetime:
                package.status = 'EN ROUTE'

            if package.left_hub > user_datetime:
                package.status = 'AT HUB'

            if package.delivery_time > user_datetime:
                package.delivery_time_string = 'NOT DELIVERED'
            else:
                package.delivery_time_string = str(package.delivery_time)

            found_package = package

            p_id = found_package.package_id
            address = found_package.address
            deadline = found_package.delivery_deadline
            status = found_package.status
            left_hub = found_package.left_hub
            delivery = found_package.delivery_time_string
            truck_num = package.truck
            city = found_package.city
            weight = found_package.weight_kilo
            zip = found_package.zipcode
            string_id = str(p_id)
            string_destination = str(address)
            string_deadline = str(deadline)
            string_status = str(status)
            string_truck = str(truck_num)
            string_delivery = str(delivery)

            print('ID: ' + string_id.ljust(10) + 'ON TRUCK: ' + string_truck.ljust(10) + 'DESTINATION: ' +
                  string_destination.ljust(45) + 'CITY: ' + city.ljust(20) + 'WEIGHT: ' + str(weight).ljust(
                5) + 'ZIP: ' + str(zip).ljust(15) + 'DEADLINE: ' + string_deadline.ljust(20) + 'STATUS: ' +
                  string_status.ljust(20) + 'TIME OF DELIVERY: ' + string_delivery)

# Quits the application if user does not type 1 or 2
if user_input != '1' or '2':
    quit()
