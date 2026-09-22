document.addEventListener("DOMContentLoaded", () => {
    loadPlatformStats();
    setupMobileMenu();
});

async function loadPlatformStats() {
    try {
        const response = await fetch(
            "https://campuspulse-backend-uzum.onrender.com/api/public/summary"
        );

        if (!response.ok) {
            throw new Error("Unable to load platform statistics.");
        }

        const data = await response.json();

        updateElement("totalStudents", data.total_students);
        updateElement("totalCompanies", data.total_companies);
        updateElement("totalJobs", data.total_jobs);
        updateElement("totalApplications", data.total_applications);
        updateElement("totalOffers", data.total_offers);

        updateElement("previewStudents", data.total_students);
        updateElement("previewCompanies", data.total_companies);
        updateElement("previewJobs", data.total_jobs);
        updateElement("previewOffers", data.total_offers);

        updateElement("analyticsStudents", data.total_students);
        updateElement("analyticsCompanies", data.total_companies);
        updateElement("analyticsJobs", data.total_jobs);
        updateElement("analyticsApplications", data.total_applications);
        updateElement("analyticsOffers", data.total_offers);

    } catch (error) {
        console.error("CampusPulse statistics error:", error);

        setFallbackValue("totalStudents");
        setFallbackValue("totalCompanies");
        setFallbackValue("totalJobs");
        setFallbackValue("totalApplications");
        setFallbackValue("totalOffers");

        setFallbackValue("previewStudents");
        setFallbackValue("previewCompanies");
        setFallbackValue("previewJobs");
        setFallbackValue("previewOffers");

        setFallbackValue("analyticsStudents");
        setFallbackValue("analyticsCompanies");
        setFallbackValue("analyticsJobs");
        setFallbackValue("analyticsApplications");
        setFallbackValue("analyticsOffers");
    }
}

function updateElement(id, value) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = Number(value).toLocaleString("en-IN");
    }
}

function setFallbackValue(id) {
    const element = document.getElementById(id);

    if (element) {
        element.textContent = "â€”";
    }
}

function setupMobileMenu() {
    const menuToggle = document.getElementById("menuToggle");
    const navLinks = document.querySelector(".nav-links");

    if (!menuToggle || !navLinks) {
        return;
    }

    menuToggle.addEventListener("click", () => {
        navLinks.classList.toggle("mobile-open");
    });

    navLinks.querySelectorAll("a").forEach((link) => {
        link.addEventListener("click", () => {
            navLinks.classList.remove("mobile-open");
        });
    });
}
