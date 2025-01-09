
class HashT:
    """
    Section A - Develop a hash table, without using any additional libraries or classes:
    """
    
    def __init__(self, extent):
        """
        Initializes the hash table.
        
        Args:
            extent (int): The size of the hash table (number of "buckets").
        
        Time Complexity: O(n), where n is the size of the extent. 
                         This is because we are initializing an empty list for each bucket.
        Space Complexity: O(n), where n is the extent. The space is allocated for the empty buckets.
        """
        # Extent - Number of buckets in the hash table
        self.extent = extent
        # Size - Keeps track of the number of key-value pairs
        self.size = 0
        # Table - Internal list to hold the buckets
        self.table = []
        for i in range(extent):
            # Initialize each bucket as an empty list
            self.table.append([])
    
    def _get_hash(self, key):
        """
        Computes the hash for a given key using Python's built-in hash function and reduces it modulo the extent.
        
        Args:
            key: The key to hash.
        
        Time Complexity: O(1), as the hash computation and modulo operation are constant time operations.
        Space Complexity: O(1).
        """
        return (hash(key) % self.extent)

    def add(self, key, value):
        """
        Adds a key-value pair to the hash table. Handles collisions by appending to the bucket list. This will take a package object as its value which
        will include all these data components: 
            •   delivery address
            •   delivery deadline
            •   delivery city
            •   delivery zip code
            •   package weight
            •   delivery status (i.e., at the hub, en route, or delivered), including the delivery time
        
        Args:
            key: The key to add (package ID).
            value: The value to associate with the key (package object).
        
        Time Complexity: O(1) on average for inserting into the bucket. 
                         In the worst case, it's O(n) if there are many collisions and all keys hash to the same bucket.
        Space Complexity: O(1) for each individual key-value pair. O(n) total if we consider all key-value pairs.
        """
        # Compute the hash for the key
        key_hash = self._get_hash(key)
        key_value = [key, value]
        # Append the key-value pair to the appropriate bucket
        self.table[key_hash].append(key_value)
        # Increase the size counter to maintain accuracy
        self.size += 1

    def get(self, key):
        """
        Retrieves the value associated with a given key.
        
        Args:
            key: The key to search for.
        
        Returns:
            The value associated with the key, or None if the key does not exist.
        
        Time Complexity: O(1) on average (assuming good hash distribution). 
                         In the worst case (if all keys hash to the same bucket), it's O(n).
        Space Complexity: O(1).
        """
        key_hash = self._get_hash(key)
        if self.table[key_hash] is not None:
            # Search through the bucket
            for pair in self.table[key_hash]:
                if pair[0] == key:
                    # Return the value if the key matches otherwise return None
                    return pair[1]
        return None
    
    def get_size(self):
        """
        Returns the number of key-value pairs in the hash table.
        
        Time Complexity: O(1), since we are just returning the size attribute.
        Space Complexity: O(1).
        """
        return self.size

    def _get_all(self):
        """
        Retrieves all the values stored in the hash table.
        
        Returns:
            A list of all values.
        
        Time Complexity: O(n), where n is the number of key-value pairs.
                         This is because we need to iterate through all the buckets and collect the values.
        Space Complexity: O(n), where n is the number of key-value pairs.
        """
        all_Packages = []
        # Iterate through all the buckets and their contents
        for each in self.table:
            for package in each:
                # Append the value to the result list
                all_Packages.append(package[1])
        return all_Packages

    def delete(self, key):
        """
        Deletes a key-value pair from the hash table.
        
        Args:
            key: The key to remove.
        
        Returns:
            True if the key was successfully removed, False if the key was not found.
        
        Time Complexity: O(1) on average (assuming good hash distribution). 
                         Worst case is O(n) if there are many collisions in the same bucket.
        Space Complexity: O(1).
        """
        key_hash = self._get_hash(key)
        if self.table[key_hash] is None:
            # Key not found
            return False
        # Iterate through the bucket if key is found
        for i in range (0, self.size):
            if self.table[key_hash][i][0] == key:
                # Remove the key-value pair
                self.table[key_hash].pop(i)
                # Decrease the size counter to maintain accuracy
                self.size -= 1
                return True
            
    def print(self):
        """
        Prints the contents of the hash table.
        
        Time Complexity: O(n), where n is the number of key-value pairs, because we print every bucket.
        Space Complexity: O(1).
        """
        print('-----------------')
        for item in self.table:
            if item is not None:
                # Print each bucket's contents
                print(str(item))
        print('-----------------')