const BASE_URL = "http://your-backend-url/api/departments"; // Replace this with actual backend URL

const form = document.getElementById("departmentForm");
const tableBody = document.getElementById("departmentsTableBody");
const searchInput = document.getElementById("searchInput");

async function fetchDepartments() {
  const res = await fetch(BASE_URL);
  const data = await res.json();
  displayDepartments(data);
}

function displayDepartments(departments) {
  tableBody.innerHTML = "";
  departments.forEach(dep => {
    const row = document.createElement("tr");
    row.innerHTML = `
      <td>${dep.department_name}</td>
      <td>${dep.department_description}</td>
      <td>${dep.email}</td>
      <td>${dep.phone}</td>
      <td>${dep.location}</td>
      <td>${dep.number_of_staff}</td>
      <td>${dep.status ? "Active" : "Inactive"}</td>
      <td class="actions">
        <button onclick='editDepartment(${JSON.stringify(dep)})'>Edit</button>
        <button onclick='deleteDepartment("${dep.department_name}")'>Delete</button>
      </td>
    `;
    tableBody.appendChild(row);
  });
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const department = {
    department_name: document.getElementById("department_name").value,
    department_description: document.getElementById("department_description").value,
    department_email: document.getElementById("department_email").value,
    hospital_id: 1,
    phone: document.getElementById("phone").value,
    location: document.getElementById("location").value,
    number_of_staff: parseInt(document.getElementById("number_of_staff").value),
    status: document.getElementById("status").value === "true",
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString(),
  };

  await fetch(BASE_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(department),
  });

  form.reset();
  fetchDepartments();
});

function editDepartment(dep) {
  document.getElementById("department_name").value = dep.department_name;
  document.getElementById("department_description").value = dep.department_description;
  document.getElementById("department_email").value = dep.email;
  document.getElementById("phone").value = dep.phone;
  document.getElementById("location").value = dep.location;
  document.getElementById("number_of_staff").value = dep.number_of_staff;
  document.getElementById("status").value = dep.status ? "true" : "false";
}

async function deleteDepartment(department_name) {
  if (confirm(`Are you sure you want to delete ${department_name}?`)) {
    await fetch(`${BASE_URL}/${department_name}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ department_name }),
    });
    fetchDepartments();
  }
}

searchInput.addEventListener("input", async () => {
  const name = searchInput.value.trim();
  if (name === "") {
    fetchDepartments();
  } else {
    const res = await fetch(`${BASE_URL}/search?name=${name}`);
    const data = await res.json();
    displayDepartments(data);
  }
});

fetchDepartments();
