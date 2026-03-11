import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect('transport.db')

def print_header(title):
    print()
    print('=' * 40)
    print(f'  {title}')
    print('=' * 40)

def revenue_summary(cursor):
    print_header('REVENUE SUMMARY')
    cursor.execute('''
        SELECT 
            COUNT(*) as total_payments,
            SUM(amount) as total_revenue,
            AVG(amount) as avg_payment
        FROM payments
        WHERE payment_status = 'completed'
    ''')
    row = cursor.fetchone()
    print(f'  Total Payments    : {row[0]}')
    print(f'  Total Revenue     : ₦{row[1]:,.2f}')
    print(f'  Average Payment   : ₦{row[2]:,.2f}')

def trip_summary(cursor):
    print_header('TRIP SUMMARY')
    cursor.execute('''
        SELECT t.trip_id, r.route_name, d.full_name,
               b.total_seats,
               COUNT(bk.booking_id) as booked,
               b.total_seats - COUNT(bk.booking_id) as remaining,
               t.status, t.date
        FROM trips t
        JOIN routes r ON t.route_id = r.route_id
        JOIN drivers d ON t.driver_id = d.driver_id
        JOIN buses b ON t.bus_id = b.bus_id
        LEFT JOIN bookings bk ON t.trip_id = bk.trip_id
        GROUP BY t.trip_id
    ''')
    for row in cursor.fetchall():
        print(f'  Trip {row[0]} | {row[1]} | Driver: {row[2]}')
        print(f'    Seats: {row[4]} booked, {row[5]} remaining | Status: {row[6]} | Date: {row[7]}')

def route_demand(cursor):
    print_header('ROUTE DEMAND')
    cursor.execute('''
        SELECT r.route_name, COUNT(bk.booking_id) as total_bookings
        FROM bookings bk
        JOIN trips t ON bk.trip_id = t.trip_id
        JOIN routes r ON t.route_id = r.route_id
        GROUP BY r.route_name
        ORDER BY total_bookings DESC
    ''')
    for row in cursor.fetchall():
        print(f'  {row[0]}: {row[1]} bookings')

def active_drivers(cursor):
    print_header('ACTIVE DRIVERS')
    cursor.execute('''
        SELECT full_name, phone_number
        FROM drivers
        WHERE is_active = TRUE
    ''')
    for row in cursor.fetchall():
        print(f'  {row[0]} | {row[1]}')

def main():
    print()
    print(f'  ABUJA CORPORATE TRANSPORT PLATFORM')
    print(f'  Operational Report — {datetime.now().strftime("%d %B %Y, %I:%M %p")}')
    
    conn = connect()
    cursor = conn.cursor()

    revenue_summary(cursor)
    trip_summary(cursor)
    route_demand(cursor)
    active_drivers(cursor)

    conn.close()
    print()
    print('=' * 40)
    print('  End of Report')
    print('=' * 40)
    print()

main()