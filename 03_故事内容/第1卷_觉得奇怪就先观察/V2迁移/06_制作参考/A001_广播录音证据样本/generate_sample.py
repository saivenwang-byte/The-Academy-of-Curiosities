#!/usr/bin/env python3
"""Generate A001 broadcast evidence WAV samples (full rehearsal + hard-cut broadcast).

Uses synthesized tone bursts as speech placeholders — replace with licensed
voice recordings for production. Safe for repo/demo without real student audio.
"""

from __future__ import annotations

import math
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 32000
OUT_DIR = Path(__file__).resolve().parent


def synth_syllable(duration_s: float, freq: float = 220.0, amp: float = 0.25) -> list[float]:
    n = int(SAMPLE_RATE * duration_s)
    return [amp * math.sin(2 * math.pi * freq * i / SAMPLE_RATE) for i in range(n)]


def silence(duration_s: float) -> list[float]:
    return [0.0] * int(SAMPLE_RATE * duration_s)


def concat(parts: list[list[float]]) -> list[float]:
    out: list[float] = []
    for p in parts:
        out.extend(p)
    return out


def write_wav(path: Path, samples: list[float]) -> None:
    with wave.open(str(path), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(SAMPLE_RATE)
        frames = b"".join(
            struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples
        )
        wf.writeframes(frames)


def main() -> None:
    # Placeholder "syllables" — different freqs suggest phrase rhythm
    full = concat(
        [
            synth_syllable(0.15, 180),
            synth_syllable(0.12, 200),
            synth_syllable(0.18, 210),
            synth_syllable(0.14, 190),
            synth_syllable(0.20, 230),
            synth_syllable(0.16, 220),
            synth_syllable(0.22, 240),
            synth_syllable(0.18, 210),
        ]
    )

    # Hard cut: skip opening ~0.45s equivalent — start mid-phrase
    cut_start = int(SAMPLE_RATE * 0.45)
    broadcast_cut = full[cut_start:]

    write_wav(OUT_DIR / "rehearsal_full.wav", full)
    write_wav(OUT_DIR / "broadcast_cut.wav", broadcast_cut)

    spec = OUT_DIR / "waveform_spec.md"
    spec.write_text(
        """# A001 波形标注 · FC-3

## rehearsal_full.wav

- 全长约 {:.2f}s · 模拟完整句「迟到的人不该参加今天的彩排」
- 起振点 t=0 · 连续音节

## broadcast_cut.wav

- 硬切起点 **t≈0.45s**（删去前导音节）
- 波形在 cut 点 **振幅突变** · 无 crossfade → FC-3「跳播/硬切」
- 听众 familiar timbre 但 **语境缺失**

## 正文对照

- FC-4：完整句含「迟到者/彩排」· 播出仅中间段
""".format(len(full) / SAMPLE_RATE),
        encoding="utf-8",
    )

    print(f"Wrote {OUT_DIR / 'rehearsal_full.wav'}")
    print(f"Wrote {OUT_DIR / 'broadcast_cut.wav'}")
    print(f"Wrote {spec}")


if __name__ == "__main__":
    main()
