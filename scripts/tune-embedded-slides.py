#!/usr/bin/env python3
"""Reapply website playback settings after replacing the Slide Studio export."""
import html
import base64
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
      frames.push(...(sequence?.length ? sequence : [{markup: figure.renderStep(i + 1), duration: 650}]));
    }
    // Runtime holds BEFORE the next frame: let each completed state remain
    // readable for 750 ms, then give the next operation 650 ms to move.
    // The last state remains visible until the next user input.
    return frames.map((f, i) => ({...f, duration: 650, hold: i === 0 ? 0 : 750}));
  }
};
mount(playback);"""
STYLE = """<style id="website-playback-selection">
#stage { -webkit-user-select: none; user-select: none; }
#stage img { -webkit-user-drag: none; }
</style>"""

SOLVER_TRANSITION = """
 transition(from,to){
  if(to!==from+1)return null;
  const frames=[];
  for(let t=states[from]+1;t<=states[to];t++){
   // These partial leaf states become numeric results immediately afterward.
   // Reveal the completed leaf directly, without flashing an unresolved label.
   if([5,8,12,13].includes(t))continue;
   frames.push({markup:scene(t),duration:650});
  }
  return frames;
 }};
"""
NEAREST_TRANSITION = """
 transition(from,to){
  if(to!==from+1)return null;
  if(to===1)return decide(0);
  if(to===2){
   const frames=[];
   // Every remaining city gets the same comparison and selection phases.
   // Do not insert brief candidate-fade states between decisions.
   for(let i=1;i<n-1;i++)frames.push(...decide(i));
   return [...frames,{markup:scene(state(2)),duration:650}];
  }
  return null;
 }};
"""


def tune_figure(match):
    module = base64.b64decode(match[1]).decode()
    if "id:'F22'" in module:
        scene = Path(__file__).with_name('nearest-neighbor-scene.mjs').read_text()
        module, count = re.subn(r'function scene\(.*?(?=\nconst state=)',
                                lambda _: scene[scene.index('function scene('):], module, flags=re.S)
        if count != 1:
            raise ValueError('Expected one nearest-neighbor scene')
        module = module.replace('const state=k=>[{},',
                                'const state=k=>[{moves:0,decision:0,picked:false},')
    transition = (SOLVER_TRANSITION if "id:'F21'" in module else
                  NEAREST_TRANSITION if "id:'F22'" in module else None)
    if transition:
        module, count = re.subn(r'\n transition\(from,to\).*\Z',
                                lambda _: transition, module, flags=re.S)
        if count != 1:
            raise ValueError('Expected one figure transition implementation')
    return match[0].replace(match[1], base64.b64encode(module.encode()).decode())


def main():
    source = DECK.read_text()
    def tune(match):
        frame = html.unescape(match[1])
        frame = re.sub(r"import figure from 'data:text/javascript;base64,([A-Za-z0-9+/=]+)'",
                       tune_figure, frame)
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
