@echo off
chcp 65001 >nul
echo ========================================
echo   SkillMate LMS - O'rnatish
echo ========================================
echo.

echo Python versiyasi tekshirilmoqda...
python --version
echo.

echo [1/5] Virtual muhit yaratilmoqda...
python -m venv venv
call venv\Scripts\activate.bat
echo   OK!

echo.
echo [2/5] Django o'rnatilmoqda (Python 3.14 uchun 5.1+)...
pip install "Django>=5.1" --quiet
echo   OK!

echo.
echo [3/5] Pillow o'rnatilmoqda...
pip install --pre Pillow --quiet 2>nul && echo   OK! || echo   Pillow o'rnatilmadi - davom etiladi...

echo.
echo [4/5] Ma'lumotlar bazasi yaratilmoqda...
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py makemigrations lms
python manage.py makemigrations dashboard
python manage.py migrate
echo   OK!

echo.
echo [5/5] Namuna ma'lumotlar yuklanmoqda...
python seed_data.py

echo.
echo ========================================
echo   TAYYOR! Brauzerda oching:
echo   http://127.0.0.1:8000
echo.
echo   HISOBLAR:
echo   admin         / admin123
echo   curator1      / curator123
echo   mentor_english/ mentor123
echo   student1      / student123
echo ========================================
echo.
python manage.py runserver
pause
