#!/usr/bin/env python3
"""Check embedded playback timing and transient labels (requires Node.js)."""
import html
from pathlib import Path
import re
import subprocess
import tempfile

source = (Path(__file__).resolve().parents[1] / 'assets/slides/nco-intro.html').read_text()
pattern = r'data-slide-studio-fig="nco/(?:solver-bnb|heuristic-nn|metaheuristic-2opt)"[^>]*><iframe srcdoc="(.*?)"'
frames = re.findall(pattern, source, re.S)
assert len(frames) == 3
with tempfile.TemporaryDirectory(prefix='slide-playback-check-') as directory:
    paths = []
    for i, frame in enumerate(frames):
        script = re.search(r'<script type="module">(.*?)</script>', html.unescape(frame), re.S)[1]
        script, count = re.subn(r"import \{mount\} from '[^']+';", '', script)
        assert count == 1
        assert script.count('mount(playback);') == 1
        script = script.replace('mount(playback);', 'export {playback};')
        path = Path(directory) / f'{i}.mjs'
        path.write_text(script)
        paths.append(path.as_uri())
    subprocess.run(['node', '--input-type=module', '-', *paths], input="""
import assert from 'node:assert/strict';
for (const path of process.argv.slice(2)) {
  const {playback: p} = await import(path);
  assert.equal(p.steps.length, {F21: 5, F22: 4, F23: 3}[p.id]);
  for (let k = 1; k < p.steps.length; k++) {
    const frames = p.transition(k - 1, k);
    assert.ok(frames.length);
    frames.forEach((f, i) => {
      assert.ok(f.duration > 500, `${p.id}: motion too brief`);
      if (i) assert.ok(f.hold > 500, `${p.id}: completed state too brief`);
      if (p.id === 'F21') {
        assert.ok(!/tree-value-(?:aab|aba|ba)-未確定/.test(f.markup),
          'Do not flash unresolved labels on leaves before their numeric result');
      }
    });
    assert.equal(frames.at(-1).markup, p.renderStep(k));
    assert.equal(p.transition(k, k - 1)[0].markup, p.renderStep(k - 1));
    if (p.id === 'F22' && k === 2) {
      // Three remaining decisions each need comparison + selection, then return.
      assert.equal(frames.length, 7);
      assert.ok(frames.reduce((sum, f) => sum + f.duration + f.hold, 0) > 9000);
    }
  }
  console.log(`${p.id}: timing, stops, labels and destination states OK`);
}
""", text=True, check=True)
