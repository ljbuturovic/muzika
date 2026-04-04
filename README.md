# muziqa

Analyze your music collection and plot two side-by-side charts: top artists and tracks by year.

![Top 20 Artists chart](artists.png)

## Install

```
pipx install muziqa
```

## Usage

Point it at a folder of music files (MP3, FLAC, WAV):

```
$ muziqa --folder /path/to/music
```

This reads the tags from every supported file in the folder and saves a bar chart to `artists.png` in the current directory.

### Options

| Option | Description |
|--------|-------------|
| `--folder DIR` | Directory of MP3/FLAC/WAV files (reads tags) |
| `--recursive` | Search all subfolders recursively (only with `--folder`) |
| `--artists FILE` | Path to a plain-text `artists.txt` file instead |
| `--output FILE` | Output image filename (default: `artists.png`) |
| `--top N` | Number of top artists to show (default: 20) |

### Examples

```
$ muziqa --folder ~/Music
$ muziqa --folder ~/Music --recursive
$ muziqa --folder ~/Music --top 30 --output top30.png
$ muziqa --artists artists.txt
```
