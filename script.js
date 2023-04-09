const posterLogo = document.getElementById("posterLogo");
const characterTextNButton = document.getElementById("characterTextNButton");
const bestiaryTextNButton = document.getElementById("bestiaryTextNButton");
const diceTextNButton = document.getElementById("diceTextNButton");
// const characterButton = document.getElementById("characterButton");
// const characterText = document.getElementById("characterText");

const options = {
  root: null,
  threshold: 0.1,
  rootMargin: '0px'
}

// const observer = new IntersectionObserver(entries => {
//   // перевірка чи елемент потрапив у зону видимості
//   if (entries[0].isIntersecting) {
//     // додавання класу, який показує елемент
//     posterLogo.classList.add("show-down");
//     characterTextNButton.classList.add("show-left");
//   }
// });


const observerDown = new IntersectionObserver(function(entries, observer) {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('show-down');
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

// observerLeft.observe(characterButton);
// observerLeft.observe(characterText);
