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

def _looks_like_wav(buf: bytes) -> bool:
    return buf[:4] == b"RIFF" and buf[8:12] == b"WAVE"

def _wav_info(blob: "ReadableBuffer") -> tuple[bytes, int, int]:
    """Return (pcm_frames, sample_rate, channels) from a WAV/PCM blob."""
    with wave.open(io.BytesIO(blob), "rb") as wf:
        rate, nch, nframes, sw = wf.getframerate(), wf.getnchannels(), wf.getnframes(), wf.getsampwidth()
        if sw != 2:
            raise ValueError(f"Only 16‑bit PCM WAV supported (got {sw*8}‑bit)")
        return wf.readframes(nframes), rate, nch


def _open_stream(sample_rate: int, n_channels: int, callback=None, on_done=None):
    return sd.RawOutputStream(
        samplerate=sample_rate,
        channels=n_channels,
        dtype=_S16_DTYPE,
        callback=callback,
        finished_callback=on_done,
    )


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
    elif _looks_like_wav(first):
        await _stream_wav(chunks, first)
    else:
        await _stream_pcm(chunks, 48000, 1)

async def _stream_pcm(
    pcm_chunks: AsyncIterable[bytes],
    sample_rate: int,
    n_channels: int,
) -> None:
    """Generic PCM player: pulls raw PCM from chunks and plays via sounddevice."""
    _need_deps()
    loop = asyncio.get_running_loop()
    done_evt = asyncio.Event()

    def finished():
        loop.call_soon_threadsafe(done_evt.set)

    pcm_q: queue.Queue[Optional[bytes]] = queue.Queue(maxsize=8)

    # pump PCM into the queue
    async def feeder():
        async for data in pcm_chunks:
            pcm_q.put(data)
        pcm_q.put(None)

    # consume queue in sounddevice callback
    async def player():
        buf = b""
        def cb(outdata, frames, *_):
            nonlocal buf
            need = frames * n_channels * _BYTES_PER_SAMP
            while len(buf) < need:
                part = pcm_q.get()
                if part is None:
                    raise sd.CallbackStop
                buf += part
            outdata[:] = buf[:need]
            buf = buf[need:]

        with _open_stream(sample_rate, n_channels, callback=cb, on_done=finished):
            await done_evt.wait()

    await asyncio.gather(feeder(), player())

async def _stream_wav(
    chunks: AsyncIterable[bytes],
    first: bytes,
) -> None:
    # build header + ensure we have 44 bytes
    header = bytearray(first)
    ait = chunks.__aiter__()
    while len(header) < 44:
        header.extend(await anext(ait))

    frames0, sample_rate, n_channels = _wav_info(header)

    async def pcm_gen():
        yield frames0
        async for c in ait:
            yield c

    await _stream_pcm(pcm_gen(), sample_rate, n_channels)

async def _stream_mp3(
    chunks: AsyncIterable[bytes],
    first: bytes,
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

    ait = chunks.__aiter__()

    # feed MP3 into ffmpeg
    async def feed():
        assert proc.stdin
        proc.stdin.write(first)
        async for chunk in ait:
            proc.stdin.write(chunk)
            await proc.stdin.drain()
        proc.stdin.close()

    async def pcm_gen():
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

    await _stream_pcm(pcm_gen(), 48_000, 2)

