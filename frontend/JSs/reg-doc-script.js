document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");

  // Create popup element
  const popup = document.createElement("div");
  popup.id = "popupMessage";
  popup.className = "popup hidden";
  popup.textContent = "Successfully registered a new doctor!";
  document.body.appendChild(popup);

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    // Collect form data
    const doctorData = {
      firstName: form.firstName.value.trim(),
      otherNames: form.otherNames.value.trim(),
      gender: form.gender.value,
      license: form.license.value.trim(),
      email: form.email.value.trim(),
      nationalId: form.nationalId.value.trim(),
      dob: form.dob.value,
      department: form.department.value,
      status: form.status.value
    };

    // Generate temporary password
    const tempPassword = `Doc${Math.floor(1000 + Math.random() * 9000)}`;

    // Simulate sending email
    console.log(`📧 Email sent to ${doctorData.email}:
Subject: Welcome to MedPulse
Body:
Dear Dr. ${doctorData.firstName},

Your account has been successfully created.
Email: ${doctorData.email}
Temporary Password: ${tempPassword}

Please log in and change your password immediately.`);

    // Show popup
    popup.classList.remove("hidden");

    // Redirect after 2 seconds
    setTimeout(() => {
      popup.classList.add("hidden");
      window.location.href = "../HTMLs/view-doc-list.html";
    }, 2000);

    // Reset form
    form.reset();
  });
});