# Product screenshots

The screenshots show the current `nco-intro` presentation from the user's
Slide Studio workspace, using the edited `mist` theme used by `multi-sampling`
and the current shared `nco` HTML figures. All 21 pages are preserved.

| Image | Content |
| --- | --- |
| `editor.webp` | The real manuscript editor, Attention Model figure and empty AI chat. |
| `theme.webp` | Theme palette/font controls alongside the current slide. |
| `outline.webp` | The presentation's saved memo, alongside the NCO learning/inference figure. |
| `export.webp` | The actual HTML/PDF export menu. |
| `home.webp` | The current `nco-intro` presentation and bundled themes. |

All captures are 1800 × 1050 pixels, encoded as WebP at quality 0.92.
The capture browser is Playwright's isolated Chromium, with no user browser
profile or AI message. The presentation, its theme and topic were copied to a
clean temporary workspace before opening the app. Existing chats, attachments,
and the other presentation are absent. The copy's manuscript and figures were
not shortened or rewritten for photography. No UI elements or alerts are hidden.

The actual workspace presentation passes the application checks with zero errors
and zero warnings. The source `mist` theme and the fixture's existing figures and
used helper modules have also been updated to the current shared versions.

## Recreate

Use a clean copy of the current presentation, `themes/`, and `topics/nco/` in a
temporary Slide Studio workspace. Do not copy `.slide-studio/chat/` or other
presentations. Start the application against that copy from `../slide-studio`:

```sh
uv run slide-studio --root /path/to/clean-copy --port 4327 --no-browser
```

Then, from this website repository:

```sh
../slide-studio/.venv/bin/python scripts/capture-screenshots.py \
  --url http://127.0.0.1:4327 --deck nco-intro --output assets/screenshots
```

The script only captures the saved presentation. It has no preparation option
that changes or removes source pages. Fix any check issues in the actual source
before recapturing. `--image-format png` provides lossless captures.

The matching standalone presentation is `../slides/nco-intro.html`.
