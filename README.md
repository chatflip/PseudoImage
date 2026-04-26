# PseudoImage

## Description

## Requirement

- Python >= 3.8, < 3.10（`pyproject.toml` の `requires-python` に合わせる）
- [uv](https://docs.astral.sh/uv/)

## Installation

本番用のみ（開発ツールを入れない）:

```bash
uv sync --no-group dev
```

開発用ツール（pysen など）も入れる:

```bash
uv sync
```

## Usage

1. Move image to the images folder
2. `uv run python src/main.py`（仮想環境を有効化済みなら `python src/main.py` でも可）
