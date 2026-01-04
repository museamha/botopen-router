const sidebarToggleBtns = document.querySelectorAll(".sidebar-toggle");
const sidebar = document.querySelector(".sidebar");
const searchForm = document.querySelector(".newchat");
const themeToggleBtn = document.querySelector(".theme-toggle");
const themeIcon = themeToggleBtn.querySelector(".theme-icon");
const menuLinks = document.querySelectorAll(".menu-link");

// Updates the theme icon based on current theme and sidebar state
const updateThemeIcon = () => {
  const isDark = document.body.classList.contains("dark-theme");
  themeIcon.textContent = sidebar.classList.contains("collapsed") ? (isDark ? "light_mode" : "dark_mode") : "dark_mode";
};

// Apply dark theme if saved or system prefers, then update icon
const savedTheme = localStorage.getItem("theme");
const systemPrefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
const shouldUseDarkTheme = savedTheme === "dark" || (!savedTheme && systemPrefersDark);

document.body.classList.toggle("dark-theme", shouldUseDarkTheme);

// --- SIDEBAR TOGGLE ---
sidebarToggleBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    sidebar.classList.toggle("collapsed");

    // Rotate the toggle icon
    btn.classList.toggle("rotated");

    // Update theme icon if necessary
    updateThemeIcon();
  });
});

// --- EXPAND SIDEBAR WHEN SEARCH FORM CLICKED ---
searchForm.addEventListener("click", () => {
  if (sidebar.classList.contains("collapsed")) {
    sidebar.classList.remove("collapsed");
    sidebarToggleBtns.forEach(btn => btn.classList.remove("rotated"));
    searchForm.querySelector("img").focus();
  }
});

// Expand sidebar by default on large screens
if (window.innerWidth > 768) {
  sidebar.classList.remove("collapsed");
  sidebarToggleBtns.forEach(btn => btn.classList.remove("rotated"));
}
