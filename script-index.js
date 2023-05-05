const posterLogo = document.getElementById("posterLogo");
const posterBot = document.getElementById("posterBot");
const characterTextNButton = document.getElementById("characterTextNButton");
const bestiaryTextNButton = document.getElementById("bestiaryTextNButton");
const diceTextNButton = document.getElementById("diceTextNButton");
const mergeDiv = document.getElementById("mergeDiv");
// const characterButton = document.getElementById("characterButton");
// const characterText = document.getElementById("characterText");

const options = {
  root: null,
  threshold: 0.1,
  rootMargin: '0px'
}


const observerDown = new IntersectionObserver(function(entries, observer) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show-down');
      observer.unobserve(entry.target);
    }
  });
}, options);

const observerDownDelay = new IntersectionObserver(function(entries, observer) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show-down-delay');
      observer.unobserve(entry.target);
    }
  });
}, options);

const observerLeft = new IntersectionObserver(function(entries, observer) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show-left');
      observer.unobserve(entry.target);
    }
  });
}, options);

const observerRight = new IntersectionObserver(function(entries, observer) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show-right');
      observer.unobserve(entry.target);
    }
  });
}, options);

observerDown.observe(posterLogo);
observerLeft.observe(characterTextNButton);
observerRight.observe(bestiaryTextNButton);
observerLeft.observe(diceTextNButton);
observerDown.observe(mergeDiv);

// observerLeft.observe(characterButton);
// observerLeft.observe(characterText);
