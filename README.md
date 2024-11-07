Plant Pal 🌱
Plant Pal is a full-stack web application designed to help users monitor and care for their plants. By synchronizing an ESP32 device with a soil moisture sensor, Plant Pal enables real-time moisture level monitoring, providing users with personalized insights and automated reminders for plant care.

Key Features
Real-Time Moisture Monitoring: Sync an ESP32 microcontroller to send live soil moisture readings from a sensor in your plant’s pot. Data is stored and processed through the backend, enabling users to track and monitor their plants’ health.

Fast Search Engine for Plants: Plant Pal features an optimized search engine that allows users to quickly search and select from a database of over 400,000 plants. The trie-based data structure provides instant suggestions, helping users efficiently find plants and access relevant data.

Custom Watering Schedule Integration: Plant Pal leverages the Google Calendar API to create personalized watering schedules for each plant based on its ideal moisture levels. With just one click, users can receive reminders directly in their Google Calendar, helping them stay on top of plant care.

Project Architecture
Backend: Built with Flask, the backend handles data storage, real-time updates, and API integration. It receives POST requests from the ESP32, parses incoming moisture data, and sends relevant information to the frontend.

Frontend: A React application that provides an intuitive user interface for interacting with Plant Pal. Users can connect their ESP32 device, view moisture data in real-time, and manage plant care schedules easily.

ESP32 Integration: The ESP32 device, acting as its own server, collects and sends real-time soil moisture data to the backend with a unique token provided during the connection process. This ensures data integrity and user-specific updates.

Tech Stack
Frontend: React
Backend: Flask (Python)
Database: PostgreSQL for data persistence
Hardware: ESP32 microcontroller with a soil moisture sensor
APIs:
Google Calendar API for automated watering schedules
Trefle Plant API for plant data
Getting Started
To set up Plant Pal on your local machine, follow these steps:

Prerequisites
Hardware: ESP32 microcontroller, soil moisture sensor.
Software:
Python 3.x
Node.js
Google Calendar API credentials
Installation
Clone the Repository:

bash
Copy code
git clone https://github.com/username/plant-pal.git
cd plant-pal
Backend Setup:

Navigate to the backend folder and install dependencies:
bash
Copy code
cd backend
pip install -r requirements.txt
Set up environment variables by creating a .env file in the backend directory with necessary credentials:
plaintext
Copy code
GOOGLE_CALENDAR_API_KEY=<your-api-key>
DATABASE_URL=<your-database-url>
Frontend Setup:

Navigate to the frontend folder and install dependencies:
bash
Copy code
cd ../frontend
npm install
ESP32 Setup:

Program the ESP32 to capture soil moisture data and send it to the backend’s designated route. The ESP32 should include the unique token received during the connection process to authenticate data submissions.
Run the Application:

In the backend directory, start the Flask server:
bash
Copy code
flask run
In the frontend directory, start the React development server:
bash
Copy code
npm start
Connect the ESP32:

Through the frontend, connect the ESP32 device and link it to a specific plant profile, ensuring the device sends data to the correct route.
Usage
Add a Plant: Use the search bar to find your plant from a database of 400,000+ plants, aided by real-time suggestions.
Monitor Soil Moisture: Once the ESP32 is synchronized, monitor real-time soil moisture data through the dashboard.
Create a Watering Schedule: Click “Generate Watering Schedule” to automatically add a custom watering plan to your Google Calendar.
License
This project is licensed under the MIT License.
