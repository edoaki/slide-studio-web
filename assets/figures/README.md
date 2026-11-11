# Embedded HTML figure

The feature 03 example embeds the actual figure from
`/Users/aki/Slides/topics/nco/html/nco-overview`.

`nco-overview/figure.mjs`, `_lib/draw.mjs`, `_lib/am-data.mjs`, and
`nco-decoder/figure.mjs` are copied from that source tree. `runtime/` contains
`figure.mjs`, `figure.css`, and `motion.mjs` from
`/Users/aki/Slides/.slide-studio/runtime/`.

The local `nco-overview/index.html`, `style.css`, and `player.mjs` provide the
website player. The player activates the runtime and handles navigation within
the iframe, with click, arrow keys, previous/next buttons, and restart. All seven
steps and the source transitions are preserved. No external assets or server API
are needed; serve the website over HTTP to load JavaScript modules.

To refresh the example, copy the source modules and runtime files above without
overwriting the website player, then check all seven steps in the embedded and
standalone views.
