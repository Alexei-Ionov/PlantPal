# Plant Pal 🌱

**Plant Pal** is a full-stack web application designed to help users monitor and care for their plants. By synchronizing an ESP32 device with a soil moisture sensor, Plant Pal enables real-time moisture level monitoring, providing users with personalized insights and automated reminders for plant care.

## Key Features

- **Real-Time Moisture Monitoring**: Sync an ESP32 microcontroller to send live soil moisture readings from a sensor in your plant’s pot. Data is stored and processed through the backend, enabling users to track and monitor their plants’ health.
  
- **Fast Search Engine for Plants**: Plant Pal features an optimized search engine that allows users to quickly search and select from a database of over 400,000 plants. The trie-based data structure provides instant suggestions, helping users efficiently find plants and access relevant data.

- **Custom Watering Schedule Integration**: Plant Pal leverages the Google Calendar API to create personalized watering schedules for each plant based on its ideal moisture levels. With just one click, users can receive reminders directly in their Google Calendar, helping them stay on top of plant care.

## Project Architecture

- **Backend**: Built with Flask, the backend handles data storage, real-time updates, and API integration. It receives POST requests from the ESP32, parses incoming moisture data, and sends relevant information to the frontend.
  
- **Frontend**: A React application that provides an intuitive user interface for interacting with Plant Pal. Users can connect their ESP32 device, view moisture data in real-time, and manage plant care schedules easily.
  
- **ESP32 Integration**: The ESP32 device, acting as its own server, collects and sends real-time soil moisture data to the backend with a unique token provided during the connection process. This ensures data integrity and user-specific updates.

## Tech Stack

- **Frontend**: React
- **Backend**: Flask (Python)
- **Database**: PostgreSQL for data persistence
- **Hardware**: ESP32 microcontroller with a soil moisture sensor
- **APIs**:
  - [Google Calendar API](https://developers.google.com/calendar) for automated watering schedules
  - [Trefle Plant API](https://trefle.io/) for plant data


