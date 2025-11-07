
document.addEventListener("DOMContentLoaded", () => {
  const fadeElements = document.querySelectorAll(".fade-in");

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
      }
    });
  }, {
    threshold: 0.3
  });

  fadeElements.forEach(el => observer.observe(el));


  // New Login & Signup Form Logic
  const signupForm = document.getElementById("signupForm");
  const loginForm = document.getElementById("loginForm");

  // SIGNUP
  if (signupForm) {
    signupForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        hospital_name: document.getElementById("hospitalName").value,
        hospital_email: document.getElementById("email").value,
        hospital_admin: document.getElementById("adminName").value,
        hospital_phone: document.getElementById("phone").value,
        hospital_location: document.getElementById("location").value,
        password: document.getElementById("password").value,
      };

      const confirmPassword = document.getElementById("confirmPassword").value;
      if (data.password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
      }

      try {
        const res = await fetch("http://127.0.0.1:8000/hospital/signup", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        const result = await res.json();

        if (res.ok) {
          alert("Signup successful! You can now log in.");
          window.location.href = "login.html";
        } else {
          alert(result.detail || "Signup failed. Please try again.");
        }
      } catch (err) {
        console.error(err);
        alert("Error connecting to server.");
      }
    });
  }

  // LOGIN HANDLER
  if (loginForm) {
    loginForm.addEventListener("submit", async (e) => {
      e.preventDefault();

      const data = {
        hospital_email: document.getElementById("email").value,
        password: document.getElementById("password").value,
      };

      try {
        const res = await fetch("http://127.0.0.1:8000/hospital/login", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });

        const result = await res.json();

        if (res.ok) {
          localStorage.setItem("token", result.access_token);
          alert("Login successful!");
          window.location.href = "dashboard.html"; // redirect after login
        } else {
          alert(result.detail || "Login failed. Check your credentials.");
        }
      } catch (err) {
        console.error(err);
        alert("Error connecting to server.");
      }
    });
  }
});
