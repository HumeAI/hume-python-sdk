#!/usr/bin/env python3
"""
🎧 Hume Audio Testing Suite

Human-in-the-loop testing for Hume SDK audio functionality.

Usage:
    pip install -e ".[microphone]"
    python tests/audio/audio_test_suite.py [test_numbers...]
"""

import asyncio, sys, time, termios, tty
from pathlib import Path
from hume.empathic_voice.chat.audio.audio_utilities import play_audio, play_audio_streaming  
from hume.empathic_voice.chat.audio.microphone import Microphone
from hume.empathic_voice.chat.audio.microphone_sender import MicrophoneSender
from hume.empathic_voice.chat.socket_client import ChatWebsocketConnection

def ask(question: str) -> bool:
    """Get y/n from user."""
    print(f"{question} (y/n): ", end='', flush=True)
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        while True:
            char = sys.stdin.read(1).lower()
            if char == 'y':
                print('y')
                return True
            elif char == 'n':
                print('n') 
                return False
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

async def play_file(path: str):
    """Play any audio file."""
    with open(path, 'rb') as f:
        await play_audio(f.read())

async def chunks_from_file(path: str):
    """Split file into chunks for streaming."""
    with open(path, 'rb') as f:
        data = f.read()
    chunk_size = len(data) // 5  # 5 chunks
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]
        await asyncio.sleep(0.2)

async def test_1_formats():
    """Test 1: WAV, MP3, PCM playback.""" 
    print("\n🎵 TEST 1: Format Support")
    await play_file("sample.wav")
    await play_file("sample.mp3") 
    await play_file("sample.pcm")
    assert ask("Did all three files play correctly?")

async def test_2_streaming():
    """Test 2: Streaming playback."""
    print("\n🚀 TEST 2: Streaming")
    await play_audio_streaming(chunks_from_file("sample.wav"))
    assert ask("Did streaming work without gaps?")

async def test_3_cancellation():
    """Test 3: Audio cancellation."""
    print("\n⏹️ TEST 3: Cancellation (stopping in 2s)")
    try:
        task = asyncio.create_task(play_audio_streaming(chunks_from_file("sample.wav")))
        await asyncio.sleep(2.0)
        task.cancel()
        await task
    except asyncio.CancelledError:
        pass
    assert ask("Did cancellation work cleanly?")

async def test_4_recording():
    """Test 4: Recording with playback."""
    print("\n🎤 TEST 4: Recording (5s)")
    chunks = []
    with Microphone.context() as mic:
        start = time.time()
        async for chunk in mic:
            chunks.append(chunk)
            if time.time() - start > 5:
                break
        # Play back recorded audio directly as PCM
        await play_audio(b''.join(chunks))
    assert ask("Did recording and playback work?")

async def test_5_sender():
    """Test 5: MicrophoneSender with mock socket."""
    print("\n🎙️ TEST 5: Microphone Sender (5s)")
    
    class MockSocket(ChatWebsocketConnection):
        def __init__(self):
            pass
        async def _send(self, data: bytes):
            print(f"MockSocket: Sending {len(data)} bytes")
            await play_audio(data)  # Play raw PCM directly
    
    with Microphone.context() as mic:
        sender = MicrophoneSender.new(microphone=mic, allow_interrupt=True)
        socket = MockSocket()
        try:
            task = asyncio.create_task(sender.send(socket=socket))
            await asyncio.sleep(5.0)
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass
    assert ask("Did you hear real-time playback?")

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print("Tests: 1=Formats 2=Streaming 3=Cancellation 4=Recording 5=Sender")
        return
        
    files = ["sample.wav", "sample.mp3", "sample.pcm"]
    missing = [f for f in files if not Path(f).exists()]
    if missing:
        print(f"❌ Missing: {missing}")
        return
        
    tests = [test_1_formats, test_2_streaming, test_3_cancellation, test_4_recording, test_5_sender]
    
    if len(sys.argv) > 1:
        # Run specific tests
        for arg in sys.argv[1:]:
            await tests[int(arg)-1]()
    else:
        # Run all tests
        for test in tests:
            await test()
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
