// ===== THEME TOGGLE =====
(function () {
  const root = document.documentElement;
  const btn = document.getElementById("themeToggle");
  const saved = localStorage.getItem("naisha-theme");
  const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
  root.setAttribute("data-theme", saved || (prefersDark ? "dark" : "light"));
  if (btn) {
    btn.addEventListener("click", function () {
      const next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
      root.setAttribute("data-theme", next);
      localStorage.setItem("naisha-theme", next);
    });
  }
})();

// ===== MOBILE NAV =====
(function () {
  const ham = document.getElementById("hamburger");
  const menu = document.getElementById("navMenu");
  if (!ham || !menu) return;
  ham.addEventListener("click", function () {
    menu.classList.toggle("active");
    ham.classList.toggle("active");
  });
  menu.querySelectorAll(".nav-link").forEach(function (l) {
    l.addEventListener("click", function () {
      menu.classList.remove("active");
      ham.classList.remove("active");
    });
  });
})();

// ===== HEADER SHADOW ON SCROLL =====
(function () {
  const h = document.getElementById("siteHeader");
  if (!h) return;
  window.addEventListener("scroll", function () {
    h.style.boxShadow = window.scrollY > 10 ? "0 4px 24px rgba(0,0,0,.3)" : "";
  });
})();

// ===== TICKER — duplicate for seamless infinite loop =====
(function () {
  const track = document.getElementById("tickerTrack");
  if (!track || !track.children.length) return;
  track.innerHTML = track.innerHTML + track.innerHTML;
  // Adjust speed based on item count (more items = slower so it feels consistent)
  const count = track.children.length;
  const duration = Math.max(25, count * 3);
  track.style.animationDuration = duration + "s";
})();

// ===== GALLERY LIGHTBOX =====
function openLightbox(src, caption) {
  const lb = document.getElementById("lightbox");
  const img = document.getElementById("lightboxImg");
  const cap = document.getElementById("lightboxCaption");
  if (!lb || !img) return;
  img.src = src;
  if (cap) cap.textContent = caption || "";
  lb.classList.add("active");
  document.body.style.overflow = "hidden";
}

function closeLightbox() {
  const lb = document.getElementById("lightbox");
  if (lb) lb.classList.remove("active");
  document.body.style.overflow = "";
}

// Close lightbox on Escape key
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") closeLightbox();
});

// ===== VIDEO — fallback if autoplay blocked =====
(function () {
  const vid = document.querySelector(".bg-video");
  if (!vid) return;
  vid.play().catch(function () {
    vid.setAttribute("controls", "");
  });
})();

// ===== AUTO-DISMISS ALERTS =====
(function () {
  document.querySelectorAll(".alert").forEach(function (a) {
    setTimeout(function () {
      a.style.transition = "opacity .5s";
      a.style.opacity = "0";
      setTimeout(function () { a.remove(); }, 500);
    }, 5000);
  });
})();

// ===== SMOOTH ANCHOR SCROLL =====
document.querySelectorAll('a[href^="#"]').forEach(function (a) {
  a.addEventListener("click", function (e) {
    var href = this.getAttribute("href");
    // Skip bare "#" or empty — querySelector("#") throws and would halt scripts
    if (!href || href === "#") return;
    var target;
    try {
      target = document.querySelector(href);
    } catch (err) {
      return;
    }
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });
});
