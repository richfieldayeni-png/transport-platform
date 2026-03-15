from flask import Flask, request, redirect, url_for
import sqlite3
import init_db

init_db.init()

app = Flask(__name__)

def connect():
    return sqlite3.connect('transport.db')

# ── shared styles ──────────────────────────────────────────────────────────────
HEAD = """
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  :root {
    --bg:      #0D0F14;
    --surface: #151820;
    --border:  #1E2330;
    --amber:   #F59E0B;
    --amber2:  #FCD34D;
    --green:   #10B981;
    --red:     #EF4444;
    --text:    #E8EAF0;
    --muted:   #6B7280;
    --mono:    'IBM Plex Mono', monospace;
    --sans:    'DM Sans', sans-serif;
    --display: 'Syne', sans-serif;
  }
  body { background: var(--bg); color: var(--text); font-family: var(--sans); min-height: 100vh; }
  a { color: var(--amber); text-decoration: none; }
  a:hover { color: var(--amber2); }

  /* NAV */
  nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 20px 48px; border-bottom: 1px solid var(--border);
    position: sticky; top: 0; background: rgba(13,15,20,0.92);
    backdrop-filter: blur(12px); z-index: 100;
  }
  .logo { font-family: var(--display); font-size: 20px; font-weight: 800;
          letter-spacing: -0.5px; color: var(--text); }
  .logo span { color: var(--amber); }
  .nav-links { display: flex; gap: 32px; }
  .nav-links a { font-size: 14px; color: var(--muted); font-weight: 500;
                 transition: color .2s; letter-spacing: 0.3px; }
  .nav-links a:hover, .nav-links a.active { color: var(--text); }
  .btn {
    display: inline-flex; align-items: center; gap: 8px;
    padding: 10px 22px; border-radius: 6px; font-size: 14px;
    font-weight: 600; font-family: var(--sans); cursor: pointer;
    transition: all .2s; border: none; text-decoration: none;
  }
  .btn-primary { background: var(--amber); color: #0D0F14; }
  .btn-primary:hover { background: var(--amber2); color: #0D0F14; }
  .btn-ghost { background: transparent; color: var(--text);
               border: 1px solid var(--border); }
  .btn-ghost:hover { border-color: var(--amber); color: var(--amber); }
  .btn-sm { padding: 6px 14px; font-size: 12px; }
  .btn-danger { background: rgba(239,68,68,0.12); color: var(--red);
                border: 1px solid rgba(239,68,68,0.3); }
  .btn-danger:hover { background: rgba(239,68,68,0.2); }

  /* CARDS */
  .card {
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 28px;
  }
  .card-sm { padding: 20px; }

  /* STAT CARD */
  .stat-label { font-size: 12px; color: var(--muted); text-transform: uppercase;
                letter-spacing: 1px; font-family: var(--mono); margin-bottom: 10px; }
  .stat-value { font-family: var(--display); font-size: 36px; font-weight: 700;
                color: var(--text); line-height: 1; }
  .stat-value.amber { color: var(--amber); }
  .stat-value.green { color: var(--green); }
  .stat-sub { font-size: 13px; color: var(--muted); margin-top: 8px;
              font-family: var(--mono); }

  /* TABLE */
  .table-wrap { overflow-x: auto; }
  table { width: 100%; border-collapse: collapse; }
  th { font-size: 11px; font-family: var(--mono); text-transform: uppercase;
       letter-spacing: 1px; color: var(--muted); padding: 12px 16px;
       border-bottom: 1px solid var(--border); text-align: left; }
  td { padding: 14px 16px; font-size: 14px; border-bottom: 1px solid rgba(30,35,48,0.6); }
  tr:last-child td { border-bottom: none; }
  tr:hover td { background: rgba(245,158,11,0.03); }

  /* BADGES */
  .badge {
    display: inline-block; padding: 3px 10px; border-radius: 20px;
    font-size: 11px; font-family: var(--mono); font-weight: 500;
    text-transform: uppercase; letter-spacing: 0.5px;
  }
  .badge-green { background: rgba(16,185,129,0.12); color: var(--green);
                 border: 1px solid rgba(16,185,129,0.25); }
  .badge-amber { background: rgba(245,158,11,0.12); color: var(--amber);
                 border: 1px solid rgba(245,158,11,0.25); }
  .badge-red   { background: rgba(239,68,68,0.12); color: var(--red);
                 border: 1px solid rgba(239,68,68,0.25); }

  /* SECTION TITLE */
  .section-title {
    font-family: var(--display); font-size: 16px; font-weight: 700;
    color: var(--text); margin-bottom: 20px; letter-spacing: -0.3px;
  }
  .section-title span { color: var(--amber); }

  /* GRID LAYOUTS */
  .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
  .grid-2 { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; }
  .grid-charts { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
  @media (max-width: 900px) {
    .grid-3, .grid-2, .grid-charts { grid-template-columns: 1fr; }
    nav { padding: 16px 24px; }
    .nav-links { gap: 16px; }
    main { padding: 24px; }
  }

  /* PAGE WRAPPER */
  main { max-width: 1280px; margin: 0 auto; padding: 40px 48px; }

  /* FORM */
  .form-group { margin-bottom: 20px; }
  label { display: block; font-size: 12px; font-family: var(--mono);
          text-transform: uppercase; letter-spacing: 1px; color: var(--muted);
          margin-bottom: 8px; }
  select, input[type=number] {
    width: 100%; padding: 12px 16px; background: var(--bg);
    border: 1px solid var(--border); border-radius: 8px;
    color: var(--text); font-size: 14px; font-family: var(--sans);
    transition: border-color .2s; outline: none;
  }
  select:focus, input:focus { border-color: var(--amber); }
  select option { background: var(--surface); }

  /* DIVIDER */
  .divider { height: 1px; background: var(--border); margin: 32px 0; }

  /* PROGRESS BAR */
  .progress-bar {
    height: 4px; background: var(--border); border-radius: 2px;
    overflow: hidden; margin-top: 8px;
  }
  .progress-fill {
    height: 100%; background: var(--amber); border-radius: 2px;
    transition: width .6s ease;
  }
</style>
"""

def nav(active="dashboard"):
    links = [
        ("landing", "/", "Overview"),
        ("dashboard", "/dashboard", "Dashboard"),
        ("book", "/book", "New Booking"),
    ]
    items = "".join(
        f'<a href="{url}" class="{"active" if k == active else ""}">{label}</a>'
        for k, url, label in links
    )
    return f"""
    <nav>
      <div class="logo">Route<span>X</span></div>
      <div class="nav-links">{items}</div>
      <a href="/book" class="btn btn-primary btn-sm">+ Book Ride</a>
    </nav>
    """

# ── LANDING PAGE ───────────────────────────────────────────────────────────────
@app.route('/')
def landing():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_active=1")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM trips")
    total_trips = cursor.fetchone()[0]
    cursor.execute("SELECT SUM(amount) FROM payments WHERE payment_status='completed'")
    total_rev = cursor.fetchone()[0] or 0
    cursor.execute("SELECT COUNT(*) FROM bookings WHERE booking_status='confirmed'")
    total_bookings = cursor.fetchone()[0]
    conn.close()

    return f"""<!DOCTYPE html>
<html lang="en">
<head>{HEAD}<title>RouteX — Corporate Transport Platform</title>
<style>
  .hero {{
    padding: 100px 48px 80px;
    max-width: 1280px; margin: 0 auto;
    display: grid; grid-template-columns: 1fr 1fr; gap: 80px; align-items: center;
  }}
  .hero-tag {{
    display: inline-block; padding: 6px 14px; border: 1px solid var(--amber);
    border-radius: 20px; font-size: 11px; font-family: var(--mono);
    color: var(--amber); text-transform: uppercase; letter-spacing: 1px;
    margin-bottom: 24px;
  }}
  .hero h1 {{
    font-family: var(--display); font-size: 54px; font-weight: 800;
    line-height: 1.05; letter-spacing: -2px; color: var(--text);
    margin-bottom: 24px;
  }}
  .hero h1 em {{ color: var(--amber); font-style: normal; }}
  .hero p {{
    font-size: 17px; color: var(--muted); line-height: 1.7;
    margin-bottom: 36px; max-width: 480px;
  }}
  .hero-actions {{ display: flex; gap: 16px; flex-wrap: wrap; }}
  .hero-visual {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 16px; padding: 32px; position: relative; overflow: hidden;
  }}
  .hero-visual::before {{
    content: ''; position: absolute; top: -60px; right: -60px;
    width: 200px; height: 200px; background: radial-gradient(circle, rgba(245,158,11,0.15), transparent);
    border-radius: 50%;
  }}
  .metric-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 20px; }}
  .metric-box {{
    background: var(--bg); border: 1px solid var(--border);
    border-radius: 10px; padding: 18px;
  }}
  .metric-box .val {{
    font-family: var(--display); font-size: 28px; font-weight: 700;
    color: var(--amber); margin-bottom: 4px;
  }}
  .metric-box .lbl {{ font-size: 12px; color: var(--muted); font-family: var(--mono); }}
  .feature-strip {{
    max-width: 1280px; margin: 0 auto; padding: 0 48px 80px;
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px;
  }}
  .feature-card {{
    background: var(--surface); border: 1px solid var(--border);
    border-radius: 12px; padding: 28px;
  }}
  .feature-icon {{
    width: 44px; height: 44px; background: rgba(245,158,11,0.1);
    border: 1px solid rgba(245,158,11,0.2); border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 20px; margin-bottom: 18px;
  }}
  .feature-card h3 {{
    font-family: var(--display); font-size: 17px; font-weight: 700;
    margin-bottom: 10px; color: var(--text);
  }}
  .feature-card p {{ font-size: 14px; color: var(--muted); line-height: 1.6; }}
  @media (max-width: 900px) {{
    .hero {{ grid-template-columns: 1fr; padding: 60px 24px; gap: 40px; }}
    .hero h1 {{ font-size: 36px; }}
    .feature-strip {{ grid-template-columns: 1fr; padding: 0 24px 60px; }}
  }}
</style>
</head>
<body>
{nav("landing")}
<section class="hero">
  <div>
    <div class="hero-tag">🚌 Abuja B2B Transport</div>
    <h1>Moving corporate<br>teams <em>efficiently</em></h1>
    <p>RouteX is a smart corporate commute platform purpose-built for Abuja's business district — connecting companies to reliable, trackable, seat-based transport.</p>
    <div class="hero-actions">
      <a href="/dashboard" class="btn btn-primary">View Live Dashboard →</a>
      <a href="/book" class="btn btn-ghost">Book a Ride</a>
    </div>
  </div>
  <div class="hero-visual">
    <div class="metric-row">
      <div class="metric-box">
        <div class="val">₦{total_rev:,.0f}</div>
        <div class="lbl">Total Revenue</div>
      </div>
      <div class="metric-box">
        <div class="val">{total_bookings}</div>
        <div class="lbl">Confirmed Bookings</div>
      </div>
    </div>
    <div class="metric-row">
      <div class="metric-box">
        <div class="val">{total_trips}</div>
        <div class="lbl">Trips Operated</div>
      </div>
      <div class="metric-box">
        <div class="val">{total_users}</div>
        <div class="lbl">Active Passengers</div>
      </div>
    </div>
    <div style="background:var(--bg);border:1px solid var(--border);border-radius:8px;padding:14px;font-family:var(--mono);font-size:12px;color:var(--muted);">
      <span style="color:var(--green);">●</span> Platform operational · Abuja Pilot Phase
    </div>
  </div>
</section>

<section class="feature-strip">
  <div class="feature-card">
    <div class="feature-icon">📍</div>
    <h3>Route Intelligence</h3>
    <p>Pre-configured corporate routes with real-time seat availability, departure tracking, and occupancy analytics.</p>
  </div>
  <div class="feature-card">
    <div class="feature-icon">💳</div>
    <h3>Seamless Payments</h3>
    <p>Card and bank transfer support with automatic booking confirmation, payment reconciliation, and receipt generation.</p>
  </div>
  <div class="feature-card">
    <div class="feature-icon">📊</div>
    <h3>Ops Dashboard</h3>
    <p>Live operational visibility — revenue, occupancy rates, driver assignments, and route demand in one place.</p>
  </div>
</section>
</body></html>"""


# ── DASHBOARD ──────────────────────────────────────────────────────────────────
@app.route('/dashboard')
def dashboard():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*), SUM(amount), AVG(amount)
        FROM payments WHERE payment_status='completed'
    """)
    revenue = cursor.fetchone()

    cursor.execute("""
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
    """)
    trips = cursor.fetchall()

    cursor.execute("""
        SELECT r.route_name, COUNT(bk.booking_id) as total_bookings
        FROM bookings bk
        JOIN trips t ON bk.trip_id = t.trip_id
        JOIN routes r ON t.route_id = r.route_id
        GROUP BY r.route_name ORDER BY total_bookings DESC
    """)
    demand = cursor.fetchall()

    cursor.execute("""
        SELECT full_name, phone_number FROM drivers WHERE is_active=1
    """)
    drivers = cursor.fetchall()

    cursor.execute("""
        SELECT r.route_name, d.full_name, t.scheduled_departure_time
        FROM trips t
        JOIN routes r ON t.route_id = r.route_id
        JOIN drivers d ON t.driver_id = d.driver_id
        WHERE t.status='scheduled'
    """)
    upcoming = cursor.fetchall()

    cursor.execute("""
        SELECT b.booking_id, u.full_name, r.route_name,
               b.seat_number, b.booking_status, p.amount
        FROM bookings b
        JOIN users u ON b.user_id = u.user_id
        JOIN trips t ON b.trip_id = t.trip_id
        JOIN routes r ON t.route_id = r.route_id
        JOIN payments p ON b.payment_id = p.payment_id
        ORDER BY b.booking_id DESC LIMIT 10
    """)
    bookings = cursor.fetchall()

    conn.close()

    # Chart data
    trip_labels = [f"Trip {t[0]}" for t in trips]
    occupancy_data = [round((t[4]/t[3])*100, 1) for t in trips]
    route_labels = [d[0] for d in demand]
    route_data = [d[1] for d in demand]

    trip_rows = ""
    for t in trips:
        pct = round((t[4]/t[3])*100)
        badge = f'<span class="badge badge-green">completed</span>' if t[6]=='completed' else f'<span class="badge badge-amber">scheduled</span>'
        trip_rows += f"""<tr>
          <td><span style="font-family:var(--mono);font-size:13px;color:var(--amber)">#{t[0]}</span></td>
          <td>{t[1]}</td>
          <td>{t[2]}</td>
          <td><span style="font-family:var(--mono)">{t[4]}/{t[3]}</span>
            <div class="progress-bar"><div class="progress-fill" style="width:{pct}%"></div></div></td>
          <td>{badge}</td>
          <td style="font-family:var(--mono);color:var(--muted);font-size:13px">{t[7]}</td>
          <td>
            <form method="POST" action="/complete/{t[0]}" style="display:inline">
              <button class="btn btn-ghost btn-sm" type="submit" {'disabled' if t[6]=='completed' else ''}>
                {'✓ Done' if t[6]=='completed' else 'Complete'}
              </button>
            </form>
          </td>
        </tr>"""

    booking_rows = ""
    for b in bookings:
        badge = f'<span class="badge badge-green">confirmed</span>' if b[4]=='confirmed' else f'<span class="badge badge-red">cancelled</span>'
        cancel_btn = "" if b[4]=='cancelled' else f"""
          <form method="POST" action="/cancel/{b[0]}" style="display:inline">
            <button class="btn btn-danger btn-sm" type="submit">Cancel</button>
          </form>"""
        booking_rows += f"""<tr>
          <td><span style="font-family:var(--mono);color:var(--amber)">#BK{b[0]:03d}</span></td>
          <td>{b[1]}</td>
          <td>{b[2]}</td>
          <td style="font-family:var(--mono)">{b[3]}</td>
          <td>{badge}</td>
          <td style="font-family:var(--mono);color:var(--green)">₦{b[5]:,.0f}</td>
          <td>{cancel_btn}</td>
        </tr>"""

    driver_rows = ""
    for d in drivers:
        driver_rows += f"""<tr>
          <td>{d[0]}</td>
          <td style="font-family:var(--mono);color:var(--muted)">{d[1]}</td>
          <td><span class="badge badge-green">active</span></td>
        </tr>"""

    upcoming_rows = ""
    for u in upcoming:
        upcoming_rows += f"""<tr>
          <td>{u[0]}</td>
          <td>{u[1]}</td>
          <td style="font-family:var(--mono);color:var(--muted);font-size:13px">{u[2]}</td>
        </tr>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>{HEAD}
<title>RouteX — Operations Dashboard</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.0/chart.umd.min.js"></script>
<style>
  .dash-header {{
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 32px;
  }}
  .dash-header h1 {{
    font-family: var(--display); font-size: 28px; font-weight: 800;
    letter-spacing: -1px;
  }}
  .dash-header h1 span {{ color: var(--amber); }}
  .timestamp {{ font-size: 12px; color: var(--muted); font-family: var(--mono); }}
</style>
</head>
<body>
{nav("dashboard")}
<main>
  <div class="dash-header">
    <h1>Operations <span>Dashboard</span></h1>
    <div class="timestamp">Abuja Corporate Transport · Live Data</div>
  </div>

  <!-- STAT CARDS -->
  <div class="grid-3" style="margin-bottom:24px">
    <div class="card card-sm">
      <div class="stat-label">Total Revenue</div>
      <div class="stat-value amber">₦{revenue[1]:,.2f}</div>
      <div class="stat-sub">{revenue[0]} completed payments</div>
    </div>
    <div class="card card-sm">
      <div class="stat-label">Avg. Ticket</div>
      <div class="stat-value">₦{revenue[2]:,.2f}</div>
      <div class="stat-sub">per booking</div>
    </div>
    <div class="card card-sm">
      <div class="stat-label">Active Routes</div>
      <div class="stat-value green">{len(demand)}</div>
      <div class="stat-sub">{len(trips)} total trips operated</div>
    </div>
  </div>

  <!-- CHARTS ROW -->
  <div class="grid-charts" style="margin-bottom:24px">
    <div class="card">
      <div class="section-title">Seat Occupancy <span>by Trip</span></div>
      <canvas id="occupancyChart" height="120"></canvas>
    </div>
    <div class="card">
      <div class="section-title">Route <span>Demand</span></div>
      <canvas id="demandChart" height="120"></canvas>
    </div>
  </div>

  <!-- TRIPS TABLE -->
  <div class="card" style="margin-bottom:24px">
    <div class="section-title">Trip <span>Summary</span></div>
    <div class="table-wrap">
      <table>
        <thead><tr>
          <th>ID</th><th>Route</th><th>Driver</th>
          <th>Occupancy</th><th>Status</th><th>Date</th><th>Action</th>
        </tr></thead>
        <tbody>{trip_rows}</tbody>
      </table>
    </div>
  </div>

  <!-- BOTTOM GRID -->
  <div class="grid-2" style="margin-bottom:24px">
    <div class="card">
      <div class="section-title">Upcoming <span>Trips</span></div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Route</th><th>Driver</th><th>Departure</th></tr></thead>
          <tbody>{upcoming_rows or '<tr><td colspan="3" style="color:var(--muted);text-align:center;padding:24px">No upcoming trips</td></tr>'}</tbody>
        </table>
      </div>
    </div>
    <div class="card">
      <div class="section-title">Active <span>Drivers</span></div>
      <div class="table-wrap">
        <table>
          <thead><tr><th>Name</th><th>Phone</th><th>Status</th></tr></thead>
          <tbody>{driver_rows}</tbody>
        </table>
      </div>
    </div>
  </div>

  <!-- BOOKINGS TABLE -->
  <div class="card">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:20px">
      <div class="section-title" style="margin-bottom:0">Recent <span>Bookings</span></div>
      <a href="/book" class="btn btn-primary btn-sm">+ New Booking</a>
    </div>
    <div class="table-wrap">
      <table>
        <thead><tr>
          <th>Ref</th><th>Passenger</th><th>Route</th>
          <th>Seat</th><th>Status</th><th>Amount</th><th>Action</th>
        </tr></thead>
        <tbody>{booking_rows}</tbody>
      </table>
    </div>
  </div>
</main>

<script>
const chartDefaults = {{
  color: '#6B7280',
  font: {{ family: 'IBM Plex Mono' }}
}};
Chart.defaults.color = '#6B7280';
Chart.defaults.font.family = 'DM Sans';

new Chart(document.getElementById('occupancyChart'), {{
  type: 'bar',
  data: {{
    labels: {trip_labels},
    datasets: [{{
      label: 'Occupancy %',
      data: {occupancy_data},
      backgroundColor: 'rgba(245,158,11,0.25)',
      borderColor: '#F59E0B',
      borderWidth: 2,
      borderRadius: 6,
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{ legend: {{ display: false }} }},
    scales: {{
      y: {{
        beginAtZero: true, max: 100,
        grid: {{ color: 'rgba(30,35,48,0.8)' }},
        ticks: {{ callback: v => v + '%', color: '#6B7280', font: {{ family: 'IBM Plex Mono', size: 11 }} }}
      }},
      x: {{
        grid: {{ display: false }},
        ticks: {{ color: '#6B7280', font: {{ family: 'IBM Plex Mono', size: 11 }} }}
      }}
    }}
  }}
}});

new Chart(document.getElementById('demandChart'), {{
  type: 'doughnut',
  data: {{
    labels: {route_labels},
    datasets: [{{
      data: {route_data},
      backgroundColor: ['rgba(245,158,11,0.8)', 'rgba(16,185,129,0.8)', 'rgba(99,102,241,0.8)'],
      borderColor: '#151820',
      borderWidth: 3,
    }}]
  }},
  options: {{
    responsive: true,
    plugins: {{
      legend: {{
        position: 'bottom',
        labels: {{ color: '#6B7280', font: {{ family: 'IBM Plex Mono', size: 11 }}, padding: 16 }}
      }}
    }}
  }}
}});
</script>
</body></html>"""


# ── BOOKING FORM ───────────────────────────────────────────────────────────────
@app.route('/book', methods=['GET'])
def book_form():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT trip_id, date, status FROM trips WHERE status='scheduled'")
    trips = cursor.fetchall()
    cursor.execute("SELECT user_id, full_name, company_name FROM users WHERE is_active=1")
    users = cursor.fetchall()
    conn.close()

    trip_options = "".join(
        f'<option value="{t[0]}">Trip #{t[0]} — {t[1]}</option>'
        for t in trips
    )
    user_options = "".join(
        f'<option value="{u[0]}">{u[1]} ({u[2] or "Independent"})</option>'
        for u in users
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>{HEAD}<title>RouteX — New Booking</title></head>
<body>
{nav("book")}
<main style="max-width:600px">
  <div style="margin-bottom:32px">
    <h1 style="font-family:var(--display);font-size:28px;font-weight:800;letter-spacing:-1px;margin-bottom:8px">
      New <span style="color:var(--amber)">Booking</span>
    </h1>
    <p style="color:var(--muted);font-size:14px">Reserve a seat on an upcoming corporate route</p>
  </div>

  <div class="card">
    <form action="/book" method="POST">
      <div class="form-group">
        <label>Passenger</label>
        <select name="user_id" required>{user_options}</select>
      </div>
      <div class="form-group">
        <label>Trip</label>
        <select name="trip_id" required>{trip_options or '<option disabled>No scheduled trips available</option>'}</select>
      </div>
      <div class="grid-2">
        <div class="form-group">
          <label>Seat Number</label>
          <input type="number" name="seat_number" min="1" max="18" placeholder="e.g. 5" required>
        </div>
        <div class="form-group">
          <label>Amount (₦)</label>
          <input type="number" name="amount" value="1500" required>
        </div>
      </div>
      <div class="form-group">
        <label>Payment Method</label>
        <select name="payment_type">
          <option value="card">Card Payment</option>
          <option value="bank_transfer">Bank Transfer</option>
        </select>
      </div>
      <div class="divider"></div>
      <div style="display:flex;gap:12px">
        <button type="submit" class="btn btn-primary" style="flex:1">Confirm Booking →</button>
        <a href="/dashboard" class="btn btn-ghost">Cancel</a>
      </div>
    </form>
  </div>
</main>
</body></html>"""


@app.route('/book', methods=['POST'])
def book_submit():
    user_id = request.form['user_id']
    trip_id = request.form['trip_id']
    seat_number = request.form['seat_number']
    payment_type = request.form['payment_type']
    amount = request.form['amount']

    conn = connect()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO payments (payment_type, payment_status, amount, payment_completion)
        VALUES (?, 'completed', ?, TRUE)
    """, (payment_type, amount))
    payment_id = cursor.lastrowid
    cursor.execute("""
        INSERT INTO bookings (user_id, trip_id, payment_id, seat_number, booking_status)
        VALUES (?, ?, ?, ?, 'confirmed')
    """, (user_id, trip_id, payment_id, seat_number))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/complete/<int:trip_id>', methods=['POST'])
def complete_trip(trip_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE trips SET status='completed' WHERE trip_id=?", (trip_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


@app.route('/cancel/<int:booking_id>', methods=['POST'])
def cancel_booking(booking_id):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE bookings SET booking_status='cancelled' WHERE booking_id=?", (booking_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)