// Function to fetch doctors list
var doctors_list = function fetchData(url = "http://127.0.0.1:8080/doctorsList/list") {
  return fetch(url)
    .then(response => {
      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.status}`);
      }
      return response;
    })
    .then(response => response.json())
    .then(data => data)
    .catch(error => {
      console.error('There has been a problem with your fetch operation:', error);
    });
}

// Populate all departments and doctors
document.addEventListener('DOMContentLoaded', () => {
  const directory = document.querySelector('.doctor-directory');

  // Clear existing content except the main title
  directory.innerHTML = '<h2>All Doctors per Department</h2>';

  // Fetch doctors
  doctors_list().then(data => {
    if (!data) return;

    Object.keys(data).forEach(department => {
      const doctors = data[department];
      if (!doctors || doctors.length === 0) return;

      // Create department section
      const section = document.createElement('section');
      section.className = 'department-section';
      section.dataset.department = department;

      // Department title
      const h3 = document.createElement('h3');
      h3.textContent = department;
      section.appendChild(h3);

      // Create table
      const table = document.createElement('table');
      table.className = 'doctor-table';

      // Table head
      table.innerHTML = `
        <thead>
          <tr>
            <th>Name</th>
            <th>Gender</th>
            <th>Phone</th>
            <th>Email</th>
          </tr>
        </thead>
        <tbody></tbody>
      `;

      const tbody = table.querySelector('tbody');

      // Add doctor rows
      doctors.forEach(doc => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>Dr. ${doc.first_name} ${doc.last_name}</td>
          <td>${doc.gender}</td>
          <td>${doc.phone_number}</td>
          <td>${doc.email}</td>
        `;
        tbody.appendChild(tr);
      });

      // Optional: sort rows by name
      const rows = Array.from(tbody.querySelectorAll('tr'));
      rows.sort((a, b) => {
        const nameA = a.cells[0].textContent.replace(/^Dr\.\s*/i, '').toLowerCase();
        const nameB = b.cells[0].textContent.replace(/^Dr\.\s*/i, '').toLowerCase();
        return nameA.localeCompare(nameB);
      });
      tbody.innerHTML = '';
      rows.forEach(row => tbody.appendChild(row));

      section.appendChild(table);
      directory.appendChild(section);
    });
  });
});
