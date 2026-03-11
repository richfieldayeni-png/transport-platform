
SELECT driver_id, full_name
from drivers
where is_active=TRUE


 SELECT bus_name
 FROM buses 
 where is_active=false


select booking_id, trip_id, user_id, seat_number, booking_status
from bookings 
where user_id=1