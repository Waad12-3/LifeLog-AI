// static/script.js
document.addEventListener('DOMContentLoaded', () => {
  const toggle = document.getElementById('darkModeToggle');
  const body = document.body;

  // Check saved mode
  if (localStorage.getItem('darkMode') === 'true') {
    body.classList.add('dark-mode');
  }

  toggle.addEventListener('click', () => {
    body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
  });
});

document.addEventListener('DOMContentLoaded', () => {
  const moodSelcet = documet.querySelector('select[name="mood"]');
  const searchInput = document.querySelector('input[name="q"]');
  const entries = document.querySelector('.entries-container');

  async function fechEntries() {
    const mood = moodSelector.value;
    const q = searchInput.value;
    const res = await fetch(`/history?mood=${mood}&q=${q}`);
    const data = await res.json();

    container.innerHTML = '';
    if (data.length === 0) {
      container.innerHTML = '<p>No entries yet!</p>';
    }
    else {
      data.foreach(entry => {
        container.innerHTML += `
        <div class="entry" data-mood="${entry.mood}">
            <p>${entry.content}</p>
            <small>${entry.mood} - ${entry.date}</small>
            <hr>
        </div>
        `;
      });
    }
  }

  if (searchInput && moodSelector && container) {
    moodSelector.addEventListener('change', fetchEntries);
    searchInput.addEventListener('input', fetchEntries);
  } 
})