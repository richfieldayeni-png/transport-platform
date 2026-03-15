from flask import Flask, request, redirect, url_for
import sqlite3

app = Flask(__name__)

import init_db
init_db.init()

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
        <p>Operational Dashboard — <a href="/book" style="color:#3498db;">+ New Booking</a></p>

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
@app.route('/book', methods=['GET'])
def book_form():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT trip_id, date FROM trips WHERE status = 'scheduled'")
    trips = cursor.fetchall()

    cursor.execute("SELECT user_id, full_name FROM users WHERE is_active = 1")
    users = cursor.fetchall()

    conn.close()

    trip_options = ''.join(f'<option value="{t[0]}">Trip {t[0]} — {t[1]}</option>' for t in trips)
    user_options = ''.join(f'<option value="{u[0]}">{u[1]}</option>' for u in users)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>New Booking</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; background: #f4f4f4; }}
            h1 {{ color: #2c3e50; }}
            .card {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); max-width: 500px; }}
            label {{ display: block; margin-top: 16px; font-weight: bold; color: #34495e; }}
            select, input {{ width: 100%; padding: 8px; margin-top: 6px; border: 1px solid #ddd; border-radius: 4px; font-size: 14px; }}
            button {{ margin-top: 24px; background: #3498db; color: white; padding: 10px 24px; border: none; border-radius: 4px; font-size: 16px; cursor: pointer; }}
            button:hover {{ background: #2980b9; }}
            a {{ display: inline-block; margin-bottom: 20px; color: #3498db; }}
        </style>
    </head>
    <body>
        <a href="/">← Back to Dashboard</a>
        <div class="card">
            <h1>New Booking</h1>
            <form action="/book" method="POST">
                <label>Passenger</label>
                <select name="user_id">{user_options}</select>

                <label>Trip</label>
                <select name="trip_id">{trip_options}</select>

                <label>Seat Number</label>
                <input type="number" name="seat_number" min="1" max="18" required />

                <label>Payment Type</label>
                <select name="payment_type">
                    <option value="card">Card</option>
                    <option value="bank_transfer">Bank Transfer</option>
                </select>

                <label>Amount (₦)</label>
                <input type="number" name="amount" value="1500" required />

                <button type="submit">Confirm Booking</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/book', methods=['POST'])
def book_submit():
    user_id = request.form['user_id']
    trip_id = request.form['trip_id']
    seat_number = request.form['seat_number']
    payment_type = request.form['payment_type']
    amount = request.form['amount']

    conn = connect()
    cursor = conn.cursor()

    # Create payment first
    cursor.execute('''
        INSERT INTO payments (payment_type, payment_status, amount, payment_completion)
        VALUES (?, 'completed', ?, TRUE)
    ''', (payment_type, amount))
    payment_id = cursor.lastrowid

    # Create booking
    cursor.execute('''
        INSERT INTO bookings (user_id, trip_id, payment_id, seat_number, booking_status)
        VALUES (?, ?, ?, ?, 'confirmed')
    ''', (user_id, trip_id, payment_id, seat_number))

    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))

@app.route('/complete/<int:trip_id>', methods=['POST'])
def complete_trip(trip_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE trips SET status = 'completed' WHERE trip_id = ?", (trip_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET booking_status = 'cancelled' WHERE booking_id = ?", (booking_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)