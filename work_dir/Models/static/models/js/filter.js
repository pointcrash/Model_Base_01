  const filterForm = document.querySelector('.filter-form');
  const filterToggleBtn = filterForm.querySelector('.filter-toggle-btn');
  const filterGroups = filterForm.querySelectorAll('.filter-group');

  filterToggleBtn.addEventListener('click', () => {
    filterGroups.forEach(group => {
      group.classList.toggle('hidden'); // переключаем класс "hidden" для каждой группы полей
    });

    if (filterToggleBtn.innerText === 'Свернуть фильтр') {
      filterToggleBtn.innerText = 'Развернуть фильтр';
    } else {
      filterToggleBtn.innerText = 'Свернуть фильтр';
    }
  });