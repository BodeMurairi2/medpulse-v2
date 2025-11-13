document.addEventListener("DOMContentLoaded", () => {
  // Fade-in animations
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

  // FAQ Toggle functionality
  const faqItems = document.querySelectorAll(".faq-item");
  faqItems.forEach(item => {
    const question = item.querySelector(".faq-question");
    question.addEventListener("click", () => {
      const isActive = item.classList.contains("active");
      // Close all FAQ items
      faqItems.forEach(faq => faq.classList.remove("active"));
      // Open clicked item if it wasn't active
      if (!isActive) {
        item.classList.add("active");
      }
    });
  });

  // Smooth scroll for Get Started button
  const getStartedBtn = document.querySelector(".get-started");
  if (getStartedBtn) {
    getStartedBtn.addEventListener("click", (e) => {
      e.preventDefault();
      const portalsSection = document.querySelector("#portals");
      if (portalsSection) {
        portalsSection.scrollIntoView({ behavior: "smooth" });
      }
    });
  }
});
