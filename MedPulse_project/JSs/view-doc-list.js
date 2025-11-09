document.addEventListener('DOMContentLoaded', () => {
  const tables = document.querySelectorAll('.doctor-table');

  tables.forEach(table => {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));

    rows.sort((a, b) => {
      const nameA = a.cells[0].textContent.replace(/^Dr\.\s*/i, '').toLowerCase();
      const nameB = b.cells[0].textContent.replace(/^Dr\.\s*/i, '').toLowerCase();
      return nameA.localeCompare(nameB);
    });

    // Clear and re-append sorted rows
    tbody.innerHTML = '';
    rows.forEach(row => tbody.appendChild(row));
  });
});