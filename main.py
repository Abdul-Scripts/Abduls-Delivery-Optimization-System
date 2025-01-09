from truck_class import Truck
from hashTable_class import HashT
from package_class import Package
from datetime import datetime, timedelta
import csv
import sys
import re

# Initialize the package ID's into three truck objects in accordance to the notes provided
truck1, truck2, truck3 = Truck(), Truck(), Truck()
# Truck 1 will have the packages with early deadlines as it will leave first
truck1 = ['1', '2', '40', '4', '7', '13', '15', '19', '29', '37', '34', '30', '20', '14', '16']
# Truck 2 will have the late packages
truck2 = ['3', '6', '18', '25', '31', '32', '36', '28', '38']
# Truck 3 will have the rest of the packages
truck3 = ['5', '11', '12', '9', '24', '17', '10', '8', '23', '26', '27', '33', '22', '35', '21', '39']
# Initialize hash table using the hash table class created
table = HashT(40)

# Used to calculate delivery time in route_knn()
def time_to_deliver(distance, speed):
    # Calculate the time (in hours) required to travel the given distance at the specified speed.
    return distance / speed

# Used to convert strings to datetime objects
def convert_to_time_object(time_str):
    # Convert a time string (e.g., '8:00:00') to a datetime object.
    return datetime.strptime(time_str, '%H:%M:%S')

# Validate time inputs by user
def validate_time_format(time_str):
    time_format = re.compile(r"^\d{2}:\d{2}:\d{2}$")  # Matches HH:MM:SS
    if time_format.match(time_str):
        try:
            # Further check if the time values are within valid ranges
            hours, minutes, seconds = map(int, time_str.split(":"))
            return 0 <= hours < 24 and 0 <= minutes < 60 and 0 <= seconds < 60
        except ValueError:
            return False
    return False

# Fills up the adjacency matrix that will be used to find the distances between different addresses
def fill_adjacency_matrix(filename):
    adjacency_matrix = []
    with open(filename, mode='r') as file:
        reader = csv.reader(file)   
        for row in reader:
            new_row = []
            for value in row:
                # Handle 'BLANK' as a string and numeric values as floats
                if value.strip() == 'BLANK':
                    new_row.append('BLANK')  # Keep as a string
                else:
                    try:
                        new_row.append(float(value))  # Convert to float
                    except ValueError:
                        new_row.append(value  )  # Keep as a string if conversion fails
            adjacency_matrix.append(new_row)
    return adjacency_matrix

def fill_hash_table(hash_table, package_file):
    with open(package_file, 'r') as file:
        next(file)  # Skip the header row
        for line in file:
            # Split the line into its respective fields
            data = line.strip().split(',')
            # Create a Package object using the data from the CSV
            package_id = int(data[0])
            package_object = Package([
                int(data[0]),  # Package ID
                data[1],       # Address
                data[2],       # City
                data[3],       # State
                data[4],       # Zip Code
                data[5],       # Delivery Deadline
                data[6],       # Weight
                data[7] if len(data) > 7 else None  # Note if provided
            ])
            # Add the Package object to the hash table using the package ID as the key
            hash_table.add(package_id, package_object)

# B.  Develop a look-up function that takes the package ID as input:
def lookup_package(package_id):
    """
    Section B - Looks up a package in the hash table by its package ID and prints its details in a presentable format.
    
    Args:
        package_id (int): The ID of the package to look up.
        
    Prints:
        The package details including:
        - delivery address
        - delivery deadline
        - delivery city
        - delivery zip code
        - package weight
        - delivery status
        - delivery time (if delivered, else None)
        
    Time Complexity:
        - Average Case: O(1) for hash table lookup and retrieving each attribute.
        - Worst Case: O(n) if there are hash collisions (searching through a bucket).
    Space Complexity: O(1) for retrieving and printing package details (no additional memory allocation).
    """
    # Retrieve the package using the package_id
    package = table.get(package_id)
    
    # If the package exists, print the details in a presentable format
    if package:
        print("\n------------------------------------------------------------------------------------------------\n")
        print(f"Package ID: {package_id}")
        print(f"Delivery Address: {package.get_address()}")
        print(f"City: {package.get_city()}")
        print(f"Zip Code: {package.get_zip()}")
        print(f"Delivery Deadline: {package.get_deadline()}")
        print(f"Package Weight: {package.get_weight()} lbs")
        print(f"Delivery Status: {package.get_status()}")
        
        # Check if the package has been delivered and print the delivery time if available
        if package.get_time_delivered():
            print(f"Delivery Time: {package.get_time_delivered()}")
        else:
            print("Delivery Time: Not delivered yet")
        
        print(f"Notes: {package.get_note()}")
        print("\n------------------------------------------------------------------------------------------------\n")

    else:
        # Print a message if the package is not found
        print("\n------------------------------------------------------------------------------------------------\n")
        print(f"Package ID {package_id} not found.")
        print("\n------------------------------------------------------------------------------------------------\n")

def route_knn(truck, leave_time):
    """
    Section C - FInds an optimized route for a given truck's package delivery using a K-nearest neighbor approach.

    Args:
        truck (list): A list of package IDs that are loaded on the truck. (initilized in the begininng)
        leave_time (str): The time the truck leaves the hub in the format 'HH:MM:SS'.

    Returns:
        dict: A dictionary containing:
            - 'route': A list of dictionaries representing the delivery order, with details such as package ID, address, delivery time, and distance.
            - 'total_distance': The total distance traveled by the truck.

    Time Complexity:
        - Preparing the route (for-loop over the truck): O(n), where n is the number of packages on the truck.
        - Main while loop (each package is visited once): O(n^2) due to nested iteration over the remaining packages.
        - Looking up addresses in the matrix: O(m) per lookup, where m is the number of locations in the matrix. If m is small compared to n, this could be considered O(1).
        
    Space Complexity:
        - Storing visited packages: O(n).
        - The route list: O(n).
        - The matrix lookups (since matrix is small, space complexity for matrix is considered negligible): O(m).
        - The route_log and distance (final output): O(n).
    """
    current_location = 'HUB (WGU)'  # Start at the hub
    total_distance = 0.00
    visited = set()  # Track visited locations
    route = []  # To store the packages' delivery order
    current_time = convert_to_time_object(leave_time)  # Start time for the truck
    route_log = []  # List to store the delivery details

    # Prepare the route with packages
    for package_id in truck:
        key = int(package_id)
        package = table.get(key)
        route.append(package)

    while route:
        nearest_distance = float('inf')
        nearest_package = None
        nearest_index = -1

        # Iterate through the undelivered packages
        for i, package in enumerate(route):
            if i in visited:
                continue

            address_zip = package.get_address_zip()

            # Find the index of the package address in the first column of the matrix
            try:
                destination_index = [row[0] for row in matrix].index(address_zip)
            except ValueError:
                print(f"Address {address_zip} not found in the distance matrix.")
                continue

            # Find the index of the current location (starting at the HUB)
            try:
                current_location_index = [row[0] for row in matrix].index(current_location)
            except ValueError:
                print(f"Current location {current_location} not found in the distance matrix.")
                break

            # Find the distance from the current location to this package's destination
            distance = matrix[current_location_index][destination_index]  # No need to convert to float again since we already did this in the fill function

            # Check if this package is the nearest unvisited package
            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package
                nearest_index = destination_index

        if nearest_package:
            # Update the current location to the nearest destination and accumulate the distance
            current_location = nearest_package.get_address_zip()
            total_distance += nearest_distance
            
            # Calculate travel time and update current time
            travel_time = time_to_deliver(nearest_distance, 18)  # 18 mph
            current_time += timedelta(hours=travel_time)
            delivery_time_str = current_time.strftime('%H:%M:%S')

            # Update package status and delivery time
            nearest_package.set_status("Delivered")
            nearest_package.set_time_delivered(delivery_time_str)  # Set the delivery time

            visited.add(nearest_index)

            # Log delivery details in the route log
            route_log.append({
                'package_id': nearest_package.get_id(),
                'address': nearest_package.get_address(),
                'delivery_time': delivery_time_str,
                'distance': nearest_distance
            })

            # Remove the delivered package from the route
            route.remove(nearest_package)

    # Return the delivery route and times
    return {
        'route': route_log,
        'total_distance': round(total_distance, 1)
    }

# print function for the previous route function
def print_delivery_details(routes, total_distance, time_of_completion):
    # Print header
    print("\n------------------------------------------------------------------------------------------------\n")
    print("Delivery Details:")

    # This will be used for calculated time elapsed from start to finish of entire route
    start_time = '8:00:00'
    time_of_completion_obj = datetime.strptime(time_of_completion, '%H:%M:%S')
    start_time_obj = datetime.strptime(start_time, '%H:%M:%S')
    time_difference = time_of_completion_obj - start_time_obj
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)    

    # Iterate through the routes for each truck
    for truck_index, truck_route in enumerate(routes):
        truck_name = f'Truck {truck_index + 1}'
        print(f"\n{truck_name} Route:\n~~~~~~~~~~~~~~\n")

        # Check status for each package in the route
        for package in truck_route['route']:
            package_id = package['package_id']
            address = package['address']
            delivery_time = package['delivery_time'] if package['delivery_time'] else 'Not Delivered'
            distance = package['distance']

            # Print the delivery status for this package
            print(f"Package ID: {package_id}, Address: {address}, "
                  f"Delivery Time: {delivery_time}, Distance: {distance}")
            
    print(f"\nTotal distance traveled by all trucks: {total_distance[0]+total_distance[1]+total_distance[2]} miles\nTime of completion for all packages: {time_of_completion} PM ({hours} HRS {minutes} MIN {seconds} SCD)")
    print("\n------------------------------------------------------------------------------------------------\n")


def status_check(routes, check_time, package_id=None):
    """
    Section D - Provide an intuitive interface for the user to view the delivery status
    """
    check_time_obj = datetime.strptime(check_time, '%H:%M:%S')
    total_mileage = 0.0  # To track total mileage for delivered packages
    package_statuses = []  # To store the status of all packages
    truck_mileage = 0.0  # Track mileage for the specific truck, when package_id is provided

    # Handling package 9 address adjustment
    cutoff_time = datetime.strptime('10:20:00', '%H:%M:%S')
    if check_time_obj >= cutoff_time:
        # Package 9 address corrected at 10:20:00
        table.get(9).set_address("410 S State St")
        table.get(9).set_city("Salt Lake City")
        table.get(9).set_state("UT")
        table.get(9).set_zip("84111")

    # Define departure times for each truck
    departure_times = {
        'truck1': datetime.strptime('08:00:00', '%H:%M:%S'),
        'truck2': datetime.strptime('09:10:00', '%H:%M:%S'),
        'truck3': datetime.strptime('10:30:00', '%H:%M:%S')
    }

    # Iterate through each truck's route
    for idx, route in enumerate(routes):
        route_mileage = 0.0  # Track mileage per route for delivered packages only
        truck_key = f'truck{idx + 1}'
        truck_print = f'truck {idx + 1}'

        # Check the delivery status of each package
        for delivery in route['route']:
            current_package_id = delivery['package_id']
            delivery_time_str = delivery['delivery_time']
            delivery_time_obj = datetime.strptime(delivery_time_str, '%H:%M:%S')
            
            # Determine package status based on check time and departure time
            departure_time = departure_times[truck_key]

            if check_time_obj < departure_time:
                package_status = "at hub"
            elif check_time_obj < delivery_time_obj:
                package_status = "en route"
            else:
                package_status = "delivered"
                route_mileage += delivery['distance']  # Add mileage only for delivered packages

            # Filter by package ID if provided
            if package_id is None or str(package_id) == str(current_package_id):
                # Update truck mileage for a specific package, if provided
                if package_id is not None and str(package_id) == str(current_package_id):
                    truck_mileage = route_mileage
                
                package_statuses.append({
                    'package_id': current_package_id,
                    'address': table.get(current_package_id).get_address(),
                    'city': table.get(current_package_id).get_city(),
                    'state': table.get(current_package_id).get_state(),
                    'zip': table.get(current_package_id).get_zip(),
                    'deadline': table.get(current_package_id).get_deadline(),
                    'truck': truck_print,
                    'status': package_status,
                    'delivery_time': delivery_time_str
                })

        total_mileage += route_mileage  # Add only the mileage for delivered packages in this route

    # Sort packages by ID for better readability when no specific package ID is given
    package_statuses.sort(key=lambda x: int(x['package_id']))

    # Print package statuses
    print(f"\n------------------------------------------------------------------------------------------------\n\nAt {check_time}:\n")
    for package in package_statuses:
        print(f"Package {package['package_id']} to {package['address']}, {package['city']}, {package['state']}, {package['zip']} "
              f"with deadline {package['deadline']} is {package['status']} on {package['truck']}.")
        if package['status'] == "delivered":
            print(f"-- Delivery time: {package['delivery_time']}")
        else:
            print("-- Delivery time: N/A")
    
    # If package ID was provided, only show truck mileage for that package's truck
    if package_id is not None:
        print(f"\nTotal mileage traveled by {package_statuses[0]['truck']} by this point in time: {round(truck_mileage, 1)} miles.")
    else:
        # Print the total mileage for all trucks
        print(f"\nTotal mileage traveled by all trucks by this point in time: {round(total_mileage, 1)} miles.")
    
    print("\n------------------------------------------------------------------------------------------------\n")

def calculate_time_of_completion(routes):
    latest_time = None
    
    # Iterate through each truck's route
    for route in routes:
        for delivery in route['route']:
            delivery_time_str = delivery['delivery_time']
            delivery_time_obj = datetime.strptime(delivery_time_str, '%H:%M:%S')
            
            # Update the latest delivery time
            if latest_time is None or delivery_time_obj > latest_time:
                latest_time = delivery_time_obj
    
    # Return the latest delivery time as a string
    return latest_time.strftime('%H:%M:%S')

def main_menu():
    print("\n------------------------------------------------------------------------------------------------\n")
    print("Welcome to the WGUPS Delivery System!\n")
    print("Select an option:")
    print("1. Lookup package")
    print("2. Check package statuses and details at a specific time")
    print("3. Print delivery routes and details")
    print("4. Exit")
    print("\n------------------------------------------------------------------------------------------------\n")
    choice = input("\nEnter your choice (1-4): ")

    if choice == '1':
        package_id = input("\nEnter the package ID: ")
        lookup_package(int(package_id))
    elif choice == '2':
        # Time input validation loop
        while True:
            check_time = input("\nEnter the time to check status (HH:MM:SS): ")
            if validate_time_format(check_time):
                break
            else:
                print("\nInvalid time format. Please enter time in HH:MM:SS format.")

        # Package ID validation loop
        while True:
            package_id = input("\nEnter package ID (leave blank for all packages): ")
            
            # If the user leaves it blank, call status_check for all packages
            if not package_id.strip():
                status_check(combined_routes, check_time)
                break  # Exit the loop
            
            try:
                # Convert package_id to int and check if it’s within valid range
                package_id = int(package_id)
                if 1 <= package_id <= 40:  # Assuming valid package IDs are between 1 and 40
                    status_check(combined_routes, check_time, package_id=package_id)
                    break  # Exit the loop once valid ID is entered
                else:
                    print("\nInvalid package ID. Please enter a number between 1 and 40.")
            except ValueError:
                print("\nInvalid input. Please enter a valid numeric package ID.")
    elif choice == '3':
        print_delivery_details(combined_routes, total_distance, time_of_completion)
    elif choice == '4':
        print("\nExiting... Goodbye!")
        sys.exit()
    else:
        print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    # Setting up the prerequisites before running the CLI
    fill_hash_table(table, 'WGUPS_package_file.csv')
    matrix = fill_adjacency_matrix('WGUPS_distance_table.csv')

    # Truck 1 leaving at 8:00:00
    route1 = route_knn(truck1, '8:00:00')
    # Truck 2 leaving at 9:10:00
    route2 = route_knn(truck2, '9:10:00')
    # Truck 3 leaving at 10:30:00 with Package 9
    route3 = route_knn(truck3, '10:30:00')

    # Combined route, will be used for status check
    combined_routes = [route1, route2, route3]
    total_distance = [route1['total_distance'], route2['total_distance'], route3['total_distance']]

    # Calculate the time of completion without printing
    time_of_completion = calculate_time_of_completion(combined_routes)

    while True:
        # Run CLI
        main_menu()