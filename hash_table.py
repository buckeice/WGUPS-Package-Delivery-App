import packages

"""
HashTable uses direct hashing with subtraction processing for keys. This ensures that packages 1-40 will
be inserted into the correct indices 0-39
"""


class HashTable:
    def __init__(self, num_packages):
        self.num_elements = 0
        self.list = [None] * num_packages
        self.size = len(self.list)

    def __get_hash_index(self, key):
        """
        Returns the index for the key by subtracting the key by 1
        :param key: The key to index
        :return: Returns the index
        """
        return int(key) - 1

    def add(self, key, value):
        """
        Method inserts data into hash table
        :param key: Key being inserted
        :param value: Data associated with key
        """
        hash_data = [key, value]
        hash_index = self.__get_hash_index(key)
        self.list[hash_index] = hash_data

    def get(self, key):
        """
        Returns data associated with a key
        :param key: The key to get data from
        :return: Returns the data
        """
        hash_index = self.__get_hash_index(key)

        if self.list[hash_index] is not None:
            data = self.list[hash_index]
            return data[1]
        return None

    def remove(self, key):
        """
        Removes the data at the key's hash index
        :param key: The key to delete
        """
        hash_index = self.__get_hash_index(key)

        if self.list[hash_index] is not None:
            self.list.pop(hash_index)
        return None

    def print(self):
        print('--ITEMS--')
        for item in self.list:
            print(str(item))

    # LOOKUP FUNCTIONS

    def lookup_address(self, package_id):
        """
        Gets the specified package's associated address by using the package ID as the search key in the hash table.
        :param package_id: The ID of the package to search. To be used as the key.
        :return: Returns the package's address
        """
        return packages.Package.get_address(self.get(package_id))
