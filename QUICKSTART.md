# CEAL Calendar - Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Step 1: Start the Application

```bash
# Navigate to project
cd d:\Github\CEAL-Calender

# Copy environment files
copy .env.example .env
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env

# Start all services with Docker
docker-compose up --build
```

**Wait 2-3 minutes** for all services to initialize.

### Step 2: Seed the Database

```bash
# In a new terminal, seed clubs
docker-compose exec backend python seed_data.py
```

### Step 3: Access the Application

Open your browser:
- **Frontend**: http://localhost:3100
- **Admin Panel**: http://localhost:8100/admin (login: admin / admin123)
- **Email UI** (MailHog): http://localhost:8026

---

## 📝 Create Your First Event

1. **Sign Up**:
   - Go to http://localhost:3100
   - Click "Sign up"
   - Choose a club (e.g., "IEEE Computer Society")
   - Complete registration

2. **Create Event**:
   - Click "+ Create Event"
   - Fill in details (title, location, date/time)
   - Click "Create Event"

3. **Test Notifications**:
   - Go to Settings
   - Enable notifications
   - Set time to 1 minute from now
   - Create another event
   - Check http://localhost:8026 after the time

---

## 🛑 Troubleshooting

### Services not starting?
```bash
docker-compose down
docker-compose up --build
```

### Database errors?
```bash
docker-compose down -v  # Removes volumes
docker-compose up --build
docker-compose exec backend python seed_data.py
```

### Frontend not loading?
```bash
# Check logs
docker-compose logs frontend

# Restart frontend
docker-compose restart frontend
```

---

## 📚 Full Documentation

- [README.md](file:///d:/Github/CEAL-Calender/README.md) - Complete installation guide
- [Walkthrough](file:///C:/Users/sreed/.gemini/antigravity/brain/ef8fa467-8a94-4ed7-9382-cedbed0dca21/walkthrough.md) - Detailed implementation walkthrough

---

**Happy event managing! 🎉**
