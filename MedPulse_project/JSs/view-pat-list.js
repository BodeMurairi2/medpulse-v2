document.addEventListener("DOMContentLoaded", () => {
  const patients = [
    {
      firstName: "Alice",
      otherNames: "Mugisha",
      gender: "Female",
      patientId: "P001",
      phone: "0788123456",
      email: "alice@example.com"
    },
    {
      firstName: "Brian",
      otherNames: "Nkurunziza",
      gender: "Male",
      patientId: "P002",
      phone: "0788234567",
      email: "brian@example.com"
    },
    {
      firstName: "Clara",
      otherNames: "Uwase",
      gender: "Female",
      patientId: "P003",
      phone: "0788345678",
      email: "clara@example.com"
    }
  ];

  const tableBody = document.querySelector("#patientTable tbody");
  const searchInput = document.getElementById("searchInput");

  function displayPatients(filteredList) {
    tableBody.innerHTML = "";

    filteredList.forEach(patient => {
      const row = document.createElement("tr");
      row.innerHTML = `
        <td>${patient.firstName} ${patient.otherNames}</td>
        <td>${patient.gender}</td>
        <td>${patient.patientId}</td>
        <td>${patient.phone}</td>
        <td>${patient.email}</td>
      `;
      tableBody.appendChild(row);
    });
  }

  // Sort alphabetically by first name
  patients.sort((a, b) => a.firstName.localeCompare(b.firstName));
  displayPatients(patients);

  searchInput.addEventListener("input", () => {
    const query = searchInput.value.toLowerCase();
    const filtered = patients.filter(p =>
      `${p.firstName} ${p.otherNames}`.toLowerCase().includes(query)
    );
    displayPatients(filtered);
  });
});