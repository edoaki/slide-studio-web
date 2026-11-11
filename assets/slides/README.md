# Embedded presentation

`nco-intro.html` is the actual self-contained Slide Studio export of the latest
`nco-intro` presentation. It uses the edited `mist` theme from `multi-sampling`
and the current shared `nco` figures. All 20 pages and all animation steps are
included, without replacing them with screenshots or a recreated slide deck.

The source is the user's `Slides/decks/nco-intro/slides.qmd`, its presentation
CSS, `Slides/themes/mist.css`, and `Slides/topics/nco/`. Preserve the latest source
and rerun the application checks before refreshing this export. The website
loads this file with an iframe, so the standalone HTML is also directly usable.

The iframe uses the exported player's own click, keyboard, overview and
fullscreen controls. The website adds no separate navigation bar. The player
needs no server API and makes no external requests.

## Theme examples

`theme-background.webp` and `theme-attention-overview.webp` show two pages from
this export with the same `mist` theme. They are unaltered 1280 × 720 captures
of `#stage`, encoded as WebP at quality 0.95. The website displays both and
supports opening each at full size.

To refresh them, serve the repository over HTTP and open the exported deck in
an isolated Playwright Chromium browser at 1280 × 720 with Japanese locale and
reduced motion. Wait for `window.deckReady`, find the slides by ID (`background`
for p4 and `am-overview` for Attention Model), then call
`await deck.go(index, Infinity)` and `await deck.settle(index)`. Wait for
`document.fonts.ready` before capturing `#stage`. Both examples show the final
animation step, including the final formula on the Attention Model slide.

## Citation example

`citation-example.webp` shows the final step of `am-overview` from the same
export. It is a lossless 3840 × 2160 WebP capture of `#stage`, taken at a
1280 × 720 viewport with `device_scale_factor=3`. Use the same readiness,
navigation, and font waits as the theme examples above, then capture a PNG
and encode it with Pillow's `lossless=True` option.

Feature 02 displays this full slide and opens the same high-resolution asset
in the image dialog. Do not crop or enlarge the small slide preview inside
`assets/screenshots/editor.webp` for this example.
