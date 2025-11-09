document.addEventListener("DOMContentLoaded", () => {
  const patients = [
    {
      firstName: "Alice",
      otherNames: "Mugisha",
      gender: "Female",
      patientId: "P001",
      phone: "0788123456",
      email: "alice@example.com",
      country: "Rwanda",
      city: "Kigali",
      district: "Gasabo",
      dob: "1990-05-12",
      nationalId: "1199001234567890",
      bloodGroup: "A+",
      medicalNotes: "Allergic to penicillin.",
      labResults: "Blood test normal. X-ray clear."
    },
    {
      firstName: "Brian",
      otherNames: "Nkurunziza",
      gender: "Male",
      patientId: "P002",
      phone: "0788234567",
      email: "brian@example.com",
      country: "Rwanda",
      city: "Huye",
      district: "Ngoma",
      dob: "2005-03-22",
      nationalId: "",
      bloodGroup: "O-",
      medicalNotes: "History of asthma.",
      labResults: "Lung function test shows mild obstruction."
    }
  ];

  const patientList = document.getElementById("patientList");
  const searchInput = document.getElementById("searchInput");

  function displayPatients(filteredList) {
    patientList.innerHTML = "";

    filteredList.forEach(patient => {
      const row = document.createElement("div");
      row.className = "patient-row";
      row.innerHTML = `
        <span>${patient.firstName} ${patient.otherNames}</span>
        <button class="access-button">Access Records</button>
      `;

      const accessBtn = row.querySelector(".access-button");
      let recordBox = null;

      accessBtn.addEventListener("click", () => {
        if (recordBox) {
          recordBox.remove();
          recordBox = null;
          return;
        }

        recordBox = document.createElement("div");
        recordBox.className = "record-box";
        recordBox.innerHTML = `
          <strong>Full Name:</strong> ${patient.firstName} ${patient.otherNames}<br>
          <strong>Gender:</strong> ${patient.gender}<br>
          <strong>Patient ID:</strong> ${patient.patientId}<br>
          <strong>Phone:</strong> ${patient.phone}<br>
          <strong>Email:</strong> ${patient.email}<br>
          <strong>Country:</strong> ${patient.country}<br>
          <strong>City:</strong> ${patient.city}<br>
          <strong>District:</strong> ${patient.district}<br>
          <strong>Date of Birth:</strong> ${patient.dob}<br>
          ${patient.nationalId ? `<strong>National ID:</strong> ${patient.nationalId}<br>` : ""}
          <strong>Blood Group:</strong> ${patient.bloodGroup}<br>
          <strong>Medical Notes:</strong> ${patient.medicalNotes}<br>
          <strong>Lab Results:</strong> ${patient.labResults}
        `;

        row.after(recordBox);
      });

      patientList.appendChild(row);
    });
  }

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