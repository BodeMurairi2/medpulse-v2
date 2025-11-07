document.addEventListener('DOMContentLoaded', () => {
  const departments = [
    {
      name: "Cardiology",
      description: "Heart and vascular care",
      email: "cardio@example.com",
      location: "Floor 2001 KG 11",
      number_of_staff: 55,
      updated_at: "2025-11-01T10:14:54.921935+02:00",
      hospital_id: 1,
      department_id: 1,
      phone: "243856707011",
      status: true,
      created_at: "2025-01-15T08:00:00"
    },
    {
      name: "Neurology",
      description: "Brain and nervous system",
      email: "neuro@example.com",
      location: "Floor 2002 KG 12",
      number_of_staff: 40,
      updated_at: "2025-10-20T09:30:00",
      hospital_id: 1,
      department_id: 2,
      phone: "243856707022",
      status: true,
      created_at: "2025-02-10T09:00:00"
    }
    // Add more departments here
  ];

  const searchInput = document.getElementById('searchInput');
  const departmentList = document.getElementById('departmentList');

  let activeDepartmentName = null;

  function displayDepartments(filtered) {
    departmentList.innerHTML = '';

    filtered.forEach(dept => {
      const card = document.createElement('div');
      card.className = 'department-card';
      card.innerHTML = `
        <h3>${dept.name}</h3>
        <p>${dept.description}</p>
        <button class="details-button">View more details</button>
      `;

      const detailsBtn = card.querySelector('.details-button');
      detailsBtn.addEventListener('click', () => {
        if (activeDepartmentName === dept.name) {
          activeDepartmentName = null;
        } else {
          activeDepartmentName = dept.name;
        }
        displayDepartments(filtered); // Re-render with updated state
      });

      departmentList.appendChild(card);

      if (activeDepartmentName === dept.name) {
        const details = document.createElement('div');
        details.className = 'department-details';
        details.innerHTML = `
          <p><strong>Email:</strong> ${dept.email}</p>
          <p><strong>Phone:</strong> ${dept.phone}</p>
          <p><strong>Location:</strong> ${dept.location}</p>
          <p><strong>Number of Staff:</strong> ${dept.number_of_staff}</p>
          <p><strong>Status:</strong> ${dept.status ? "Active" : "Inactive"}</p>
          <p><strong>Hospital ID:</strong> ${dept.hospital_id}</p>
          <p><strong>Department ID:</strong> ${dept.department_id}</p>
          <p><strong>Created At:</strong> ${dept.created_at}</p>
          <p><strong>Updated At:</strong> ${dept.updated_at}</p>
        `;
        card.appendChild(details);
      }
    });
  }

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    const filtered = departments.filter(dept =>
      dept.name.toLowerCase().includes(query)
    );
    activeDepartmentName = null;
    displayDepartments(filtered);
  });

  departments.sort((a, b) => a.name.localeCompare(b.name));
  displayDepartments(departments);
});