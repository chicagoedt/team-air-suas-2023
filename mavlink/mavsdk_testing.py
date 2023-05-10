import asyncio
from mavsdk import System


async def run():
    drone = System()
    await drone.connect(system_address="serial:///dev/ttyTHS1:57600")

    await drone.action.arm()
    # await print_health(drone)

    asyncio.ensure_future(print_position(drone))
    asyncio.ensure_future(print_battery(drone))
    asyncio.ensure_future(print_mode(drone))

    
#    while True:
#        await asyncio.sleep(1)


async def print_health(drone):
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
        else:
            print("-- Global position estimate BAD")


async def print_position(drone):
    async for position in drone.telemetry.position():
        print(position)


async def print_battery(drone):
    async for battery in drone.telemetry.battery():
        print(f"Battery: {battery.remaining_percent}")


async def print_mode(drone):
    async for mode in drone.telemetry.flight_mode():
        print(f"mode: {mode}")


if __name__ == "__main__":
    asyncio.run(run())

