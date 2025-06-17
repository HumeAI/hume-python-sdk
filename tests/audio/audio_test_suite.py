#!/usr/bin/env python3
"""
🎧 Hume Audio Testing Suite

Human-in-the-loop testing for Hume SDK audio functionality.

Usage:
    pip install -e ".[microphone]"
    python tests/audio/audio_test_suite.py [test_numbers...]
"""

import asyncio, sys, time, termios, tty, platform, shutil, subprocess, os
from pathlib import Path
from hume.empathic_voice.chat.audio.audio_utilities import play_audio, play_audio_streaming  
from hume.empathic_voice.chat.audio.microphone import Microphone
from hume.empathic_voice.chat.audio.microphone_sender import MicrophoneSender
from hume.empathic_voice.chat.socket_client import ChatWebsocketConnection

test_dir = os.path.dirname(os.path.abspath(__file__))
WAV_SAMPLE = str(Path(test_dir) / "sample.wav")
MP3_SAMPLE = str(Path(test_dir) / "sample.mp3")
PCM_SAMPLE = str(Path(test_dir) / "sample.pcm")

def select_audio_device():
    """Let user select audio output device."""
    try:
        import sounddevice as sd  # type: ignore
        
        devices = sd.query_devices()
        output_devices = [(i, d) for i, d in enumerate(devices) if d['max_output_channels'] > 0]
        
        if not output_devices:
            print("❌ No output devices found")
            return None
            
        print("\n🔊 Available Audio Output Devices:")
        print("=" * 40)
        
        for i, (device_id, device) in enumerate(output_devices):
            default_marker = " (default)" if device_id == sd.default.device[1] else ""
            print(f"{i}: {device['name']}{default_marker}")
        
        print(f"{len(output_devices)}: Use system default")
        
        while True:
            try:
                choice = input(f"\nSelect device (0-{len(output_devices)}): ").strip()
                choice_num = int(choice)
                
                if choice_num == len(output_devices):
                    print("Using system default device")
                    return None
                elif 0 <= choice_num < len(output_devices):
                    device_id, device = output_devices[choice_num]
                    print(f"Selected: {device['name']}")
                    return device_id
                else:
                    print(f"Invalid choice. Enter 0-{len(output_devices)}")
            except (ValueError, KeyboardInterrupt):
                print("\nUsing system default device")
                return None
                
    except ImportError:
        print("❌ sounddevice not available")
        return None

def detect_environment():
    """Detect and print environment information relevant to audio functionality."""
    print("🔍 Environment Detection")
    print("=" * 40)
    
    # Platform info
    print(f"Platform: {platform.system()} {platform.release()} ({platform.machine()})")
    print(f"Python: {sys.version.split()[0]} ({platform.python_implementation()})")
    
    # Container/virtualization detection
    container_hints = []
    if Path("/.dockerenv").exists():
        container_hints.append("Docker")
    if "microsoft" in platform.uname().release.lower():
        container_hints.append("WSL")
    if any(Path(p).exists() for p in ["/proc/vz", "/proc/xen"]):
        container_hints.append("VM")
    if container_hints:
        print(f"Container: {', '.join(container_hints)}")
    
    # Audio dependencies
    print("\nAudio Dependencies:")
    try:
        import sounddevice as sd  # type: ignore
        print(f"✅ sounddevice {sd.__version__}")
        
        # Audio backend info
        try:
            backend = sd.query_hostapis()
            backends = [api['name'] for api in backend]
            print(f"   Backends: {', '.join(backends)}")
        except:
            print("   Backends: detection failed")
            
        # Audio devices
        try:
            devices = sd.query_devices()
            input_devices = [d for d in devices if d['max_input_channels'] > 0]
            output_devices = [d for d in devices if d['max_output_channels'] > 0]
            print(f"   Input devices: {len(input_devices)}")
            print(f"   Output devices: {len(output_devices)}")
            
            # Default devices
            try:
                default_in = sd.default.device[0]
                default_out = sd.default.device[1] 
                if default_in is not None:
                    print(f"   Default input: {devices[default_in]['name']}")
                if default_out is not None:
                    print(f"   Default output: {devices[default_out]['name']}")
            except:
                print("   Default devices: detection failed")
                
        except Exception as e:
            print(f"   Device query failed: {e}")
            
    except ImportError:
        print("❌ sounddevice not available")
    
    # CFFI backend (required by sounddevice)
    try:
        import _cffi_backend  # type: ignore
        print("✅ CFFI backend available")
    except ImportError:
        print("❌ CFFI backend missing")
    
    # Media tools
    print("\nMedia Tools:")
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        try:
            result = subprocess.run(["ffmpeg", "-version"], 
                                  capture_output=True, text=True, timeout=5)
            version_line = result.stdout.split('\n')[0]
            print(f"✅ {version_line}")
        except:
            print(f"✅ ffmpeg available at {ffmpeg_path}")
    else:
        print("❌ ffmpeg not in PATH (MP3 support unavailable)")
    
    # Audio system detection
    print("\nAudio System:")
    if platform.system() == "Linux":
        # Check for PulseAudio
        if shutil.which("pulseaudio"):
            print("✅ PulseAudio detected")
        # Check for ALSA
        if Path("/proc/asound").exists():
            print("✅ ALSA detected")
        # Check for JACK
        if shutil.which("jackd"):
            print("✅ JACK detected")
    elif platform.system() == "Darwin":
        print("✅ CoreAudio (macOS native)")
    elif platform.system() == "Windows":
        print("✅ WASAPI (Windows native)")
    
    print("\n" + "=" * 40)

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

async def play_file(path: str, device=None):
    """Play any audio file."""
    with open(path, 'rb') as f:
        await play_audio(f.read(), device=device)

async def chunks_from_file(path: str):
    """Split file into chunks for streaming."""
    with open(path, 'rb') as f:
        data = f.read()
    chunk_size = len(data) // 5
    for i in range(0, len(data), chunk_size):
        yield data[i:i+chunk_size]
        await asyncio.sleep(0.2)

async def test_1_wav(device=None):
    """Test 1: WAV playback.""" 
    print("\n🎵 TEST 1: WAV Format")
    await play_file(WAV_SAMPLE, device=device)
    assert ask("Did WAV file play correctly?")

async def test_2_mp3(device=None):
    """Test 2: MP3 playback.""" 
    print("\n🎵 TEST 2: MP3 Format")
    await play_file(MP3_SAMPLE, device=device)
    assert ask("Did MP3 file play correctly?")

async def test_3_pcm(device=None):
    """Test 3: PCM playback.""" 
    print("\n🎵 TEST 3: PCM Format")
    await play_file(PCM_SAMPLE, device=device)
    assert ask("Did PCM file play correctly?")

async def test_4_streaming(device=None):
    """Test 4: Streaming playback."""
    print("\n🚀 TEST 4: Streaming")
    await play_audio_streaming(chunks_from_file(WAV_SAMPLE), device=device)
    assert ask("Did streaming work without gaps?")

async def test_5_cancellation(device=None):
    """Test 5: Audio cancellation."""
    print("\n⏹️ TEST 5: Cancellation (stopping in 2s)")
    try:
        task = asyncio.create_task(play_audio_streaming(chunks_from_file(WAV_SAMPLE), device=device))
        await asyncio.sleep(2.0)
        task.cancel()
        await task
    except asyncio.CancelledError:
        pass
    assert ask("Did cancellation work cleanly?")


async def test_6_recording(device=None):
    """Test 6: Recording with playback."""
    print("\n🎤 TEST 6: Recording (5s)")
    chunks = []
    with Microphone.context() as mic:
        print(f"Recording at {mic.sample_rate}Hz, {mic.num_channels} channels")
        start = time.time()
        async for chunk in mic:
            chunks.append(chunk)
            if time.time() - start > 5:
                break
        
        # Play back recorded audio using correct sample rate
        from hume.empathic_voice.chat.audio.audio_utilities import _stream_pcm
        
        async def recorded_chunks():
            yield b''.join(chunks)
            
        await _stream_pcm(recorded_chunks(), mic.sample_rate, mic.num_channels, device=device)
    assert ask("Did recording and playback work?")

async def test_7_sender(device=None):
    """Test 7: MicrophoneSender with mock socket."""
    print("\n🎙️ TEST 7: Microphone Sender (5s)")
    
    chunks_collected = []
    
    class MockSocket(ChatWebsocketConnection):
        def __init__(self, *args, **kwargs):
            pass
        async def _send(self, data: bytes):
            chunks_collected.append(data)
    
    with Microphone.context() as mic:
        print(f"Recording at {mic.sample_rate}Hz, {mic.num_channels} channels")
        sender = MicrophoneSender.new(microphone=mic, allow_interrupt=True)
        socket = MockSocket()
        
        print("Recording...")
        try:
            task = asyncio.create_task(sender.send(socket=socket))
            await asyncio.sleep(5.0)
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass
        
        # Play back all collected chunks
        if chunks_collected:
            print("Playing back recorded audio...")
            from hume.empathic_voice.chat.audio.audio_utilities import _stream_pcm
            
            async def collected_chunks():
                yield b''.join(chunks_collected)
                
            await _stream_pcm(collected_chunks(), mic.sample_rate, mic.num_channels, device=device)
        
    assert ask("Did you hear your voice played back after recording?")

async def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--list":
        print("Tests: 1=WAV 2=MP3 3=PCM 4=Streaming 5=Cancellation 6=Recording 7=Sender")
        return
    
    # Print environment information
    detect_environment()
    
    # Let user select audio device
    selected_device = select_audio_device()
        
    tests = [test_1_wav, test_2_mp3, test_3_pcm, test_4_streaming, test_5_cancellation, test_6_recording, test_7_sender]
    
    if len(sys.argv) > 1:
        # Run specific tests
        for arg in sys.argv[1:]:
            await tests[int(arg)-1](device=selected_device)
    else:
        # Run all tests
        for test in tests:
            await test(device=selected_device)
    
    print("✅ All tests completed!")

if __name__ == "__main__":
    asyncio.run(main())
