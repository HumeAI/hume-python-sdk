#!/usr/bin/env python3
"""
🎧 Hume Audio Testing Suite
==========================

Comprehensive human-in-the-loop testing for Hume SDK audio functionality.
Tests the actual use cases: TTS playback, conversational AI audio pipeline.

Usage:
    pip install -e ".[microphone]"
    python tests/audio/audio_test_suite.py

Requirements:
    Install the Hume SDK in development mode with audio dependencies
"""

import argparse
import asyncio
import io
import sys
import struct
import time
from pathlib import Path

import soundfile as sf

from hume.empathic_voice.chat.audio.audio_utilities import play_audio, play_audio_streaming


class AudioTestSuite:
    """Human-in-the-loop audio testing suite for Hume SDK."""
    
    def __init__(self):
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
    
    def log_result(self, test_name: str, passed: bool, details: str = ""):
        """Log test result."""
        self.results[test_name] = {"passed": passed, "details": details}
        self.total_tests += 1
        if passed:
            self.passed_tests += 1
        
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"    {details}")
    
    def get_user_feedback(self, question: str) -> bool:
        """Get yes/no feedback from user."""
        print(f"{question} (y/n): ", end='', flush=True)
        
        try:
            # Unix/Mac
            import termios, tty
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
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
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        except ImportError:
            # Windows
            import msvcrt
            while True:
                char = msvcrt.getch().decode().lower()
                if char == 'y':
                    print('y')
                    return True
                elif char == 'n':
                    print('n')
                    return False
    
    async def play_pcm_file(self, file_path: str) -> None:
        """Play PCM file with known format (s16le, 48kHz)."""
        # Read raw PCM data
        with open(file_path, 'rb') as f:
            raw_data = f.read()
        
        # Convert s16le to float32 samples
        sample_count = len(raw_data) // 2
        samples = []
        for i in range(sample_count):
            # Unpack signed 16-bit little-endian, normalize to [-1, 1]
            sample = struct.unpack('<h', raw_data[i*2:(i+1)*2])[0]
            samples.append(sample / 32768.0)
        
        # Create a BytesIO buffer with WAV format for play_audio
        buffer = io.BytesIO()
        sf.write(buffer, samples, 48000, format='WAV')
        buffer.seek(0)
        
        # Use the SDK's play_audio function
        await play_audio(buffer.getvalue())
    
    async def play_audio_file(self, file_path: str) -> None:
        """Play audio file using Hume SDK play_audio function."""
        with open(file_path, 'rb') as f:
            audio_bytes = f.read()
        await play_audio(audio_bytes)
    
    async def test_1_tts_format_support(self):
        """Test 1: TTS Format Support - WAV, MP3, PCM playback."""
        print("\n" + "="*50)
        print("🎵 TEST 1: TTS Format Support")
        print("="*50)
        print("Testing WAV, MP3, and PCM playback...")
        
        await self.play_audio_file("sample.wav")
        await self.play_audio_file("sample.mp3") 
        await self.play_pcm_file("sample.pcm")
        
        passed = self.get_user_feedback("Did all three audio files play correctly?")
        self.log_result("TTS Format Support", passed)
    
    async def generate_audio_chunks(self, chunk_duration: float = 1.0):
        """Split sample.wav into chunks to simulate streaming TTS."""
        # Read the original WAV file as bytes
        with open("sample.wav", "rb") as f:
            wav_data = f.read()
        
        # First chunk: WAV header + some initial PCM data
        header_size = 44  # Standard WAV header size
        chunk_size = int(chunk_duration * 48000 * 2 * 2)  # Approximate chunk size in bytes
        
        # Yield header + first chunk of PCM data
        first_chunk_end = header_size + chunk_size
        yield wav_data[:first_chunk_end]
        await asyncio.sleep(0.2)
        
        # Subsequent chunks: raw PCM data only
        pos = first_chunk_end
        while pos < len(wav_data):
            end = min(pos + chunk_size, len(wav_data))
            yield wav_data[pos:end]
            pos = end
            await asyncio.sleep(0.2)
    
    async def test_2_streaming_tts(self):
        """Test 2: Streaming TTS - Seamless buffered playback of audio chunks."""
        print("\n" + "="*50)
        print("🚀 TEST 2: Streaming TTS")
        print("="*50)
        print("Playing sample.wav as seamless streaming chunks...")
        
        await play_audio_streaming(self.generate_audio_chunks())
        
        passed = self.get_user_feedback("Did streaming playback work correctly without gaps?")
        self.log_result("Streaming TTS", passed)
    
    async def test_3_cancellation(self):
        """Test 3: Audio Cancellation - Clean interruption of streaming audio."""
        print("\n" + "="*50)
        print("⏹️ TEST 3: Audio Cancellation")
        print("="*50)
        print("Testing cancellation (will stop after 2 seconds)...")
        
        try:
            task = asyncio.create_task(play_audio_streaming(self.generate_audio_chunks(10)))
            await asyncio.sleep(2.0)
            task.cancel()
            await task
        except asyncio.CancelledError:
            pass
        
        passed = self.get_user_feedback("Did cancellation work cleanly?")
        self.log_result("Audio Cancellation", passed)
    
    
    async def test_4_conversation_flow(self):
        """
        Test 4: Conversational AI Audio Pipeline
        - Test WebSocket WAV playback
        - Test audio interruption (clean stop when interruption event received)
        - Test audio queueing (multiple files play in sequence without gaps)
        - Test real-time performance and latency
        """
        print("\n💬 TEST 4: Conversation Flow - NOT YET IMPLEMENTED")
        # Implementation needed:
        # - Mock WebSocket audio data
        # - Test audio interruption mechanism
        # - Test queueing multiple audio files
        # - Measure end-to-end latency
        pass
    
    async def test_5_recording_pipeline(self):
        """
        Test 5: Recording Pipeline  
        - Test recording 5 seconds of audio
        - Verify audio is sent in proper ~10ms chunks
        - Test recording quality and format (16-bit linear PCM)
        - Test microphone device detection and selection
        """
        print("\n🎤 TEST 5: Recording Pipeline - NOT YET IMPLEMENTED")
        # Implementation needed:
        # - Test microphone recording functionality
        # - Verify chunk timing (10ms intervals)
        # - Test audio format compliance
        # - Test device detection and switching
        pass
    
    async def test_6_real_conversation_simulation(self):
        """
        Test 6: Real Conversation Simulation
        - Full WebSocket conversation flow simulation
        - Test interruptions during playback
        - Test audio queueing with realistic timing
        - Test recovery from errors and device issues
        - Test cross-platform behavior
        """
        print("\n🗣️  TEST 6: Real Conversation Simulation - NOT YET IMPLEMENTED")
        # Implementation needed:
        # - Simulate full conversation scenario
        # - Test interrupt + resume flows
        # - Test error recovery scenarios
        # - Test platform-specific behavior
        pass
    
    async def test_7_cross_platform_reliability(self):
        """
        Test 7: Cross-Platform & Device Reliability
        - Test on different operating systems (macOS, Linux, Windows)
        - Test with different audio hardware (built-in, USB headsets, etc.)
        - Test audio device disconnection/reconnection during use
        - Test with unusual audio configurations
        """
        print("\n🖥️  TEST 7: Cross-Platform Reliability - NOT YET IMPLEMENTED")
        # Implementation needed:
        # - Platform-specific testing
        # - Device enumeration and selection
        # - Hot-plug device testing
        # - Error handling for device issues
        pass
    
    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.total_tests - self.passed_tests}")
        print(f"Success Rate: {(self.passed_tests/self.total_tests*100):.1f}%" if self.total_tests > 0 else "No tests run")
        
        print("\n📋 Detailed Results:")
        for test_name, result in self.results.items():
            status = "✅ PASS" if result["passed"] else "❌ FAIL"
            print(f"  {status} {test_name}")
            if result["details"]:
                print(f"      → {result['details']}")
    
    async def run_tests(self, test_numbers=None):
        """Run specified tests or all tests if none specified."""
        available_tests = {
            1: ("TTS Format Support", self.test_1_tts_format_support),
            2: ("Streaming TTS", self.test_2_streaming_tts),
            3: ("Audio Cancellation", self.test_3_cancellation),
            # TODO: Add as implemented
            # 4: ("Conversation Flow", self.test_4_conversation_flow),
            # 5: ("Recording Pipeline", self.test_5_recording_pipeline),
        }
        
        if test_numbers is None:
            selected_tests = list(available_tests.values())
        else:
            selected_tests = []
            for num in test_numbers:
                if num in available_tests:
                    selected_tests.append(available_tests[num])
                else:
                    print(f"❌ Test {num} not available. Available tests: {list(available_tests.keys())}")
                    return
        
        print("🎧 Hume Audio Testing Suite")
        print("==========================")
        print(f"Running {len(selected_tests)} test(s):")
        for name, _ in selected_tests:
            print(f"  • {name}")
        print()
        
        for _, test_func in selected_tests:
            await test_func()
        
        self.print_summary()


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Hume Audio Testing Suite")
    parser.add_argument(
        "tests", 
        nargs="*", 
        type=int, 
        help="Test numbers to run (e.g. 1 2). If none specified, runs all tests."
    )
    parser.add_argument(
        "--list", 
        action="store_true", 
        help="List available tests and exit"
    )
    
    args = parser.parse_args()
    
    if args.list:
        print("Available tests:")
        print("  1. TTS Format Support")
        print("  2. Streaming TTS")
        print("  3. Audio Cancellation")
        print("\nUsage examples:")
        print("  python audio_test_suite.py     # Run all tests")
        print("  python audio_test_suite.py 1   # Run test 1 only")
        print("  python audio_test_suite.py 1 2 3 # Run tests 1, 2, and 3")
        return
    
    # Check for sample files
    required_files = ["sample.wav", "sample.mp3", "sample.pcm"]
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Missing sample files: {missing_files}")
        print("Please ensure sample.wav, sample.mp3, and sample.pcm are in the current directory.")
        return
    
    # Run the test suite
    suite = AudioTestSuite()
    try:
        await suite.run_tests(args.tests if args.tests else None)
    except KeyboardInterrupt:
        print("\n\n⚠️  Testing interrupted by user")
        suite.print_summary()
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        suite.print_summary()


if __name__ == "__main__":
    asyncio.run(main())
