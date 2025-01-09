# UPS Delivery Optimization System

## Overview
This was final assignment for a DSA2 class at WGU. This project is a package delivery optimization system designed to minimize the total mileage for trucks while ensuring all packages are delivered by their specified deadlines. The system models a delivery scenario with constraints such as limited truck capacity, time-sensitive deliveries, and dynamically updated delivery requirements.

## Problem Statement
UPS aims to optimize the delivery routes for its Daily Local Deliveries (DLD) in Salt Lake City. The solution must:
- Deliver all packages on time.
- Minimize total mileage for all trucks.
- Handle dynamically updated package details, such as address corrections.
- Provide real-time updates on truck and package status.

## Key Features
- **Route Optimization**: Implements the k-nearest-neighbor (KNN) algorithm to calculate efficient delivery routes.
- **Dynamic Address Updates**: Supports mid-route updates, such as correcting the delivery address for a package.
- **Real-Time Status Tracking**: Tracks package and truck statuses, including time of delivery, truck mileage, and delivery completion.
- **Scalable Design**: Designed for adaptability to other cities and delivery scenarios.

## Assumptions
1. Each truck can carry up to 16 packages.
2. Trucks travel at an average speed of 18 miles per hour.
3. Trucks can return to the hub to reload packages if needed.
4. Deliveries are instantaneous, with time accounted for in the travel speed.
5. Package #9 has a corrected address available at 10:20 a.m.
6. Delivery day starts at 8:00 a.m. and ends when all packages are delivered.

## Inputs
- **Package File**: A CSV file containing package details, including ID, address, city, state, zip, deadline, weight, and special notes.
- **Distance Table**: A CSV file containing distances between delivery locations.

## Outputs
- Optimized routes for each truck.
- Delivery schedule with timestamps for each package.
- Total mileage for all trucks.
- Status updates for packages and trucks.

## Solution Approach
1. **Data Preparation**: Parses input files and prepares a distance adjacency matrix.
2. **Algorithm Design**: Utilizes the k-nearest-neighbor algorithm to iteratively select the next closest delivery location.
3. **Dynamic Handling**: Incorporates constraints like address corrections and time-sensitive deliveries.
4. **Tracking and Reporting**: Provides real-time updates on delivery progress and overall performance metrics.

## Usage
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd ups-delivery-optimizer
   ```
2. Place the `Package File` and `Distance Table` CSV files in the `data/` directory.
3. Run the program:
   ```bash
   python main.py
   ```
4. Follow the CLI instructions to view real-time delivery updates and performance metrics.

## Technology Stack
- **Programming Language**: Python
- **Algorithm**: K-Nearest-Neighbor (KNN)
- **Data Structures**: Custom hash table for package management, adjacency matrix for distance data

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.


