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
