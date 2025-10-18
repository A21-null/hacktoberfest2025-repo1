import asyncio
import websockets
import sys

# Configuración
WS_URL = "ws://localhost:8000/ws/audio-stream"
AUDIO_FILE = "audio_test.wav"  # Cambia por tu archivo WAV (PCM 16kHz, mono, 16bit)
CHUNK_SIZE = 16000 * 2  # 1 segundo de audio

async def send_audio():
    async with websockets.connect(WS_URL) as ws:
        with open(AUDIO_FILE, "rb") as f:
            while True:
                chunk = f.read(CHUNK_SIZE)
                if not chunk:
                    break
                await ws.send(chunk)
                # Recibe transcripción parcial si llega
                try:
                    response = await asyncio.wait_for(ws.recv(), timeout=2)
                    print("Transcripción parcial:", response)
                except asyncio.TimeoutError:
                    pass
        # Cierra la conexión para recibir la transcripción final
        await ws.close()
        # Recibe la última transcripción
        try:
            response = await asyncio.wait_for(ws.recv(), timeout=2)
            print("Transcripción final:", response)
        except Exception:
            pass

if __name__ == "__main__":
    if len(sys.argv) > 1:
        AUDIO_FILE = sys.argv[1]
    asyncio.run(send_audio())
