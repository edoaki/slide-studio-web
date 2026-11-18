#!/usr/bin/env python3
"""Reapply website playback settings after replacing the Slide Studio export."""
import html
import re
from pathlib import Path

DECK = Path(__file__).resolve().parents[1] / 'assets/slides/nco-intro.html'
POLICY = """// Website playback: stop at explanations/results, keep intermediate motion automatic.
const stops = figure.id === 'F21' ? [0, 4, 5, 6, 7] : figure.steps.map((_, i) => i);
const playback = {
  ...figure,
  steps: stops.map(i => figure.steps[i]),
  renderStep: k => figure.renderStep(stops[k]),
  transition(from, to) {
    if (to !== from + 1) return [{markup: figure.renderStep(stops[to]), duration: 0}];
    const frames = [];
    for (let i = stops[from]; i < stops[to]; i++) {
      const sequence = figure.transition?.(i, i + 1);
      frames.push(...(sequence?.length ? sequence : [{markup: figure.renderStep(i + 1), duration: 220}]));
    }
    const total = frames.reduce((sum, f) => sum + (f.duration ?? 220) + (f.hold ?? 0), 0);
    const scale = Math.min(1, 900 / Math.max(1, total));
    return frames.map(f => ({...f, duration: (f.duration ?? 220) * scale, hold: (f.hold ?? 0) * scale}));
  }
};
mount(playback);"""
STYLE = """<style id="website-playback-selection">
#stage { -webkit-user-select: none; user-select: none; }
#stage img { -webkit-user-drag: none; }
</style>"""


def main():
    source = DECK.read_text()
    def tune(match):
        frame = html.unescape(match[1])
        if 'mount(playback);' in frame:
            frame = re.sub(r'// Website playback:.*?mount\(playback\);', lambda _: POLICY, frame, flags=re.S)
        else:
            if frame.count('mount(figure);') != 1:
                raise ValueError('Expected a single figure mount')
            frame = frame.replace('mount(figure);', POLICY)
        return match[0].replace(match[1], html.escape(frame, quote=True))

    # Match only the three solving-method figures; preserve every other embedded asset.
    pattern = r'data-slide-studio-fig="nco/(?:solver-bnb|heuristic-nn|metaheuristic-2opt)"[^>]*><iframe srcdoc="(.*?)"'
    source, count = re.subn(pattern, tune, source, flags=re.S)
    if count != 3:
        raise ValueError(f'Expected three solving-method figures, found {count}')
    if 'id="website-playback-selection"' not in source:
        source = source.replace('</head>', STYLE + '\n</head>', 1)
    DECK.write_text(source)


if __name__ == '__main__':
    main()
