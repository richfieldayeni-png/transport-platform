# Abuja Corporate Transport Platform — Operational Dashboard

## Problem
Transport operations generate critical data — bookings, revenue, 
seat availability, driver assignments — that gets lost in spreadsheets 
and phone calls. This project builds a structured database and live 
web dashboard to give operations teams real-time visibility into 
platform performance.

## Features
- 10-table relational database schema covering trips, bookings, 
  payments, drivers, routes and GPS tracking
- Business logic queries with multi-table JOINs
- Automated operational report via terminal
- Dynamic data insertion script
- Live web dashboard served via Flask

## Tech Stack
- Python 3.11
- SQLite
- Flask

## How to Run
1. Clone the repository
   git clone https://github.com/richfieldayeni-png/transport-platform
2. Navigate into the folder
   cd transport-platform
3. Install Flask
   pip install flask
4. Run the web dashboard
   python3 app.py
5. Open your browser at http://127.0.0.1:5000

## Author
Richfield Ayeni — Product Manager and aspiring Data Engineer. 
Built as a real portfolio project tied to an active B2B transport 
startup in Abuja, Nigeria.