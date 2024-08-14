# Simple Recommendation System

## Overview
This project implements a simple recommendation system which consists of two services:
- **Generator system**: Generates random recommendations based on a given model name.
- **Invoker system**: Retrieves and caches recommendations, making parallel calls to the Generator service.

## Caching
To optimize the performance of the recommendation system, two levels of caching have been implemented:
- **Local Cache (In-Memory Cache)**
This cache has a Time-to-Live (TTL) of 10 seconds and is limited to storing up to 3 keys at any given time. 
- **Redis Cache**
Redis is an in-memory data store that allows fast access to cached data and is particularly well-suited for handling larger datasets and high traffic scenarios. 

## Setup Instructions

### Prerequisites
- Docker
- Docker Compose

### How to Run
1. Clone the repository.
2. Navigate to the project directory.
3. Run the following command to build and start the services:
   ```bash
   docker-compose up
