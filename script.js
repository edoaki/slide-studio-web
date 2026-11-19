"use strict";

const dialog = document.getElementById("image-dialog");
const dialogImage = document.getElementById("dialog-image");
const dialogCaption = document.getElementById("dialog-caption");
let previousOverflow = "";

document.querySelectorAll("[data-zoom]").forEach((button) => {
  button.addEventListener("click", () => {
    dialogImage.src = button.dataset.zoom;
    dialogImage.alt = button.dataset.alt || button.querySelector("img").alt;
    dialogCaption.textContent = button.dataset.caption;
    previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    dialog.showModal();
  });
});

document.getElementById("close-dialog").addEventListener("click", () => dialog.close());
dialog.addEventListener("click", (event) => {
  const bounds = dialog.getBoundingClientRect();
  if (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom) dialog.close();
});
dialog.addEventListener("close", () => {
  document.body.style.overflow = previousOverflow;
});

const copyButton = document.getElementById("copy-command");
const copyStatus = document.getElementById("copy-status");
const command = "git clone --branch migration/electron https://github.com/edoaki/slide-studio.git\ncd slide-studio\nnpm install\nnpm start";
let resetCopyState;

copyButton.addEventListener("click", async () => {
  clearTimeout(resetCopyState);
  try {
    await navigator.clipboard.writeText(command);
    copyButton.querySelector("span").textContent = "コピーしました";
    copyButton.querySelector("use").setAttribute("href", "#i-check");
    copyStatus.textContent = "導入コマンドをクリップボードにコピーしました。";
  } catch {
    copyButton.querySelector("span").textContent = "手動でコピー";
    copyStatus.textContent = "コピーできませんでした。コードを選択してコピーしてください。";
    const selection = window.getSelection();
    const range = document.createRange();
    range.selectNodeContents(document.querySelector(".terminal code"));
    selection.removeAllRanges();
    selection.addRange(range);
  }
  resetCopyState = setTimeout(() => {
    copyButton.querySelector("span").textContent = "コピー";
    copyButton.querySelector("use").setAttribute("href", "#i-copy");
    copyStatus.textContent = "";
  }, 3500);
});

// Only publish fixed, verified release assets. A failed fetch keeps the static state.
fetch(new URL('assets/release.json', document.baseURI)).then(response => {
  if (!response.ok) throw new Error('Release metadata unavailable');
  return response.json();
}).then(release => {
  if (release.published !== true || !/^v[0-9]+\.[0-9]+\.[0-9]+$/.test(release.tag)) return;
  const targets = ['mac-arm64', 'mac-x64', 'win-x64'];
  const labels = ['Mac Apple Silicon · DMG', 'Mac Intel · DMG', 'Windows x64 · EXE'];
  const names = targets.map(target => `Slide-Studio-${release.tag.slice(1)}-${target}${target === 'win-x64' ? '-Setup.exe' : '.dmg'}`);
  if (!targets.every((target, i) => release.assets?.[target] === names[i])) return;
  targets.forEach((target, i) => {
    const placeholder = document.querySelector(`[data-download="${target}"]`);
    if (!placeholder) return;
    const link = document.createElement('a');
    link.className = placeholder.className;
    link.dataset.download = target;
    link.textContent = labels[i];
    link.href = `https://github.com/edoaki/slide-studio/releases/download/${release.tag}/${names[i]}`;
    placeholder.replaceWith(link);
  });
  document.getElementById('download-status').textContent = `バージョン ${release.tag.slice(1)}。お使いの OS と CPU を選んでください。`;
}).catch(() => {});
