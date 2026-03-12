import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect('transport.db')

def add_trip(cursor, route_id, bus_id, driver_id, departure, arrival, date):
    cursor.execute('''
        INSERT INTO trips (route_id, bus_id, driver_id, scheduled_departure_time, 
                          scheduled_arrival_time, status, date)
        VALUES (?, ?, ?, ?, ?, 'scheduled', ?)
    ''', (route_id, bus_id, driver_id, departure, arrival, date))
    return cursor.lastrowid

def add_payment(cursor, payment_type, amount):
    cursor.execute('''
        INSERT INTO payments (payment_type, payment_status, amount, payment_completion)
        VALUES (?, 'completed', ?, TRUE)
    ''', (payment_type, amount))
    return cursor.lastrowid

def add_booking(cursor, user_id, trip_id, payment_id, seat_number):
    cursor.execute('''
        INSERT INTO bookings (user_id, trip_id, payment_id, seat_number, booking_status)
        VALUES (?, ?, ?, ?, 'confirmed')
    ''', (user_id, trip_id, payment_id, seat_number))
    return cursor.lastrowid

def main():
    conn = connect()
    cursor = conn.cursor()

    print('Seeding new data...')

    # Add a new trip on Route B
    trip_id = add_trip(
        cursor,
        route_id=2,
        bus_id=2,
        driver_id=2,
        departure='2024-01-17 08:00:00',
        arrival='2024-01-17 08:20:00',
        date='2024-01-17'
    )
    print(f'  New trip created — Trip ID: {trip_id}')

    # Add 3 new bookings for that trip
    for i, (user_id, seat) in enumerate([(1, 2), (2, 4), (3, 6)], 1):
        payment_id = add_payment(cursor, 'card', 1500.00)
        booking_id = add_booking(cursor, user_id, trip_id, payment_id, seat)
        print(f'  Booking {booking_id} confirmed — User {user_id}, Seat {seat}')

    conn.commit()
    conn.close()
    print()
    print('Done. Run report.py to see updated numbers.')

main()