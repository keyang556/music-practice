# music-practice

以 [music21](https://www.music21.org/) 產生「兩隻老虎」旋律 MIDI 檔的小工具。

## 需求

- Python 3.10 以上
- music21（見 `requirements.txt`）

## 安裝

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt
```

## 使用

```bash
python two_tigers.py                    # 產生 two_tigers.mid
python two_tigers.py -o out/tiger.mid   # 指定輸出路徑
python two_tigers.py --tempo 100        # 指定速度 (BPM，須大於 0)
```

旋律資料以樂句為單位放在 `two_tigers.py` 的 `PHRASES`，可直接修改音高與時值。
`build_part` / `build_score` / `write_midi` 分開，方便在其他程式裡重用樂譜或輸出成別的格式。
