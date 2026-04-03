#!/usr/bin/env python3
"""Analyze artists from artists.txt or directly from MP3 ID3 tags.

Usage:
  analyze_artists.py --artists artists.txt
  analyze_artists.py --mp3 /path/to/music/dir
"""

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


def parse_artists_txt(filepath: str) -> Counter:
    pattern = re.compile(r"Artist:\s*(.+?)\s*,\s*Year:")
    counts: Counter = Counter()
    with open(filepath, encoding="utf-8") as f:
        for line in f:
            m = pattern.search(line)
            if m:
                name = m.group(1).strip()
                if name:
                    counts[name] += 1
    return counts


def parse_artists_mp3(directory: str) -> Counter:
    from mutagen.id3 import ID3, ID3NoHeaderError

    counts: Counter = Counter()
    mp3_files = list(Path(directory).glob("*.mp3"))
    if not mp3_files:
        print(f"No MP3 files found in {directory}")
        sys.exit(1)

    print(f"Reading ID3 tags from {len(mp3_files):,} files…", flush=True)
    for path in mp3_files:
        try:
            tags = ID3(path)
            artist = tags.get("TPE1")  # Lead artist / band
            if artist:
                name = str(artist).strip()
                if name:
                    counts[name] += 1
        except ID3NoHeaderError:
            pass  # No ID3 header — skip silently
        except Exception:
            pass

    return counts


def plot_top20(counts: Counter, output: str = "artists.png", top: int = 20) -> None:
    top_artists = counts.most_common(top)
    if len(top_artists) < top:
        print(f"Warning: only {len(top_artists)} artists found.")
    artists, values = zip(*top_artists)

    # Reverse so highest is at top
    artists = artists[::-1]
    values = values[::-1]

    fig, ax = plt.subplots(figsize=(12, 8))
    fig.patch.set_facecolor("#0f0f1a")
    ax.set_facecolor("#0f0f1a")

    cmap = plt.colormaps["plasma"]
    n = len(values)
    colours = [cmap(i / (n - 1)) for i in range(n)]

    bars = ax.barh(range(n), values, color=colours, edgecolor="none", height=0.72)

    for bar, val in zip(bars, values):
        ax.text(
            bar.get_width() + 0.15,
            bar.get_y() + bar.get_height() / 2,
            str(val),
            va="center",
            ha="left",
            color="#e0e0e0",
            fontsize=9,
            fontweight="bold",
        )

    ax.set_yticks(range(n))
    ax.set_yticklabels(artists, fontsize=10.5, color="#e0e0e0")
    ax.tick_params(axis="x", colors="#666680", labelsize=9)
    ax.tick_params(axis="y", length=0)

    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#333350")
    ax.set_xlabel("Tracks", labelpad=8, color="#888899")

    total = sum(counts.values())
    unique = len(counts)
    ax.set_title(
        f"Top {top} Artists  ·  {total:,} tracks  ·  {unique:,} unique artists",
        fontsize=13,
        fontweight="bold",
        color="#c8c8e0",
        pad=14,
    )

    ax.xaxis.grid(True, color="#222240", linewidth=0.6, zorder=0)
    ax.set_axisbelow(True)

    plt.tight_layout()

    plt.savefig(output, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"Saved → {output}")
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Plot top 20 artists from artists.txt or MP3 ID3 tags."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--artists", metavar="FILE", help="Path to artists.txt")
    group.add_argument("--mp3", metavar="DIR", help="Directory of MP3 files (reads ID3 tags)")
    parser.add_argument("--output", metavar="FILE", default="artists.png", help="Output image file (default: artists.png)")
    parser.add_argument("--top", metavar="N", type=int, default=20, help="Number of top artists to plot (default: 20)")
    args = parser.parse_args()

    if args.mp3:
        counts = parse_artists_mp3(args.mp3)
    else:
        counts = parse_artists_txt(args.artists)

    if not counts:
        print("No artist data found.")
        sys.exit(1)

    plot_top20(counts, args.output, args.top)


if __name__ == "__main__":
    main()
