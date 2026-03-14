import sqlite3
from datetime import datetime

def connect():
    return sqlite3.connect('transport.db')

def extract(cursor):
    print('Extracting data...')
    cursor.execute('''
        SELECT t.trip_id, r.route_name, b.total_seats,
               COUNT(bk.booking_id) as seats_booked,
               SUM(p.amount) as total_revenue
        FROM trips t
        JOIN routes r ON t.route_id = r.route_id
        JOIN buses b ON t.bus_id = b.bus_id
        LEFT JOIN bookings bk ON t.trip_id = bk.trip_id
        LEFT JOIN payments p ON bk.payment_id = p.payment_id
        GROUP BY t.trip_id
    ''')
    rows = cursor.fetchall()
    print(f'  Extracted {len(rows)} trips')
    return rows

def transform(rows):
    print('Transforming data...')
    transformed = []
    for row in rows:
        trip_id = row[0]
        route_name = row[1]
        total_seats = row[2]
        seats_booked = row[3]
        total_revenue = row[4] or 0
        seats_remaining = total_seats - seats_booked
        occupancy_rate = round((seats_booked / total_seats) * 100, 2)
        transformed.append((
            trip_id, route_name, total_seats,
            seats_booked, seats_remaining,
            total_revenue, occupancy_rate
        ))
        print(f'  Trip {trip_id} | {route_name} | Occupancy: {occupancy_rate}% | Revenue: ₦{total_revenue:,.2f}')
    return transformed

def load(cursor, conn, transformed):
    print('Loading into summary table...')
    cursor.execute('DELETE FROM trip_summary_log')
    for row in transformed:
        cursor.execute('''
            INSERT INTO trip_summary_log (
                trip_id, route_name, total_seats,
                seats_booked, seats_remaining,
                total_revenue, occupancy_rate
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', row)
    conn.commit()
    print(f'  Loaded {len(transformed)} records into trip_summary_log')

def main():
    print()
    print('=' * 40)
    print(f'  PIPELINE RUN — {datetime.now().strftime("%d %B %Y, %I:%M %p")}')
    print('=' * 40)

    conn = connect()
    cursor = conn.cursor()

    rows = extract(cursor)
    transformed = transform(rows)
    load(cursor, conn, transformed)

    conn.close()
    print()
    print('Pipeline complete.')
    print('=' * 40)
    print()

main()