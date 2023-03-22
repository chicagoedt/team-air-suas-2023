from pymavlink import mavutil

conn = mavutil.mavlink_connection("/dev/ttyTHS1", baud=57600)

print("waiting for heartbeat...")
conn.wait_heartbeat()

while True:
    msg = conn.recv_match(blocking=True).to_dict()
    print(msg)

