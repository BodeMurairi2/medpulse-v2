document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('createForm');
  const popup = document.getElementById('popupMessage');

  form.addEventListener('submit', (e) => {
    e.preventDefault();

    const newDepartment = {
      department_name: document.getElementById('department_name').value,
      department_description: document.getElementById('department_description').value,
      email: document.getElementById('email').value,
      location: document.getElementById('location').value,
      phone: document.getElementById('phone').value,
      number_of_staff: parseInt(document.getElementById('number_of_staff').value),
      hospital_id: parseInt(document.getElementById('hospital_id').value),
      department_id: parseInt(document.getElementById('department_id').value),
      status: document.getElementById('status').value === "true",
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString()
    };

    console.log("New department created:", newDepartment);

    popup.classList.remove('hidden');

    setTimeout(() => {
      popup.classList.add('hidden');
      window.location.href = "../HTMLs/view-dep-list.html";
    }, 2000);
  });
});