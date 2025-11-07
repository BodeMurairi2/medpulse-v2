document.addEventListener('DOMContentLoaded', () => {
  const doctors = [
    {
      doctorID: "DOC001",
      firstName: "Amina",
      otherNames: "Nkurunziza",
      email: "amina.n@medpulse.rw",
      phone: "+250 788 123 456",
      department: "Cardiology",
      status: "Active"
    },
    {
      doctorID: "DOC002",
      firstName: "Jean Bosco",
      otherNames: "Mugisha",
      email: "jb.mugisha@medpulse.rw",
      phone: "+250 788 654 321",
      department: "Pediatrics",
      status: "Active"
    },
    {
      doctorID: "DOC003",
      firstName: "Laura",
      otherNames: "Karangwa",
      email: "laurakar@medpulse.rw",
      phone: "+250 788 654 000",
      department: "Neurology",
      status: "Inactive"
    }
  ];

  const searchInput = document.getElementById('searchInput');
  const doctorList = document.getElementById('doctorList');
  const successMessage = document.getElementById('successMessage');

  let activeForm = null;

  function displayDoctorList(filteredDoctors) {
    doctorList.innerHTML = '';
    filteredDoctors.forEach(doc => {
      const li = document.createElement('li');
      li.innerHTML = `
        <span>${doc.firstName} ${doc.otherNames}</span>
        <button class="update-button">Update</button>
      `;

      const updateBtn = li.querySelector('.update-button');
      updateBtn.addEventListener('click', () => showUpdateForm(doc, li));

      doctorList.appendChild(li);
    });
  }

  function showUpdateForm(doc, liElement) {
    if (activeForm) {
      activeForm.remove();
      activeForm = null;
    }

    const form = document.createElement('div');
    form.className = 'update-form';
    form.innerHTML = `
      <p><strong>Doctor ID:</strong> ${doc.doctorID}</p>
      <p><strong>Name:</strong> ${doc.firstName} ${doc.otherNames}</p>
      <input type="email" value="${doc.email}" placeholder="New Email" />
      <input type="text" value="${doc.phone}" placeholder="New Phone" />
      <input type="text" value="${doc.department}" placeholder="New Department" />
      <button type="button" class="status-toggle ${doc.status === 'Inactive' ? 'inactive' : ''}">${doc.status}</button>
      <div class="button-row">
        <button class="save-button">Save Changes</button>
        <button class="cancel-button">Cancel</button>
      </div>
    `;

    const statusBtn = form.querySelector('.status-toggle');
    statusBtn.addEventListener('click', () => {
      if (statusBtn.textContent === "Active") {
        statusBtn.textContent = "Inactive";
        statusBtn.classList.add('inactive');
      } else {
        statusBtn.textContent = "Active";
        statusBtn.classList.remove('inactive');
      }
    });

    const saveBtn = form.querySelector('.save-button');
    saveBtn.addEventListener('click', () => {
      doc.email = form.querySelector('input[type="email"]').value;
      doc.phone = form.querySelector('input[type="text"]').value;
      doc.department = form.querySelectorAll('input')[2].value;
      doc.status = statusBtn.textContent;

      form.remove();
      activeForm = null;
      showSuccessMessage();
      displayDoctorList(doctors);
    });

    const cancelBtn = form.querySelector('.cancel-button');
    cancelBtn.addEventListener('click', () => {
      form.remove();
      activeForm = null;
    });

    liElement.insertAdjacentElement('afterend', form);
    activeForm = form;
  }

  function showSuccessMessage() {
    successMessage.classList.remove('hidden');
    setTimeout(() => {
      successMessage.classList.add('hidden');
    }, 5000);
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