document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const departmentList = document.getElementById('departmentList');

  let departments = [];
  let activeDepartmentName = null;

  // Fetch departments from the API
  function fetchDepartments() {
    fetch('http://127.0.0.1:8080/department/all')
      .then(response => response.json())
      .then(data => {
        // Map API response to consistent format
        departments = data.map(dept => ({
          name: dept.department_name,
          description: dept.department_description,
          email: dept.email,
          location: dept.location,
          number_of_staff: dept.number_of_staff,
          updated_at: dept.updated_at,
          hospital_id: dept.hospital_id,
          department_id: dept.department_id,
          phone: dept.phone,
          status: dept.status,
          created_at: dept.created_at
        }));

        // Sort alphabetically
        departments.sort((a, b) => a.name.localeCompare(b.name));

        displayDepartments(departments); // Display all initially
      })
      .catch(err => console.error('Error fetching departments:', err));
  }

  // Render departments
  function displayDepartments(filtered) {
    departmentList.innerHTML = '';

    filtered.forEach(dept => {
      const card = document.createElement('div');
      card.className = 'department-card';
      card.innerHTML = `
        <h3>${dept.name}</h3>
        <p>${dept.description}</p>
        <button class="details-button">${activeDepartmentName === dept.name ? 'Hide details' : 'View more details'}</button>
      `;

      const detailsBtn = card.querySelector('.details-button');
      detailsBtn.addEventListener('click', () => toggleDepartmentDetails(dept, card));

      departmentList.appendChild(card);

      // Show details if this card is active
      if (activeDepartmentName === dept.name) {
        const details = document.createElement('div');
        details.className = 'department-details';
        details.innerHTML = `
          <p><strong>Email:</strong> ${dept.email}</p>
          <p><strong>Phone:</strong> ${dept.phone}</p>
          <p><strong>Location:</strong> ${dept.location}</p>
          <p><strong>Number of Staff:</strong> ${dept.number_of_staff}</p>
          <p><strong>Status:</strong> ${dept.status ? "Active" : "Inactive"}</p>
        `;
        card.appendChild(details);
      }
    });
  }

  function toggleDepartmentDetails(dept, cardElement) {
    if (activeDepartmentName === dept.name) {
      activeDepartmentName = null; // hide
    } else {
      activeDepartmentName = dept.name; // show
    }
    displayDepartments(departments.filter(d => d.name.toLowerCase().includes(searchInput.value.toLowerCase())));
  }

  // Search filter
  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    activeDepartmentName = null; // reset active on new search
    const filtered = departments.filter(dept =>
      dept.name.toLowerCase().includes(query)
    );
    displayDepartments(filtered);
  });

  // Fetch departments on page load
  fetchDepartments();
});
