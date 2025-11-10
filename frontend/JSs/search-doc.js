document.addEventListener('DOMContentLoaded', () => {
  const searchInput = document.getElementById('searchInput');
  const searchButton = document.getElementById('searchButton');
  const doctorList = document.getElementById('doctorList');

  let activeDoctorID = null;
  let activeDetailBox = null;

  // Function to display the list of doctors
  function displayDoctorList(doctors) {
    doctorList.innerHTML = '';
    activeDoctorID = null;
    activeDetailBox = null;

    if (doctors.length === 0) {
      doctorList.innerHTML = '<li>No doctors found.</li>';
      return;
    }

    doctors.forEach(doc => {
      const li = document.createElement('li');
      li.textContent = `${doc.firstName} ${doc.otherNames}`;
      li.classList.add('doctor-name');
      li.addEventListener('click', () => toggleDoctorDetails(doc, li));
      doctorList.appendChild(li);
    });
  }

  // Function to show/hide doctor details
  function toggleDoctorDetails(doc, liElement) {
    if (activeDoctorID === doc.doctorID) {
      if (activeDetailBox) {
        activeDetailBox.remove();
        activeDetailBox = null;
        activeDoctorID = null;
      }
      return;
    }

    if (activeDetailBox) activeDetailBox.remove();

    const detailBox = document.createElement('div');
    detailBox.className = 'doctor-details';
    detailBox.innerHTML = `
      <p><strong>First Name:</strong> ${doc.firstName}</p>
      <p><strong>Other Names:</strong> ${doc.otherNames}</p>
      <p><strong>Gender:</strong> ${doc.gender}</p>
      <p><strong>Email:</strong> ${doc.email}</p>
      <p><strong>Tel Number:</strong> ${doc.phone}</p>
      <p><strong>Department:</strong> ${doc.department}</p>
      <p><strong>Hospital ID:</strong> ${doc.hospitalID}</p>
      <p><strong>Status:</strong> ${doc.status}</p>
    `;

    liElement.insertAdjacentElement('afterend', detailBox);
    activeDetailBox = detailBox;
    activeDoctorID = doc.doctorID;
  }

  // Function to perform search using API path parameter
  function performSearch() {
    const query = encodeURIComponent(searchInput.value.trim());
    if (!query) return;

    fetch(`http://127.0.0.1:8080/doctorsList/list/${query}`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Network response was not ok: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        // Map API response to consistent format
        const doctors = data.map(doc => ({
          firstName: doc.first_name,
          otherNames: doc.last_name,
          gender: doc.gender,
          email: doc.email,
          phone: doc.phone_number,
          department: doc.department,
          hospitalID: doc.hospital_id,
          status: 'Active'
        }));

        // Sort alphabetically by first name
        doctors.sort((a, b) =>
          a.firstName.toLowerCase().localeCompare(b.firstName.toLowerCase())
        );

        displayDoctorList(doctors);
      })
      .catch(err => {
        console.error('Error fetching doctors:', err);
        doctorList.innerHTML = '<li>No doctors found.</li>';
      });
  }

  // Only search when the button is clicked
  searchButton.addEventListener('click', performSearch);

  // Optional: search when user presses Enter in the input field
  searchInput.addEventListener('keypress', event => {
    if (event.key === 'Enter') performSearch();
  });
});
