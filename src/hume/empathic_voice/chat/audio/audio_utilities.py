# THIS FILE IS MANUALLY MAINTAINED: see .fernignore
"""
* WAV/PCM handled with `wave` module
* MP3 decoded by shelling out to ffmpeg (`ffmpeg` must be in $PATH)
"""

from __future__ import annotations
import asyncio, io, wave, queue, shlex
from typing import TYPE_CHECKING, AsyncIterable, Optional

_missing: Optional[Exception] = None
try:
    import sounddevice as sd  # type: ignore
except ModuleNotFoundError as exc:
    _missing = exc

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer
    import sounddevice as sd  # type: ignore

def _need_deps() -> None:
    if _missing:
        raise RuntimeError(
            'pip install "hume[microphone]" ‑‑ or drop audio playback entirely'
        ) from _missing


_S16_DTYPE = "int16"
_BYTES_PER_SAMP = 2

def _looks_like_mp3(buf: bytes) -> bool:
    return buf[:3] == b"ID3" or buf[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")


def _wav_info(blob: "ReadableBuffer") -> tuple[bytes, int, int]:
    """Return (pcm_frames, sample_rate, channels) from a WAV/PCM blob."""
    with wave.open(io.BytesIO(blob), "rb") as wf:
        rate, nch, nframes, sw = wf.getframerate(), wf.getnchannels(), wf.getnframes(), wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"Only 16‑bit PCM WAV supported (got {sw*8}‑bit)")
        return wf.readframes(nframes), rate, nch


def _open_stream(sr: int, ch: int, callback=None, on_done=None):
    return sd.RawOutputStream(
        samplerate=sr,
        channels=ch,
        dtype=_S16_DTYPE,
        callback=callback,
        finished_callback=on_done,
    )


# ---------------- one‑shot playback ----------------
async def play_audio(blob: bytes) -> None:
    async def _one_chunk():
        yield blob
    await play_audio_streaming(_one_chunk().__aiter__())

async def play_audio_streaming(
    chunks: AsyncIterable[bytes],
) -> None:
    _need_deps()
    first = await anext(chunks.__aiter__())          # may raise StopAsyncIteration

    if _looks_like_mp3(first):
        await _stream_mp3(chunks, first)
    else:
        await _stream_wav(chunks, first)


# ---- internal streamers ------------------------------------------------------
async def _stream_mp3(chunks: AsyncIterable[bytes], first: bytes) -> None:
    """Feed MP3 bytes to ffmpeg and pump decoded PCM to speakers."""
    cmd = (
        "ffmpeg -hide_banner -loglevel error -i pipe:0 "
        "-f s16le -acodec pcm_s16le -ac 2 -ar 48000 -"
    )
    proc = await asyncio.create_subprocess_exec(
        *shlex.split(cmd),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )

    # -- async tasks: feed stdin / consume stdout --
    async def feed():
        assert proc.stdin
        proc.stdin.write(first)
        async for chunk in chunks:
            proc.stdin.write(chunk)
            await proc.stdin.drain()
        proc.stdin.close()

    pcm_q: queue.Queue[Optional[bytes]] = queue.Queue(maxsize=8)

    async def drain():
        assert proc.stdout
        while True:
            data = await proc.stdout.read(8192)
            if not data:
                break
            pcm_q.put(data)
        pcm_q.put(None)

    async def play():
        loop = asyncio.get_running_loop()
        done_evt = asyncio.Event()

        def finished():
            loop.call_soon_threadsafe(done_evt.set)

        # feed bytes to RawOutputStream inside callback
        buf = b""

        def cb(outdata, frames, *_):
            nonlocal buf
            need = frames * 2 * 2  # 2 channels * 2 bytes
            while len(buf) < need:
                part = pcm_q.get()
                if part is None:
                    raise sd.CallbackStop
                buf += part
            outdata[:] = buf[:need]
            buf = buf[need:]

        with _open_stream(48_000, 2, callback=cb, on_done=finished):
            await done_evt.wait()

    await asyncio.gather(feed(), drain(), play())
    await proc.wait()


async def _stream_wav(chunks: AsyncIterable[bytes], first: bytes) -> None:
    """
    Stream WAV (16‑bit PCM) chunks.

    Header must be entirely in `first`.
    """
    header = bytearray(first)
    # Ensure header is complete (44 bytes min); read until then
    while len(header) < 44:
        header.extend(await anext(chunks.__aiter__()))

    frames0, sr, ch = _wav_info(header)
    pcm_q: queue.Queue[Optional[bytes]] = queue.Queue(maxsize=8)
    pcm_q.put(frames0)

    async def feeder():
        async for c in chunks:
            pcm_q.put(c)
        pcm_q.put(None)

    async def player():
        loop = asyncio.get_running_loop()
        done = asyncio.Event()

        def finished():
            loop.call_soon_threadsafe(done.set)

        buf = b""

        def cb(outdata, frames, *_):
            nonlocal buf
            need = frames * ch * _BYTES_PER_SAMP
            while len(buf) < need:
                part = pcm_q.get()
                if part is None:
                    raise sd.CallbackStop
                buf += part
            outdata[:] = buf[:need]
            buf = buf[need:]

        with _open_stream(sr, ch, callback=cb, on_done=finished):
            await done.wait()

    await asyncio.gather(feeder(), player())
