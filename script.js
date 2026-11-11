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
const command = "git clone https://github.com/edoaki/slide-studio.git\ncd slide-studio\nuv run slide-studio";
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
