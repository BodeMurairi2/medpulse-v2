document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('updateForm');
  const popup = document.getElementById('popupMessage');
  const statusBtn = document.getElementById('statusToggle');

  // Toggle status active/inactive
  statusBtn.addEventListener('click', () => {
    if (statusBtn.textContent === "Active") {
      statusBtn.textContent = "Inactive";
      statusBtn.classList.add('inactive');
    } else {
      statusBtn.textContent = "Active";
      statusBtn.classList.remove('inactive');
    }
  });

  // Handle form submission (PUT request)
  form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const departmentName = document.getElementById('department_name').value.trim();
    if (!departmentName) {
      alert("Please enter a department name before submitting.");
      return;
    }

    const createdAtText = document.getElementById('created_at').textContent.trim();
    const updatedDepartment = {
      department_name: departmentName,
      department_description: document.getElementById('department_description').value.trim(),
      department_email: document.getElementById('email').value.trim(),
      hospital_id: parseInt(document.getElementById('hospital_id').value),
      phone: document.getElementById('phone').value.trim(),
      location: document.getElementById('location').value.trim(),
      number_of_staff: parseInt(document.getElementById('number_of_staff').value),
      status: statusBtn.textContent === "Active",
      created_at: createdAtText || new Date().toISOString(), // keep displayed or fallback
      updated_at: new Date().toISOString(),
    };

    try {
      const response = await fetch(`http://localhost:8080/department/update/${departmentName}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(updatedDepartment),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(errorText || 'Failed to update department');
      }

      popup.textContent = 'Successfully updated the department!';
      popup.classList.remove('hidden');

      setTimeout(() => {
        popup.classList.add('hidden');
        window.location.href = "../HTMLs/view-dep-list.html";
      }, 2000);
    } catch (err) {
      alert(`Error updating department: ${err.message}`);
    }
  });
});
