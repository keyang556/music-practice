"""以 music21 產生「兩隻老虎」旋律的 MIDI 檔。

用法:
    python two_tigers.py                    # 產生 two_tigers.mid
    python two_tigers.py -o out/tiger.mid   # 指定輸出路徑
    python two_tigers.py --tempo 100        # 指定速度 (BPM)
"""

from __future__ import annotations

import argparse
from pathlib import Path

from music21 import instrument, metadata, note, stream, tempo

# --- 樂曲設定 -------------------------------------------------------------

TITLE = "兩隻老虎"
DEFAULT_TEMPO = 120          # BPM
DEFAULT_OUTPUT = Path("two_tigers.mid")

# 旋律樂句：每個樂句是 (歌詞, [(音高, 時值), ...])
# 時值以四分音符為 1.0。分成樂句是為了好讀、好修改。
PHRASES: list[tuple[str, list[tuple[str, float]]]] = [
    ("兩隻老虎", [("C4", 1.0), ("D4", 1.0), ("E4", 1.0), ("C4", 1.0)]),
    ("兩隻老虎", [("C4", 1.0), ("D4", 1.0), ("E4", 1.0), ("C4", 1.0)]),
    ("跑得快", [("E4", 1.0), ("F4", 1.0), ("G4", 2.0)]),
    ("跑得快", [("E4", 1.0), ("F4", 1.0), ("G4", 2.0)]),
    ("一隻沒有耳朵", [("G4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 0.5),
                 ("E4", 1.0), ("C4", 1.0)]),
    ("一隻沒有尾巴", [("G4", 0.5), ("A4", 0.5), ("G4", 0.5), ("F4", 0.5),
                 ("E4", 1.0), ("C4", 1.0)]),
    ("真奇怪", [("C4", 1.0), ("G3", 1.0), ("C4", 2.0)]),
    ("真奇怪", [("C4", 1.0), ("G3", 1.0), ("C4", 2.0)]),
]


# --- 建構流程 -------------------------------------------------------------

def build_part(phrases=PHRASES, bpm: int = DEFAULT_TEMPO) -> stream.Part:
    """把樂句資料轉成一個 music21 Part（單一旋律聲部）。"""
    part = stream.Part()
    part.append(instrument.Piano())
    part.append(tempo.MetronomeMark(number=bpm))

    for lyric, pitches in phrases:
        for index, (pitch_name, quarter_length) in enumerate(pitches):
            n = note.Note(pitch_name, quarterLength=quarter_length)
            if index == 0:
                n.lyric = lyric      # 每個樂句的第一個音附上歌詞備註
            part.append(n)
    return part


def build_score(phrases=PHRASES, bpm: int = DEFAULT_TEMPO) -> stream.Score:
    """組出完整樂譜（含標題等中繼資料）。"""
    score = stream.Score()
    score.metadata = metadata.Metadata(title=TITLE, composer="Traditional")
    score.append(build_part(phrases, bpm))
    return score


def write_midi(score: stream.Score, output: Path) -> Path:
    """把樂譜寫成 MIDI 檔，回傳實際輸出路徑。"""
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    score.write("midi", fp=str(output))
    return output


# --- 命令列介面 -----------------------------------------------------------

def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"產生「{TITLE}」MIDI 檔")
    parser.add_argument("-o", "--output", type=Path, default=DEFAULT_OUTPUT,
                        help=f"輸出的 MIDI 檔路徑（預設 {DEFAULT_OUTPUT}）")
    parser.add_argument("-t", "--tempo", type=int, default=DEFAULT_TEMPO,
                        help=f"速度 BPM（預設 {DEFAULT_TEMPO}）")
    return parser.parse_args(argv)


def main(argv=None) -> None:
    args = parse_args(argv)
    score = build_score(bpm=args.tempo)
    path = write_midi(score, args.output)
    total_beats = sum(d for _, ns in PHRASES for _, d in ns)
    print(f"已輸出 {path.resolve()}（{total_beats:g} 拍 / {args.tempo} BPM）")


if __name__ == "__main__":
    main()
