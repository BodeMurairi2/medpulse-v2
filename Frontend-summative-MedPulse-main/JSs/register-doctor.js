let doctorsList = [];

//form submission
document.getElementById('doctorForm').addEventListener('submit', (e) => {
  e.preventDefault();


  const doctorData = {
    name: document.getElementById('doctorName').value.trim(),
    gender: document.getElementById('gender').value,
    license: document.getElementById('license').value.trim(),
    email: document.getElementById('doctorEmail').value.trim(),
    dob: document.getElementById('dob').value,
    nationalId: document.getElementById('nationalId').value.trim(),
    phone: document.getElementById('phone').value.trim(),
    department: document.getElementById('department').value,
    status: document.getElementById('status').value,
    password: document.getElementById('password').value,
    confirmPassword: document.getElementById('confirmPassword').value,
  };


  if (doctorData.password !== doctorData.confirmPassword) {
    alert('Passwords do not match!');
    return;
  }

  // Create doctor ID
  const doctorId = 'MP-' + Math.floor(Math.random() * 1000000);
  doctorData.doctorId = doctorId;

 
  delete doctorData.confirmPassword;

  doctorsList.push(doctorData);

 
  localStorage.setItem('doctorsList', JSON.stringify(doctorsList));

 
  document.getElementById('generatedDoctorId').textContent = doctorId;
  document.getElementById('success-message').style.display = 'block';
  document.getElementById('doctorForm').reset();

  console.log('Doctor added:', doctorData);
  console.log('All registered doctors:', doctorsList);
});
