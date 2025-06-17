# Tsrc/hume/empathic_voice/chat/audio/audio_utilities.pyHIS FILE IS MANUALLY MAINTAINED: see .fernignore
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
_DEFAULT_BLOCKSIZE = 256

def _looks_like_mp3(buf: bytes) -> bool:
    return buf[:3] == b"ID3" or buf[:2] in (b"\xff\xfb", b"\xff\xf3", b"\xff\xf2")

def _looks_like_wav(buf: bytes) -> bool:
    return buf[:4] == b"RIFF" and buf[8:12] == b"WAVE"

def _wav_info(blob: "ReadableBuffer") -> tuple[bytes, int, int]:
    """Return (pcm_frames, sample_rate, channels) from a WAV/PCM blob."""
    with wave.open(io.BytesIO(blob), "rb") as wf:
        rate, nch, nframes, sw = wf.getframerate(), wf.getnchannels(), wf.getnframes(), wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"Only 16‑bit PCM WAV supported (got {sw*8}‑bit)")
        return wf.readframes(nframes), rate, nch


async def play_audio(
    blob: bytes,
    *,
    device: Optional[int] = None,
    blocksize = None
) -> None:
    async def _one_chunk():
        yield blob
    await play_audio_streaming(_one_chunk().__aiter__(), device=device, blocksize=blocksize)


async def play_audio_streaming(
    chunks: AsyncIterable[bytes],
    *, 
    device: Optional[int] = None,
    blocksize: Optional[int] = None,
) -> None:
    _need_deps()
    iterator = chunks.__aiter__()
    first = await iterator.__anext__()

    if _looks_like_mp3(first):
        await _stream_mp3(chunks, first, device=device)
    elif _looks_like_wav(first):
        await _stream_wav(chunks, first, device=device)
    else:
        async def _reassembled():
            yield first
            async for chunk in chunks:
                yield chunk
        await _stream_pcm(_reassembled(), 48000, 1, device=device, blocksize=blocksize)

async def _stream_pcm(
    pcm_chunks: AsyncIterable[bytes],
    sample_rate: int,
    n_channels: int,
    device: Optional[int] = None,
    blocksize: Optional[int] = _DEFAULT_BLOCKSIZE,
) -> None:
    """Generic PCM player: pulls raw PCM from chunks and plays via sounddevice."""
    _need_deps()
    loop = asyncio.get_running_loop()
    done_event = asyncio.Event()

    def finished():
        loop.call_soon_threadsafe(done_event.set)

    pcm_queue: queue.Queue[Optional[bytes]] = queue.Queue(maxsize=32)

    # pump PCM into the queue
    async def feeder():
        async for data in pcm_chunks:
            pcm_queue.put(data)
        pcm_queue.put(None)

    # consume queue in sounddevice callback
    async def player():
        buf = b""
        def cb(outdata, frames, *_):
            nonlocal buf
            need = frames * n_channels * _BYTES_PER_SAMP
            while len(buf) < need:
                part = pcm_queue.get()
                if part is None:
                    raise sd.CallbackStop
                buf += part
            outdata[:] = buf[:need]
            buf = buf[need:]

        with sd.RawOutputStream(
          samplerate=sample_rate,
          channels=n_channels,
          dtype=_S16_DTYPE,
          callback=cb,
          blocksize=blocksize,
          device=device,
          finished_callback=finished):
            await done_event.wait()

    await asyncio.gather(feeder(), player())

async def _stream_wav(
    chunks: AsyncIterable[bytes],
    first: bytes,
    device: Optional[int] = None,
) -> None:
    # build header + ensure we have 44 bytes
    header = bytearray(first)
    iterator = chunks.__aiter__()
    while len(header) < 44:
        header.extend(await iterator.__anext__())

    frames0, sample_rate, n_channels = _wav_info(header)

    async def pcm_gen():
        yield frames0
        async for c in iterator:
            yield c

    await _stream_pcm(pcm_gen(), sample_rate, n_channels, device=device)

async def _stream_mp3(
    chunks: AsyncIterable[bytes],
    first: bytes,
    device: Optional[int] = None,
) -> None:
    cmd = (
        "ffmpeg -hide_banner -loglevel error -i pipe:0 "
        "-f s16le -acodec pcm_s16le -ac 2 -ar 48000 -"
    )
    proc = await asyncio.create_subprocess_exec(
        *shlex.split(cmd),
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
    )

    iterator = chunks.__aiter__()

    # feed MP3 into ffmpeg
    async def feed():
        assert proc.stdin
        proc.stdin.write(first)
        async for chunk in iterator:
            proc.stdin.write(chunk)
            await proc.stdin.drain()
        proc.stdin.close()

    async def pcm_generator():
        assert proc.stdout
        # start feeding in background
        feed_task = asyncio.create_task(feed())
        # yield decoded PCM as it comes
        while True:
            data = await proc.stdout.read(8192)
            if not data:
                break
            yield data
        await feed_task
        await proc.wait()

    await _stream_pcm(pcm_generator(), 48_000, 2, device=device)
