document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("patientForm");

  // Create popup element
  const popup = document.createElement("div");
  popup.id = "popupMessage";
  popup.className = "popup hidden";
  popup.textContent = "Successfully registered a new patient!";
  document.body.appendChild(popup);

  form.addEventListener("submit", function (e) {
    e.preventDefault();

    const firstName = document.getElementById("firstName").value.trim();
    const otherNames = document.getElementById("otherNames").value.trim();
    const email = document.getElementById("email").value.trim();
    const dob = document.getElementById("dob").value;

    if (!firstName || !otherNames || !email || !dob) {
      alert("Please fill in all required fields.");
      return;
    }

    // Generate temporary password
    const tempPassword = `Pat${Math.floor(1000 + Math.random() * 9000)}`;

    // Simulate sending email
    console.log(`📧 Email sent to ${email}:
Subject: Welcome to MedPulse
Body:
Dear ${firstName},

Your patient account has been successfully created.
Email: ${email}
Temporary Password: ${tempPassword}

Please log in and change your password immediately.`);

    // Show popup
    popup.classList.remove("hidden");

    // Redirect after 2 seconds
    setTimeout(() => {
      popup.classList.add("hidden");
      window.location.href = "../HTMLs/view-pat-list.html";
    }, 2000);

    // Reset form
    form.reset();
  });
});