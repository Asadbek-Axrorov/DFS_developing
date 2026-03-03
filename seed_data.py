#!/usr/bin/env python
"""
SkillMate boshlang'ich ma'lumotlarini yaratish skripti.
Ishlatish: python seed_data.py
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillmate.settings')

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.accounts.models import User
from apps.courses.models import Category, Course, Module, Lesson


def run():
    print("🌱 Ma'lumotlarni yaratyapmiz...")

    # === CATEGORIES ===
    categories_data = [
        {'name': 'Ingliz tili', 'slug': 'ingliz-tili', 'icon': '🇬🇧', 'color': '#4F46E5'},
        {'name': 'Rus tili', 'slug': 'rus-tili', 'icon': '🇷🇺', 'color': '#DC2626'},
        {'name': 'Matematika', 'slug': 'matematika', 'icon': '📐', 'color': '#059669'},
        {'name': 'Fizika', 'slug': 'fizika', 'icon': '⚛️', 'color': '#D97706'},
    ]
    cats = {}
    for c in categories_data:
        cat, created = Category.objects.get_or_create(slug=c['slug'], defaults=c)
        cats[c['slug']] = cat
        print(f"  ✅ Kategoriya: {cat.name}")

    # === USERS ===
    # Admin
    if not User.objects.filter(username='admin').exists():
        admin = User.objects.create_superuser('admin', 'admin@skillmate.uz', 'admin123')
        admin.role = 'admin'
        admin.first_name = 'Admin'
        admin.last_name = 'SkillMate'
        admin.save()
        print("  ✅ Admin yaratildi: admin / admin123")

    # Mentors
    mentors_data = [
        {'username': 'mentor_english', 'first_name': 'Malika', 'last_name': 'Yusupova', 'bio': 'IELTS 8.5 ball. 5 yillik tajribali ingliz tili o\'qituvchisi.'},
        {'username': 'mentor_russian', 'first_name': 'Aleksey', 'last_name': 'Petrov', 'bio': 'Moskva davlat universitetini tamomlagan. 7 yil rus tili o\'qitaman.'},
        {'username': 'mentor_math', 'first_name': 'Jasur', 'last_name': 'Toshmatov', 'bio': 'Matematika fanlari nomzodi. Olimpiada g\'oliblarini tayyorlayman.'},
        {'username': 'mentor_physics', 'first_name': 'Nilufar', 'last_name': 'Karimova', 'bio': 'Fizika-matematika fanlari nomzodi. MIT online kurslarini tamomlagan.'},
    ]
    mentors = {}
    for m in mentors_data:
        if not User.objects.filter(username=m['username']).exists():
            mentor = User.objects.create_user(m['username'], f"{m['username']}@skillmate.uz", 'mentor123')
            mentor.role = 'mentor'
            mentor.first_name = m['first_name']
            mentor.last_name = m['last_name']
            mentor.bio = m['bio']
            mentor.save()
            print(f"  ✅ Mentor: {mentor.get_full_name()} ({m['username']} / mentor123)")
        mentors[m['username']] = User.objects.get(username=m['username'])

    # Curator
    if not User.objects.filter(username='curator1').exists():
        curator = User.objects.create_user('curator1', 'curator@skillmate.uz', 'curator123')
        curator.role = 'curator'
        curator.first_name = 'Sardor'
        curator.last_name = 'Nazarov'
        curator.save()
        print("  ✅ Kurator: Sardor Nazarov (curator1 / curator123)")

    # Student
    if not User.objects.filter(username='student1').exists():
        student = User.objects.create_user('student1', 'student@skillmate.uz', 'student123')
        student.role = 'student'
        student.first_name = 'Aziz'
        student.last_name = 'Rahimov'
        student.save()
        print("  ✅ Talaba: Aziz Rahimov (student1 / student123)")

    curator_obj = User.objects.get(username='curator1')

    # === COURSES ===
    courses_data = [
        {
            'title': 'Ingliz tili — A1 dan B2 gacha',
            'slug': 'ingliz-tili-a1-b2',
            'short_description': 'Noldan boshlab ingliz tilini o\'rganing. Grammatika, leksika va suhbat ko\'nikmalari.',
            'description': 'Ushbu kurs ingliz tilini boshlang\'ichdan o\'rta darajagacha o\'rgatadi. Kursda grammatika qoidalari, leksika, tinglab tushunish, so\'zlashuv va yozish ko\'nikmalari ishlab chiqiladi. Darslar interaktiv bo\'lib, real hayotiy vaziyatlar asosida qurilgan.',
            'category': cats['ingliz-tili'],
            'mentor_key': 'mentor_english',
            'level': 'beginner',
            'language': 'uz',
            'duration_hours': 60,
            'is_free': False,
            'price': 299000,
            'students_count': 234,
            'rating': 4.8,
            'is_published': True,
            'is_featured': True,
            'modules': [
                {'title': '1-modul: Alfavit va asosiy iboralar', 'lessons': [
                    ('Ingliz alifbosi', 'video', 'https://www.youtube.com/watch?v=dQw4w9WgXcQ', 15),
                    ('Salomlashish va tanishish', 'video', '', 20),
                    ('Raqamlar 1-100', 'text', '', 10),
                    ('1-modul testi', 'quiz', '', 15),
                ]},
                {'title': '2-modul: Grammatika asoslari', 'lessons': [
                    ('To be fe\'li', 'video', '', 25),
                    ('Hozirgi zamon (Present Simple)', 'video', '', 30),
                    ('Savol tuzish', 'text', '', 20),
                ]},
                {'title': '3-modul: Kundalik suhbat', 'lessons': [
                    ('Oila haqida gaplashish', 'video', '', 25),
                    ('Ish va kasb', 'video', '', 30),
                    ('Savdo va do\'kon', 'video', '', 20),
                ]},
            ]
        },
        {
            'title': 'Rus tili — Boshlang\'ichdan O\'rtacha',
            'slug': 'rus-tili-boshlangich',
            'short_description': 'Rus tilini noldan o\'rganing. Kirillcha, grammatika va kundalik suhbat.',
            'description': 'Rus tilini boshlang\'ichdan o\'rganing. Kirill alifbosi, asosiy grammatika, kundalik suhbat va leksika. Rossiyaga safar yoki ish uchun zarur bo\'lgan barcha ko\'nikmalar.',
            'category': cats['rus-tili'],
            'mentor_key': 'mentor_russian',
            'level': 'beginner',
            'language': 'uz',
            'duration_hours': 48,
            'is_free': True,
            'price': 0,
            'students_count': 189,
            'rating': 4.7,
            'is_published': True,
            'is_featured': True,
            'modules': [
                {'title': '1-modul: Kirill alifbosi', 'lessons': [
                    ('Unlilar va undoshlar', 'video', '', 20),
                    ('O\'qish mashqlari', 'video', '', 25),
                    ('Alifbo testi', 'quiz', '', 10),
                ]},
                {'title': '2-modul: Asosiy grammatika', 'lessons': [
                    ('Ot turkumlari (Rod)', 'video', '', 30),
                    ('Kelishiklar (Padejlar)', 'video', '', 35),
                    ('Fe\'l tuslanishi', 'text', '', 25),
                ]},
            ]
        },
        {
            'title': 'Matematika — Algebra va Geometriya',
            'slug': 'matematika-algebra-geometriya',
            'short_description': 'Maktab matematikasini chuqurlashtiring. Imtihon va olimpiadasiga tayyorlanish.',
            'description': 'Ushbu kurs algebra, geometriya va trigonometriyani qamrab oladi. DTM imtihoniga tayyorlanish uchun ideal. Har bir mavzu ko\'plab misollar va masalalar bilan tushuntiriladi.',
            'category': cats['matematika'],
            'mentor_key': 'mentor_math',
            'level': 'intermediate',
            'language': 'uz',
            'duration_hours': 72,
            'is_free': False,
            'price': 349000,
            'students_count': 312,
            'rating': 4.9,
            'is_published': True,
            'is_featured': True,
            'modules': [
                {'title': '1-modul: Algebra asoslari', 'lessons': [
                    ('Natural sonlar va amallar', 'video', '', 20),
                    ('Kasrlar', 'video', '', 25),
                    ('Tenglamalar', 'video', '', 30),
                    ('Testlar', 'quiz', '', 20),
                ]},
                {'title': '2-modul: Geometriya', 'lessons': [
                    ('Uchburchaklar', 'video', '', 35),
                    ('To\'rtburchaklar', 'video', '', 30),
                    ('Aylana va doira', 'video', '', 25),
                ]},
                {'title': '3-modul: Trigonometriya', 'lessons': [
                    ('Sin, cos, tan funksiyalari', 'video', '', 40),
                    ('Trigonometrik tenglamalar', 'video', '', 35),
                ]},
            ]
        },
        {
            'title': 'Fizika — Mexanika va Termodinamika',
            'slug': 'fizika-mexanika-termodinamika',
            'short_description': 'Fizika fanini chuqur o\'rganing. Mexanika, termodinamika va elektr fizikasi.',
            'description': 'Ushbu kurs mexanika, dinamika, termodinamika va elektrdinamikani o\'z ichiga oladi. DTM va xalqaro olimpiadalarga tayyorlanish uchun mo\'ljallangan. Formulalar, misollar va masalalar yechish usullari.',
            'category': cats['fizika'],
            'mentor_key': 'mentor_physics',
            'level': 'intermediate',
            'language': 'uz',
            'duration_hours': 64,
            'is_free': False,
            'price': 329000,
            'students_count': 145,
            'rating': 4.8,
            'is_published': True,
            'is_featured': True,
            'modules': [
                {'title': '1-modul: Kinematika', 'lessons': [
                    ('Tezlanish va tezlik', 'video', '', 30),
                    ('Bir tekis harakat', 'video', '', 25),
                    ('Tekislikdagi harakat', 'video', '', 30),
                ]},
                {'title': '2-modul: Dinamika', 'lessons': [
                    ('Nyuton qonunlari', 'video', '', 35),
                    ('Ishqalanish kuchi', 'video', '', 25),
                    ('Tortishish qonuni', 'video', '', 30),
                ]},
                {'title': '3-modul: Termodinamika', 'lessons': [
                    ('Issiqlik miqdori', 'video', '', 30),
                    ('Gaz qonunlari', 'video', '', 35),
                ]},
            ]
        },
    ]

    for c_data in courses_data:
        if Course.objects.filter(slug=c_data['slug']).exists():
            print(f"  ⏭️  Kurs mavjud: {c_data['title']}")
            continue

        course = Course.objects.create(
            title=c_data['title'],
            slug=c_data['slug'],
            short_description=c_data['short_description'],
            description=c_data['description'],
            category=c_data['category'],
            mentor=mentors[c_data['mentor_key']],
            curator=curator_obj,
            level=c_data['level'],
            language=c_data['language'],
            duration_hours=c_data['duration_hours'],
            is_free=c_data['is_free'],
            price=c_data['price'],
            students_count=c_data['students_count'],
            rating=c_data['rating'],
            is_published=c_data['is_published'],
            is_featured=c_data['is_featured'],
        )

        for i, m_data in enumerate(c_data['modules']):
            module = Module.objects.create(
                course=course,
                title=m_data['title'],
                order=i + 1
            )
            for j, (title, ltype, url, dur) in enumerate(m_data['lessons']):
                Lesson.objects.create(
                    module=module,
                    title=title,
                    lesson_type=ltype,
                    video_url=url,
                    duration_minutes=dur,
                    order=j + 1,
                    is_free_preview=(j == 0),
                )

        print(f"  ✅ Kurs yaratildi: {course.title}")

    print()
    print("✨ Tayyor! Quyidagi hisoblar yaratildi:")
    print("  👤 admin / admin123          — Admin")
    print("  👤 mentor_english / mentor123 — Ingliz tili mentori")
    print("  👤 mentor_russian / mentor123 — Rus tili mentori")
    print("  👤 mentor_math / mentor123    — Matematika mentori")
    print("  👤 mentor_physics / mentor123 — Fizika mentori")
    print("  👤 curator1 / curator123      — Kurator")
    print("  👤 student1 / student123      — Talaba")
    print()
    print("🚀 Serverni ishga tushiring: python manage.py runserver")


if __name__ == '__main__':
    run()
