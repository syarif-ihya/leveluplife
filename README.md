# Level Up Life 🌱
**Level Up Life** is a gamified web app designed to help users improve their real-life skills and habits through quest-based progression and XP rewards.

This project combines:
- 🎨 Frontend: React + Vite + TailwindCSS  
- ⚙️ Backend: FastAPI (Python)  
- (optional) 🔥 Database: (Firebase / PostgreSQL / TBD)

## 🚀 Features
- Input Achievment and list your Achievment
- XP Rewards for store your Achievment
- Progress visualization
- User authentication (login/register)

## 🏗️ Project Structure

leveluplife/
├─ frontend/       # React + Vite + Tailwind
├─ backend/        # FastAPI (Python)
├─ docs/           # Documentation, diagrams, and notes
└─ README.md


## 🧠 Setup Instructions

### 1️⃣ Clone the repository
```bash
git clone https://github.com/syarif-ihya/leveluplife.git
cd leveluplife

cd frontend
npm install
npm run dev

cd backend
python -m venv venv
venv\Scripts\activate    # (Windows)
# source venv/bin/activate  # (Mac/Linux)

pip install -r requirements.txt
uvicorn app.main:app --reload

# Server jalan di http://127.0.0.1:8000
```


---

### 🔗 API Endpoint (Contoh)
```markdown
## 🔗 Example API Endpoints

| Method | Endpoint | Description |
|--------|-----------|-------------|
| GET | `/api/users` | Get all users |
| POST | `/api/achievments` | Add a new achievment |
| GET | `/api/rewards` | Get reward list |
```


## 👥 Team Members
| Role | Name | GitHub |
|------|------|---------|
| Project Manager | Syarif Ihya Izzuddin | [@syarifdev](https://github.com/syarifdev) |
| Frontend Dev | Aurel Arta Ghani | [@xx](#) |
| Backend Dev | M Dzhafa Abdurahman | [@xx](#) |
| Database Engineer | Aghniya Rizki Amalia | [@xx](#) |
| UI/UX Designer | Fathi Khasyi | [@xx](#) |


## 📚 Documentation
All additional notes, wireframes, and flowcharts can be found in the `/docs` folder.

## 💡 Notes
This project is built for learning and portfolio purposes as part of the LevelUpLife initiative.
