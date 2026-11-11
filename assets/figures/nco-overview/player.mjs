import {mount} from '../runtime/figure.mjs';
import figure from './figure.mjs';

mount(figure);
const animation = window.animation;
animation.setVisible(true);
const stage = document.getElementById('stage');
const previous = document.getElementById('previous');
const next = document.getElementById('next');
const restart = document.getElementById('restart');
const status = document.getElementById('step-status');

function go(step) {
  animation.setStep(step, true);
  previous.disabled = animation.step === 0;
  next.disabled = animation.step === animation.steps;
  restart.disabled = animation.step === 0;
  status.textContent = `${animation.step + 1} / ${animation.steps + 1}　${animation.stepNames[animation.step]}`;
}
previous.addEventListener('click', () => go(animation.step - 1));
next.addEventListener('click', () => go(animation.step + 1));
restart.addEventListener('click', () => go(0));

// The slide runtime delegates embedded navigation to its host. This standalone
// demo owns navigation so it also works inside a regular website iframe.
let pointer;
stage.addEventListener('pointerdown', event => {
  pointer = event.button === 0 ? {x:event.clientX, y:event.clientY, dragged:false} : null;
});
stage.addEventListener('pointermove', event => {
  if (pointer && Math.hypot(event.clientX - pointer.x, event.clientY - pointer.y) > 5) pointer.dragged = true;
});
stage.addEventListener('pointercancel', () => { pointer = null; });
stage.addEventListener('click', event => {
  event.stopPropagation();
  if (pointer && !pointer.dragged && !getSelection().toString()) go(animation.step + 1);
  pointer = null;
});
document.addEventListener('keydown', event => {
  if (event.target.closest('button') || event.altKey || event.ctrlKey || event.metaKey) return;
  const targets = {ArrowLeft:animation.step - 1, ArrowRight:animation.step + 1, Home:0, End:animation.steps};
  if (!(event.key in targets)) return;
  event.preventDefault();
  event.stopImmediatePropagation();
  if (!event.repeat) go(targets[event.key]);
}, true);
go(0);
