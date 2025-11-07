document.addEventListener('DOMContentLoaded', () => {
  const doctors = [
    {
      firstName: "Amina",
      otherNames: "Nkurunziza",
      gender: "Female",
      doctorID: "DOC001",
      email: "amina.n@medpulse.rw",
      phone: "+250 788 123 456",
      department: "Cardiology",
      hospitalID: "HSP1001",
      createdAt: "2025-10-01 09:30",
      updatedAt: "2025-11-05 14:15",
      status: "Active"
    },
    {
      firstName: "Jean Bosco",
      otherNames: "Mugisha",
      gender: "Male",
      doctorID: "DOC002",
      email: "jb.mugisha@medpulse.rw",
      phone: "+250 788 654 321",
      department: "Pediatrics",
      hospitalID: "HSP1002",
      createdAt: "2025-09-20 11:00",
      updatedAt: "2025-11-06 10:45",
      status: "Active"
    },
    {
      firstName: "Laura",
      otherNames: "Karangwa",
      gender: "Female",
      doctorID: "DOC003",
      email: "laurakar@medpulse.rw",
      phone: "+250 788 654 000",
      department: "Neurology",
      hospitalID: "HSP1003",
      createdAt: "2025-05-28 14:00",
      updatedAt: "2025-06-20 17:55",
      status: "Active"
    }
  ];

  const searchInput = document.getElementById('searchInput');
  const doctorList = document.getElementById('doctorList');

  let activeDoctorID = null;
  let activeDetailBox = null;

  // Sort doctors alphabetically by first name
  doctors.sort((a, b) =>
    a.firstName.toLowerCase().localeCompare(b.firstName.toLowerCase())
  );

  function displayDoctorList(filteredDoctors) {
    doctorList.innerHTML = '';
    activeDoctorID = null;
    activeDetailBox = null;

    filteredDoctors.forEach(doc => {
      const li = document.createElement('li');
      li.textContent = `${doc.firstName} ${doc.otherNames}`;
      li.classList.add('doctor-name');
      li.addEventListener('click', () => toggleDoctorDetails(doc, li));
      doctorList.appendChild(li);
    });
  }

  function toggleDoctorDetails(doc, liElement) {
    // If clicking the same doctor, remove the box
    if (activeDoctorID === doc.doctorID) {
      if (activeDetailBox) {
        activeDetailBox.remove();
        activeDetailBox = null;
        activeDoctorID = null;
      }
      return;
    }

    // Remove previous box if any
    if (activeDetailBox) {
      activeDetailBox.remove();
    }

    // Create new box
    const detailBox = document.createElement('div');
    detailBox.className = 'doctor-details';
    detailBox.innerHTML = `
      <p><strong>First Name:</strong> ${doc.firstName}</p>
      <p><strong>Other Names:</strong> ${doc.otherNames}</p>
      <p><strong>Gender:</strong> ${doc.gender}</p>
      <p><strong>Doctor ID:</strong> ${doc.doctorID}</p>
      <p><strong>Email:</strong> ${doc.email}</p>
      <p><strong>Tel Number:</strong> ${doc.phone}</p>
      <p><strong>Department:</strong> ${doc.department}</p>
      <p><strong>Hospital ID:</strong> ${doc.hospitalID}</p>
      <p><strong>Status:</strong> ${doc.status}</p>
      <p><strong>Created At:</strong> ${doc.createdAt}</p>
      <p><strong>Updated At:</strong> ${doc.updatedAt}</p>
    `;

    liElement.insertAdjacentElement('afterend', detailBox);
    activeDetailBox = detailBox;
    activeDoctorID = doc.doctorID;
  }

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    const filtered = doctors.filter(doc =>
      `${doc.firstName} ${doc.otherNames}`.toLowerCase().includes(query)
    );
    displayDoctorList(filtered);
  });

  displayDoctorList(doctors);
});