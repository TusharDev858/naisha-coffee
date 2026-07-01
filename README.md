# Nayesa Coffee — Django Website

A full, modern, mobile-optimized coffee shop website built with Django,
based on Nayesa's original hero page design (`Nayesa_code.zip`). The
superuser can edit **everything** — branding, hero text, about section,
menu, testimonials, gallery, team, and contact info — straight from the
Django admin. No template editing needed to update content.

## Features

- **Fully responsive** — looks great on mobile, tablet, and desktop.
- **Dark mode / light mode** toggle (saved in the visitor's browser).
- **Editable from the admin**:
  - Site Settings (singleton): logo, hero section, about section, stats,
    contact info, social links, footer text.
  - Menu Categories & Menu Items: name, description, price, photo,
    "Popular" badge, available/unavailable toggle.
  - Testimonials: name, role, photo, message, star rating.
  - Gallery: photo grid with captions, click to view full-size (lightbox).
  - Team members: photo, role, bio.
  - Contact messages sent through the website's contact form land in
    the admin so you never miss an inquiry.
- Pages: **Home, About, Menu, Testimonials, Gallery, Contact** — all the
  pages Nayesa already named in her original navbar.
- Built using the original color palette (`#3b141c` deep maroon +
  `#f3961c` warm orange) and the "Poppins" font, now paired with
  "Playfair Display" for an elevated, modern coffee-shop feel.

## Project structure

```
nayesa_coffee/
├── manage.py
├── requirements.txt
├── nayesa_coffee/        # Django project settings
├── coffee/                # Main app: models, admin, views, urls
│   └── management/commands/seed_demo_data.py   # demo content loader
├── templates/              # base.html + all page templates
└── static/
    ├── css/style.css       # full responsive + dark/light theme styles
    ├── js/main.js           # theme toggle, mobile nav, lightbox
    └── img/Nayesa.png        # original hero image, used as fallback
```

## Getting started

1. **Create a virtual environment & install dependencies**
   ```bash
   python -m venv venv
   venv\Scripts\activate        # Windows
   # source venv/bin/activate   # macOS/Linux
   pip install -r requirements.txt
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **(Optional) Load demo content** — fills in sample menu items,
   testimonials, and team members so the site looks complete right away:
   ```bash
   python manage.py seed_demo_data
   ```

4. **Create a superuser account**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` for the website and
   `http://127.0.0.1:8000/admin/` to manage content.

## Editing content as the superuser

Log into `/admin/`:

- **Site Settings** → controls the hero section, about section, stats,
  contact details, social links and footer — opens straight to the
  single editable record.
- **Menu Categories** → add categories like "Hot Coffee", "Cold & Iced",
  "Pastries"; add items inline directly under each category.
- **Menu Items** → set price, photo, mark as "Popular" to feature it on
  the homepage, toggle availability without deleting it.
- **Testimonials** → add customer reviews with a star rating (1–5).
- **Gallery Images** → upload photos for the gallery page (shown on the
  homepage too, first 8 images).
- **Team Members** → showcase your baristas and staff on the About page.
- **Contact Messages** → read messages sent through the website's
  Contact page.

## Notes for production

- Set `DEBUG = False` and configure `ALLOWED_HOSTS` in
  `nayesa_coffee/settings.py` before deploying.
- Replace `SECRET_KEY` with a securely generated value (use an
  environment variable).
- Serve static and media files via a proper web server (or a service
  like WhiteNoise / S3) instead of Django's development server.
- Switch the database from SQLite to PostgreSQL/MySQL for production
  use if you expect meaningful traffic.
