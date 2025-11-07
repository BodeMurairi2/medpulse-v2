document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('updateForm');
  const popup = document.getElementById('popupMessage');
  const statusBtn = document.getElementById('statusToggle');

  // Simulated department data (replace with real fetch if needed)
  const department = {
    department_id: 2,
    created_at: "2025-02-10T09:00:00",
    department_name: "Neurology",
    department_description: "Brain and nervous system",
    email: "neuro@example.com",
    location: "Floor 2002 KG 12",
    phone: "243856707022",
    number_of_staff: 40,
    hospital_id: 1,
    status: true
  };

  // Populate current info
  document.getElementById('department_id').textContent = department.department_id;
  document.getElementById('created_at').textContent = department.created_at;
  document.getElementById('department_name').value = department.department_name;
  document.getElementById('department_description').value = department.department_description;
  document.getElementById('email').value = department.email;
  document.getElementById('location').value = department.location;
  document.getElementById('phone').value = department.phone;
  document.getElementById('number_of_staff').value = department.number_of_staff;
  document.getElementById('hospital_id').value = department.hospital_id;
  statusBtn.textContent = department.status ? "Active" : "Inactive";
  if (!department.status) statusBtn.classList.add('inactive');

  // Toggle status
  statusBtn.addEventListener('click', () => {
    if (statusBtn.textContent === "Active") {
      statusBtn.textContent = "Inactive";
      statusBtn.classList.add('inactive');
    } else {
      statusBtn.textContent = "Active";
      statusBtn.classList.remove('inactive');
    }
  });

  // Handle form submission
  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const updatedDepartment = {
      department_id: department.department_id,
      created_at: department.created_at,
      department_name: document.getElementById('department_name').value,
      department_description: document.getElementById('department_description').value,
      email: document.getElementById('email').value,
      location: document.getElementById('location').value,
      phone: document.getElementById('phone').value,
      number_of_staff: parseInt(document.getElementById('number_of_staff').value),
      hospital_id: parseInt(document.getElementById('hospital_id').value),
      status: statusBtn.textContent === "Active",
      updated_at: new Date().toISOString()
    };

    console.log("Updated department:", updatedDepartment);

    popup.classList.remove('hidden');

    setTimeout(() => {
      popup.classList.add('hidden');
      window.location.href = "../HTMLs/view-dep-list.html";
    }, 2000);
  });
});