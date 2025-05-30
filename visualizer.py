import pygame
import asyncio
import websockets
import json

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Дрон-симулятор")
font = pygame.font.SysFont('Arial', 20)

drone_pos = [400, 300]
drone_data = {"x": 0, "y": 0, "z": 0, "speed": 0}

async def receive_data():
    async with websockets.connect("ws://localhost:8000") as ws:
        while True:
            data = await ws.recv()
            drone_data.update(json.loads(data))

def update_drone_pos():
    drone_pos[0] = int(drone_data["x"] * 8)
    drone_pos[1] = int(drone_data["y"] * 6)

async def main():
    asyncio.create_task(receive_data())
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        update_drone_pos()
        screen.fill((0, 0, 0))
        pygame.draw.circle(screen, (255, 0, 0), drone_pos, 10)
        text = f"X: {drone_data['x']:.1f}, Y: {drone_data['y']:.1f}, Z: {drone_data['z']:.1f}"
        screen.blit(font.render(text, True, (255, 255, 255)), (10, 10))
        pygame.display.flip()
        clock.tick(60)
        await asyncio.sleep(0)

asyncio.run(main())


