#!/usr/bin/env python3
"""Capture the real Slide Studio UI in an isolated development browser.

Capture the currently saved presentation without changing its content.
This script never sends an AI message or prepares a shortened demo.

Dependency: playwright. The browser is Playwright's bundled Chromium,
not a running user browser or an existing browser profile.
"""

import argparse
import base64
import json
import time
from pathlib import Path
from urllib.parse import quote

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:4320")
    parser.add_argument("--deck", default="nco-intro")
    parser.add_argument("--output", type=Path, default=Path("assets/screenshots"))
    parser.add_argument("--image-format", choices=["webp", "png"], default="webp")
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    errors = []
    captures = []

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1800, "height": 1050},
            device_scale_factor=1,
            locale="ja-JP",
            reduced_motion="reduce",
        )
        page = context.new_page()
        page.set_default_timeout(15000)
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(f"{args.url.rstrip('/')}/deck/{quote(args.deck)}")
        page.wait_for_function(
            "document.querySelector('#slideBox iframe:not(.loading)')?.contentWindow?.deckReady === true",
            timeout=60000,
        )
        checks_url = f"/api/deck/{quote(args.deck)}/checks"
        deadline = time.monotonic() + 120
        while True:
            status = context.request.get(args.url.rstrip("/") + checks_url).json()
            result = status.get("result")
            if result and not status.get("busy") and not status.get("stale"):
                break
            if time.monotonic() > deadline:
                raise TimeoutError("The current presentation check did not finish")
            page.wait_for_timeout(250)
        if result["errors"] or result["warnings"]:
            raise RuntimeError("Fix demo content before capturing: " + json.dumps({
                "errors": result["errors"], "warnings": result["warnings"]
            }, ensure_ascii=False))
        live_issues = page.evaluate("document.querySelector('#slideBox iframe:not(.loading)').contentWindow.slideStudioLint?.issues || []")
        if live_issues:
            raise RuntimeError("Fix live preview layout before capturing: " + json.dumps(live_issues, ensure_ascii=False))

        def settle():
            page.mouse.move(1790, 1045)
            page.wait_for_timeout(2800)  # Let transient tab toasts and hover tips close.
            page.evaluate("document.fonts.ready")

        def go(title, step=0):
            page.evaluate("""async ([title, step]) => {
                const frame = document.querySelector('#slideBox iframe:not(.loading)');
                const slides = [...frame.contentDocument.querySelectorAll('.slide')];
                const index = slides.findIndex(slide => slide.querySelector('h2')?.textContent.includes(title));
                if (index < 0) throw new Error('Slide not found: ' + title);
                await frame.contentWindow.deck.go(index, step);
            }""", [title, step])
            settle()

        def capture(name):
            settle()
            png = page.screenshot(type="png", animations="disabled")
            target = args.output / f"{name}.{args.image_format}"
            if args.image_format == "webp":
                # Encode the unaltered screenshot using a detached browser canvas.
                # No UI elements are removed, substituted, or composited.
                encoded = page.evaluate("""async encoded => {
                    const image = new Image();
                    image.src = 'data:image/png;base64,' + encoded;
                    await image.decode();
                    const canvas = document.createElement('canvas');
                    canvas.width = image.naturalWidth; canvas.height = image.naturalHeight;
                    canvas.getContext('2d').drawImage(image, 0, 0);
                    return canvas.toDataURL('image/webp', 0.92).split(',')[1];
                }""", base64.b64encode(png).decode())
                target.write_bytes(base64.b64decode(encoded))
            else:
                target.write_bytes(png)
            captures.append(str(target))

        go("Attention Model：概要", 2)
        capture("editor")

        # The standard app control closes the empty chat panel for a closer view.
        page.locator("#chatToggle").click()
        page.get_by_role("tab", name="テーマ", exact=True).click()
        settle()
        capture("theme")

        page.get_by_role("tab", name="下書き", exact=True).click()
        page.locator(".memo-input").wait_for(state="visible")
        page.locator(".memo-input").blur()
        go("NCO：解き方を学習する", 3)
        page.locator(".memo-view").evaluate("node => { node.scrollTop = 0; }")
        capture("outline")

        page.locator('.ptabs [data-tab="qmd"]').click()
        go("Attention Model：概要", 2)
        page.locator('[data-output="build"]').click()
        page.get_by_role("dialog", name="書き出し", exact=True).wait_for(state="visible")
        capture("export")
        page.keyboard.press("Escape")

        page.goto(args.url.rstrip("/") + "/")
        page.locator(".card").first.wait_for(state="visible")
        capture("home")
        context.close()
        browser.close()

    if errors:
        raise RuntimeError("Browser errors: " + json.dumps(errors, ensure_ascii=False))
    print(json.dumps({"viewport": [1800, 1050], "captures": captures, "browser_errors": errors}, ensure_ascii=False))


if __name__ == "__main__":
    main()
