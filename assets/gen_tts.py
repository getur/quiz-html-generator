import asyncio, base64, io
import edge_tts

async def gen(text, filename):
    communicate = edge_tts.Communicate(text, voice="pt-PT-RaquelNeural")
    buf = io.BytesIO()
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            buf.write(chunk["data"])
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    print(f"=== {filename} ===")
    print(f"data:audio/mp3;base64,{b64}")
    print()

asyncio.run(gen("Correcto", "correcto.txt"))
asyncio.run(gen("Incorrecto", "incorrecto.txt"))
