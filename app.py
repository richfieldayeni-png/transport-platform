from flask import Flask
import sqlite3

app = Flask(__name__)

def connect():
    return sqlite3.connect('transport.db')

@app.route('/')
def dashboard():
    conn = connect()
    cursor = conn.cursor()

    # Revenue
    cursor.execute('''
        SELECT COUNT(*), SUM(amount), AVG(amount)
        FROM payments WHERE payment_status = 'completed'
    ''')
    revenue = cursor.fetchone()

    # Trips
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
    trips = cursor.fetchall()

    # Route demand
    cursor.execute('''
        SELECT r.route_name, COUNT(bk.booking_id) as total_bookings
        FROM bookings bk
        JOIN trips t ON bk.trip_id = t.trip_id
        JOIN routes r ON t.route_id = r.route_id
        GROUP BY r.route_name
        ORDER BY total_bookings DESC
    ''')
    demand = cursor.fetchall()

    # Upcoming trips
    cursor.execute('''
        SELECT r.route_name, d.full_name, t.scheduled_departure_time
        FROM trips t
        JOIN routes r ON t.route_id = r.route_id
        JOIN drivers d ON t.driver_id = d.driver_id
        WHERE t.status = 'scheduled'
    ''')
    upcoming = cursor.fetchall()

    conn.close()

    html = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Transport Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }}
            h1 {{ color: #2c3e50; }}
            h2 {{ color: #34495e; border-bottom: 2px solid #3498db; padding-bottom: 5px; }}
            .card {{ background: white; padding: 20px; margin: 20px 0; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
            .stat {{ font-size: 28px; font-weight: bold; color: #27ae60; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ background: #3498db; color: white; padding: 10px; text-align: left; }}
            td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
            tr:hover {{ background: #f5f5f5; }}
            .scheduled {{ color: #f39c12; font-weight: bold; }}
            .completed {{ color: #27ae60; font-weight: bold; }}
        </style>
    </head>
    <body>
        <h1>Abuja Corporate Transport Platform</h1>
        <p>Operational Dashboard</p>

        <div class="card">
            <h2>Revenue Summary</h2>
            <p>Total Payments: <span class="stat">{revenue[0]}</span></p>
            <p>Total Revenue: <span class="stat">₦{revenue[1]:,.2f}</span></p>
            <p>Average Payment: <span class="stat">₦{revenue[2]:,.2f}</span></p>
        </div>

        <div class="card">
            <h2>Trip Summary</h2>
            <table>
                <tr>
                    <th>Trip</th><th>Route</th><th>Driver</th>
                    <th>Booked</th><th>Remaining</th><th>Status</th><th>Date</th>
                </tr>
                {''.join(f"""<tr>
                    <td>{t[0]}</td><td>{t[1]}</td><td>{t[2]}</td>
                    <td>{t[4]}</td><td>{t[5]}</td>
                    <td class="{t[6]}">{t[6]}</td><td>{t[7]}</td>
                </tr>""" for t in trips)}
            </table>
        </div>

        <div class="card">
            <h2>Route Demand</h2>
            <table>
                <tr><th>Route</th><th>Total Bookings</th></tr>
                {''.join(f"<tr><td>{d[0]}</td><td>{d[1]}</td></tr>" for d in demand)}
            </table>
        </div>

        <div class="card">
            <h2>Upcoming Trips</h2>
            <table>
                <tr><th>Route</th><th>Driver</th><th>Departure</th></tr>
                {''.join(f"<tr><td>{u[0]}</td><td>{u[1]}</td><td>{u[2]}</td></tr>" for u in upcoming)}
            </table>
        </div>

    </body>
    </html>
    '''
    return html

if __name__ == '__main__':
    app.run(debug=True)