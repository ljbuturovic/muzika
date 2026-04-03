# muziqa

Analyze your MP3 collection and plot a chart of your most-listened-to artists.

![Top 20 Artists chart](artists.png)

## Install

```
pipx install muziqa
```

## Usage

Point it at a folder of MP3 files:

```
$ muziqa --mp3 /path/to/music
```

This reads the ID3 tags from every `.mp3` file in the folder and saves a bar chart to `artists.png` in the current directory.

### Options

| Option | Description |
|--------|-------------|
| `--mp3 DIR` | Directory of MP3 files (reads ID3 tags) |
| `--artists FILE` | Path to a plain-text `artists.txt` file instead |
| `--output FILE` | Output image filename (default: `artists.png`) |
| `--top N` | Number of top artists to show (default: 20) |

### Examples

```
$ muziqa --mp3 ~/Music
$ muziqa --mp3 ~/Music --top 30 --output top30.png
$ muziqa --artists artists.txt
```
