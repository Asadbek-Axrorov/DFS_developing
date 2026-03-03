# SkillMate LMS — O'rnatish Qo'llanmasi

## 🚀 Loyiha haqida

SkillMate — zamonaviy Django-ga asoslangan LMS (Learning Management System) platformasi.

### Xususiyatlar:
- 🎓 4 ta kurs: Ingliz tili, Rus tili, Matematika, Fizika
- 👨‍🏫 Mentor va Kurator boshqaruv paneli
- 🎬 Video darslar (YouTube va fayl yuklash)
- 📊 Progress tracking
- ⭐ Chiroyli admin panel
- 📱 Responsive dizayn

---

## ⚙️ O'rnatish

### 1. Python virtual muhit yarating
```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
# yoki
venv\Scripts\activate      # Windows
```

### 2. Kutubxonalarni o'rnating
```bash
pip install -r requirements.txt
```

### 3. Ma'lumotlar bazasini yarating
```bash
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py makemigrations
python manage.py migrate
```

### 4. Boshlang'ich ma'lumotlarni yuklang
```bash
python seed_data.py
```

### 5. Serverni ishga tushiring
```bash
python manage.py runserver
```

Brauzerda oching: http://127.0.0.1:8000

---

## 👥 Foydalanuvchi hisoblar

| Username | Parol | Rol |
|----------|-------|-----|
| admin | admin123 | Admin |
| mentor_english | mentor123 | Ingliz tili mentori |
| mentor_russian | mentor123 | Rus tili mentori |
| mentor_math | mentor123 | Matematika mentori |
| mentor_physics | mentor123 | Fizika mentori |
| curator1 | curator123 | Kurator |
| student1 | student123 | Talaba |

---

## 🔗 Sahifalar

| URL | Tavsif |
|-----|--------|
| / | Bosh sahifa |
| /courses/ | Kurslar ro'yxati |
| /courses/<slug>/ | Kurs sahifasi |
| /accounts/login/ | Kirish |
| /accounts/register/ | Ro'yxatdan o'tish |
| /dashboard/ | Dashboard (rol bo'yicha) |
| /lms/course/<slug>/ | Video dars o'ynatgich |
| /admin/ | Django admin panel |

---

## 👨‍🏫 Mentor imkoniyatlari
- Kurs yaratish va tahrirlash
- Modul va darslar qo'shish
- Video URL yoki fayl yuklash

## 🎯 Kurator imkoniyatlari
- Kurs yaratish va tahrirlash
- Talabalarni boshqarish
- Mentorlarni nazorat qilish

## ⚡ Admin imkoniyatlari
- Django admin panel (/admin/)
- Barcha foydalanuvchilarni boshqarish
- Barcha kurslarni boshqarish

---

## 📁 Loyiha tuzilmasi

```
skillmate_lms/
├── manage.py
├── requirements.txt
├── seed_data.py         # Boshlang'ich ma'lumotlar
├── skillmate/
│   ├── settings.py
│   └── urls.py
├── apps/
│   ├── accounts/        # Foydalanuvchilar
│   ├── courses/         # Kurslar
│   ├── lms/             # Video o'ynatgich
│   └── dashboard/       # Boshqaruv paneli
├── templates/           # HTML shablonlar
└── static/              # CSS, JS, rasmlar
```
