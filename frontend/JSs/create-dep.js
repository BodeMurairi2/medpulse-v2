document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('createForm');
  const popup = document.getElementById('popupMessage');
  const apiEndpoint = "http://localhost:8080/department/add";

  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const department_name = document.getElementById('department_name').value.trim();
    const department_description = document.getElementById('department_description').value.trim();
    const email = document.getElementById('email').value.trim();
    const location = document.getElementById('location').value.trim();
    const phone = document.getElementById('phone').value.trim();
    const number_of_staff = parseInt(document.getElementById('number_of_staff').value);
    const hospital_id = parseInt(document.getElementById('hospital_id').value);
    const status = document.getElementById('status').value === "true";

    // Validation
    if (!department_name || department_name.length < 3 || !department_description || department_description.length < 10 || !email || !phone || !location || isNaN(number_of_staff) || number_of_staff < 2 || isNaN(hospital_id)) {
      alert("Please fill in all fields correctly according to validation rules.");
      return;
    }

    const newDepartment = {
      department_name,
      department_description,
      department_email: email,
      hospital_id,
      phone,
      location,
      number_of_staff,
      status
    };

    try {
      const response = await fetch(apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(newDepartment)
      });

      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

      const data = await response.json();
      console.log('Success:', data);

      popup.textContent = `Department "${department_name}" created successfully!`;
      popup.classList.remove('hidden');

      setTimeout(() => {
        popup.classList.add('hidden');
        window.location.href = "../HTMLs/view-dep-list.html";
      }, 2000);

    } catch (error) {
      console.error('Error:', error);
      popup.textContent = `Error creating department: ${error.message}`;
      popup.classList.remove('hidden');
      setTimeout(() => popup.classList.add('hidden'), 3000);
    }
  });
});
