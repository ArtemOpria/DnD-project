const searchInput = document.querySelector('.search-input');
const monsters = document.querySelectorAll('.pointer');

searchInput.addEventListener('input', () => {
  const searchText = searchInput.value.toLowerCase();
  monsters.forEach(monster => {
    const name = monster.querySelector(".besiary-element").textContent.toLowerCase();

    if (name.includes(searchText)) {
      monster.style.display = '';
    } else {
      monster.style.display = 'none';
    }
  });
});
