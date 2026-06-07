# yomikomi_hyakkei · tools

## Corpus SSoT (Gate A eval)

| 文件 | 用途 |
|------|------|
| `data/corpus/gatea_preface_a001_ja.txt` | **Eval SSoT** · committed plain text |
| `data/corpus/gatea_preface_a001_ja.manifest.json` | char count · sha256 · markers |
| `config/quota_phase1.json` | `corpus.txt` + `expected_sha256` |

HTML (`../GateA_样张MVP_20260610/*.html`) is display/PDF only and may be empty on clone.

### Regenerate TXT from HTML

```bash
cd yomikomi_hyakkei
python tools/extract_corpus_from_html.py --write --update-manifest
# If sha changed, update config/quota_phase1.json expected_sha256
python -m unittest discover -s tests -q
```

## Main entrypoints

| Script | Purpose |
|--------|---------|
| `run_phase1.py` | Phase 1 dry-run / live eval |
| `corpus_loader.py` | Load + validate corpus (txt primary) |
| `eval_worker.py` | Persona evaluation worker |
| `extract_corpus_from_html.py` | Regenerate txt from GateA HTML |
