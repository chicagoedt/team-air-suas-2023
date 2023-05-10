import asyncio
from mavsdk import System
from mavsdk.server_utility import StatusTextType
from mavsdk.offboard import Offboard, OffboardError, VelocityNedYaw

async def run():

    drone = System(sysid = 1)
    await drone.connect(system_address="serial:///dev/ttyTHS1:57600")
    print("Waiting for drone ...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("drone is connected")
            break;

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    #print("-- Setting initial setpoint")
    #await drone.offboard.set_velocity_ned(VelocityNedYaw(0.0, 0.0, 0.0, 0.0))

    #print("-- Starting offboard")
    #try:
    #    await drone.offboard.start()
    #except OffboardError as error:
    #    print(f"Starting offboard mode failed with error code: \
    #          {error._result.result}")
    #    return
    #print("Welcome to offboard mode")
    


    #print("--Checking if switch to offboard mode")
    #async for flight_mode in drone.telemetry.flight_mode():
    #    print("Not in offboard mode yet :(. FlightMode:{}".format(flight_mode))
    #    if str(flight_mode) == "OFFBOARD":
    #        print("Welcome to offboard mode")
    #        break
    #    await drone.server_utility.send_status_text(StatusTextType.INFO, "Hello world")
    #    print("hello world")

    # arm
    print("-- Arming")
    await drone.action.arm()
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
