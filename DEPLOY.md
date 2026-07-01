# 🚀 Deploy Naisha Coffee to GitHub + Render

---

## STEP 1 — Install Git (if not installed)

Download from https://git-scm.com/download/win and install.
Open **Command Prompt** and verify: `git --version`

---

## STEP 2 — Create a GitHub Account & Repository

1. Go to https://github.com and sign up (free)
2. Click **+** → **New repository**
3. Name it: `naisha-coffee`
4. Keep it **Public**
5. **Do NOT** tick "Add README"
6. Click **Create repository**
7. Copy the repository URL (looks like `https://github.com/YOUR_USERNAME/naisha-coffee.git`)

---

## STEP 3 — Push Your Code to GitHub

Open **Command Prompt** inside the `naisha_coffee` project folder:

```cmd
cd C:\Projects\naisha_coffee

git init
git add .
git commit -m "Initial commit - Naisha Coffee website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/naisha-coffee.git
git push -u origin main
```

> Replace `YOUR_USERNAME` with your actual GitHub username.
> GitHub will ask for your username and password (use a Personal Access Token as password).

**Getting a GitHub Personal Access Token:**
1. GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)
2. Generate new token → check `repo` → Generate
3. Copy the token and use it as your password when pushing

---

## STEP 4 — Create a Render Account

1. Go to https://render.com and sign up (free) — use your GitHub account to sign up (easier!)
2. Verify your email

---

## STEP 5 — Deploy on Render

1. In Render dashboard → click **New +** → **Web Service**
2. Click **Connect a repository** → select `naisha-coffee`
3. Fill in the form:

| Field | Value |
|-------|-------|
| **Name** | `naisha-coffee` |
| **Region** | Singapore (closest to Bangladesh) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `./build.sh` |
| **Start Command** | `gunicorn naisha_coffee.wsgi:application` |

4. Scroll down to **Environment Variables** → click **Add Environment Variable**:

| Key | Value |
|-----|-------|
| `SECRET_KEY` | Click **Generate** button |
| `DEBUG` | `False` |

5. Select **Free** plan → click **Create Web Service**

---

## STEP 6 — Wait for Deployment

Render will:
- Install all packages
- Collect static files (CSS, JS, images)
- Run database migrations
- Load all demo content (menu, branches, gallery, team)
- Create admin account

This takes **3–5 minutes** on first deploy.

---

## STEP 7 — Your Site is Live! 🎉

Your website URL will be: `https://naisha-coffee.onrender.com`

| Page | URL |
|------|-----|
| Website | `https://naisha-coffee.onrender.com` |
| Admin Panel | `https://naisha-coffee.onrender.com/admin` |
| Admin Login | username: `admin` / password: `NaishaCoffee2024!` |

> ⚠️ **Change the admin password immediately** after first login!

---

## STEP 8 — Future Updates

Every time you make changes locally, just run:

```cmd
git add .
git commit -m "Your change description"
git push
```

Render will **automatically redeploy** within 2–3 minutes. ✅

---

## ⚠️ Free Tier Note

On Render's free tier, the server **sleeps after 15 minutes of inactivity**.
The first visit after sleep takes ~30 seconds to wake up.
To keep it always awake, upgrade to the **Starter plan ($7/month)**.

---

## Troubleshooting

**Site shows "Application Error"** → Check Render logs (Dashboard → your service → Logs tab)

**Images not showing** → Wait for build to complete and check the Logs tab for seed errors

**Admin password forgotten** → In Render dashboard → Shell tab → run:
```
python manage.py changepassword admin
```
