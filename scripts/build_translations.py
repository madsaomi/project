"""Сборка переводов без GNU gettext: генерирует и компилирует .po/.mo через polib.

Использование:
    venv\\Scripts\\python.exe scripts\\build_translations.py

msgstr заполняются из CATALOGS ниже. Строки, для которых перевод не найден,
останутся пустыми — Django откатится к msgid (русский исходник).
"""
import os
import sys

import polib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCALE_DIR = os.path.join(BASE_DIR, 'locale')

CATALOGS = {
    'uz': {
        'Стажировки': 'Stajirovkalar',
        'Уведомления': 'Bildirishnomalar',
        'Сообщения': 'Xabarlar',
        'Мои стажировки': 'Mening stajirovklarim',
        'Моя компания': 'Kompaniyam',
        'Дашборд': 'Boshqaruv paneli',
        'Создать стажировку': 'Stajirovka yaratish',
        'Выйти': 'Chiqish',
        'Войти': 'Kirish',
        'Зарегистрироваться': 'Ro‘yxatdan o‘tish',
        'Все права защищены.': 'Barcha huquqlar himoyalangan.',
        'стажировки для студентов': 'talabalar uchun stajirovkalar',
        'Начни свою карьеру со': 'Karyerangizni bilan boshlang:',
        'Найти стажировку': 'Stajirovka topish',
        'Я работодатель': 'Men ish beruvchiman',
        'Пароль': 'Parol',
        'Роль': 'Rol',
        'Студент': 'Talaba',
        'Работодатель': 'Ish beruvchi',
        'Регистрация': 'Ro‘yxatdan o‘tish',
        'Вход в аккаунт': 'Hisobga kirish',
        'Забыли пароль?': 'Parolni eslay olmaysizmi?',
        'Сброс пароля': 'Parolni tiklash',
        'Укажите email — пришлём ссылку для создания нового пароля.':
            'Email kiriting — yangi parol uchun havola yuboramiz.',
        'Отправить ссылку': 'Havolani yuborish',
        'Вернуться ко входу': 'Kirish sahifasiga qaytish',
        'Проверьте почту': 'Pochtangizni tekshiring',
        'Письмо отправлено': 'Xabar yuborildi',
        'Если аккаунт с таким email существует, мы отправили туда ссылку для сброса пароля. Проверьте почту (и папку «Спам»).':
            'Bunday email bilan hisob mavjud bo‘lsa, parolni tiklash havolasini yubordik. Pochtani (va «Spam» papkasini) tekshiring.',
        'Ко входу': 'Kirishga',
        'Новый пароль': 'Yangi parol',
        'Придумайте новый пароль': 'Yangi parol o‘ylab toping',
        'Сохранить пароль': 'Parolni saqlash',
        'Ссылка недействительна': 'Havola yaroqsiz',
        'Ссылка для сброса устарела или уже была использована. Запросите сброс пароля ещё раз.':
            'Tiklash havolasi eskirgan yoki allaqachon ishlatilgan. Parolni tiklashni yana so‘rang.',
        'Запросить заново': 'Yana so‘rash',
        'Пароль изменён': 'Parol o‘zgartirildi',
        'Теперь войдите с новым паролем.': 'Endi yangi parol bilan kiring.',
        'Каталог стажировок': 'Stajirovkalar katalogi',
        'Актуальные стажировки для студентов: удалённые и в офисе, оплачиваемые и с гибким графиком. Откликайся напрямую работодателям.':
            'Talabalar uchun dolzarb stajirovkalar: masofaviy va ofisdagi, to‘lanadigan va moslashuvchan jadval bilan.',
        'Фильтры': 'Filtrlar',
        'Отклики и текущий статус по каждому': 'Har biri bo‘yicha arizalar va joriy holat',
        'Всего откликов': 'Jami arizalar',
        'На рассмотрении': 'Ko‘rib chiqilmoqda',
        'Активные': 'Faol',
        'Завершённые': 'Yakunlangan',
        'Кандидаты': 'Nomzodlar',
        'Управление откликами на ваши стажировки': 'Stajirovkalaringizga kelib tushgan arizalarni boshqarish',
        'Новая стажировка': 'Yangi stajirovka',
        'откл.': 'ariza',
        'Активна': 'Faol',
        'Закрыта': 'Yopiq',
        'Изменить': 'Tahrirlash',
        'У вас ещё нет стажировок — опубликуйте первую.':
            'Sizda hali stajirovka yo‘q — birinchisini e’lon qiling.',
        'Новые отклики': 'Yangi arizalar',
        'В процессе': 'Jarayonda',
        'Завершено': 'Yakunlangan',
        'Вы откликнулись': 'Siz ariza topshirdingiz',
        'Откликнуться': 'Ariza yuborish',
        'Войти для отклика': 'Ariza uchun kiring',
        'Только студенты могут откликаться на стажировки.':
            'Faqat talabalar stajirovkalarga ariza topshirishi mumkin.',
        'Ничего не найдено': 'Hech narsa topilmadi',
        'Попробуйте изменить параметры фильтра.': 'Filtrlar parametrlarini o‘zgartirib ko‘ring.',
        'Оплачиваемая': 'To‘lanadigan',
        'Описание стажировки': 'Stajirovka tavsifi',
        'Требования': 'Talablar',
        'Обязанности': 'Vazifalar',
        'Подробнее': 'Batafsil',
        'Последние события по вашим стажировкам': 'Stajirovkalaringiz bo‘yicha so‘nggi hodisalar',
        'Прочитать все': 'Hammasini o‘qilgan deb belgilash',
        'новое': 'yangi',
        'Уведомлений пока нет': 'Hali bildirishnomalar yo‘q',
        'Здесь появятся отклики и изменения статусов.':
            'Bu yerda arizalar va holat o‘zgarishlari paydo bo‘ladi.',
        'Ваши чаты с работодателями': 'Ish beruvchilar bilan suhbatlaringiz',
        'Ваши чаты с кандидатами': 'Nomzodlar bilan suhbatlaringiz',
        'Нет сообщений': 'Xabarlar yo‘q',
        'У вас пока нет чатов': 'Sizda hali chatlar yo‘q',
        'Откликнитесь на стажировку, чтобы начать общение.':
            'Suhbatni boshlash uchun stajirovkaga ariza yuboring.',
        'Дождитесь откликов студентов.': 'Talabalarning arizalarini kutib turing.',
        'Поиск': 'Qidirish',
        'Категория': 'Kategoriya',
        'Все категории': 'Barcha kategoriyalar',
        'Должность или компания…': 'Lavozim yoki kompaniya…',
        'Найдите идеальную стажировку для старта карьеры':
            'Karyerani boshlash uchun ideal stajirovkani toping',
        'Редактирование': 'Tahrirlash',
        'Редактирование стажировки': 'Stajirovkani tahrirlash',
        'Публикация стажировки': 'Stajirovkani e’lon qilish',
        'Изменения сразу видны студентам. Снимите галочку «Активна», чтобы закрыть набор.':
            'O‘zgarishlar talabalarga darhol ko‘rinadi. Yopish uchun «Faol» belgisini oling.',
        'Заполните детали, чтобы привлечь лучших студентов.':
            'Eng yaxshi talabalarni jalb qilish uchun tafsilotlarni to‘ldiring.',
        'видна в каталоге': 'katalogda ko‘rinadi',
        'Отмена': 'Bekor qilish',
        'Сохранить': 'Saqlash',
        'Опубликовать': 'E’lon qilish',
        'Конструктор резюме': 'Rezyume konstruktori',
        'Создание профиля (Резюме)': 'Profil yaratish (Rezyume)',
        'ФИО': 'F.I.Sh.',
        'Желаемая должность': 'Orzu qilingan lavozim',
        'О себе': 'O‘zingiz haqingizda',
        'Вуз / Колледж': 'OTM / Kollej',
        'Специальность': 'Mutaxassislik',
        'Сохранить и посмотреть': 'Saqlash va ko‘rish',
        'Чат': 'Suhbat',
        'Введите сообщение...': 'Xabar kiriting...',
    },
    'en': {
        'Стажировки': 'Internships',
        'Уведомления': 'Notifications',
        'Сообщения': 'Messages',
        'Мои стажировки': 'My internships',
        'Моя компания': 'My company',
        'Дашборд': 'Dashboard',
        'Создать стажировку': 'Post an internship',
        'Выйти': 'Log out',
        'Войти': 'Log in',
        'Зарегистрироваться': 'Sign up',
        'Все права защищены.': 'All rights reserved.',
        'стажировки для студентов': 'internships for students',
        'Начни свою карьеру со': 'Start your career with',
        'Найти стажировку': 'Find an internship',
        'Я работодатель': "I'm an employer",
        'Пароль': 'Password',
        'Роль': 'Role',
        'Студент': 'Student',
        'Работодатель': 'Employer',
        'Регистрация': 'Sign up',
        'Вход в аккаунт': 'Log in',
        'Забыли пароль?': 'Forgot password?',
        'Сброс пароля': 'Password reset',
        'Укажите email — пришлём ссылку для создания нового пароля.':
            'Enter your email and we will send you a link to set a new password.',
        'Отправить ссылку': 'Send link',
        'Вернуться ко входу': 'Back to login',
        'Проверьте почту': 'Check your inbox',
        'Письмо отправлено': 'Email sent',
        'Если аккаунт с таким email существует, мы отправили туда ссылку для сброса пароля. Проверьте почту (и папку «Спам»).':
            "If an account with this email exists, we've sent a password reset link to it. Check your inbox (and spam folder).",
        'Ко входу': 'To login',
        'Новый пароль': 'New password',
        'Придумайте новый пароль': 'Choose a new password',
        'Сохранить пароль': 'Save password',
        'Ссылка недействительна': 'Invalid link',
        'Ссылка для сброса устарела или уже была использована. Запросите сброс пароля ещё раз.':
            'The reset link has expired or was already used. Please request a new one.',
        'Запросить заново': 'Request again',
        'Пароль изменён': 'Password changed',
        'Теперь войдите с новым паролем.': 'Now log in with your new password.',
        'Каталог стажировок': 'Internship catalog',
        'Актуальные стажировки для студентов: удалённые и в офисе, оплачиваемые и с гибким графиком. Откликайся напрямую работодателям.':
            'Current internships for students: remote and on-site, paid and flexible. Apply directly to employers.',
        'Фильтры': 'Filters',
        'Отклики и текущий статус по каждому': 'Your applications and their current status',
        'Всего откликов': 'Total applications',
        'На рассмотрении': 'Pending',
        'Активные': 'Active',
        'Завершённые': 'Completed',
        'Кандидаты': 'Candidates',
        'Управление откликами на ваши стажировки': 'Manage applications to your internships',
        'Новая стажировка': 'New internship',
        'откл.': 'apps',
        'Активна': 'Active',
        'Закрыта': 'Closed',
        'Изменить': 'Edit',
        'У вас ещё нет стажировок — опубликуйте первую.':
            "You have no internships yet — post your first one.",
        'Новые отклики': 'New applications',
        'В процессе': 'In progress',
        'Завершено': 'Completed',
        'Вы откликнулись': 'You have applied',
        'Откликнуться': 'Apply now',
        'Войти для отклика': 'Log in to apply',
        'Только студенты могут откликаться на стажировки.':
            'Only students can apply for internships.',
        'Ничего не найдено': 'Nothing found',
        'Попробуйте изменить параметры фильтра.': 'Try adjusting the filters.',
        'Оплачиваемая': 'Paid',
        'Описание стажировки': 'About the internship',
        'Требования': 'Requirements',
        'Обязанности': 'Responsibilities',
        'Подробнее': 'Details',
        'Последние события по вашим стажировкам': 'Latest updates on your internships',
        'Прочитать все': 'Mark all as read',
        'новое': 'new',
        'Уведомлений пока нет': 'No notifications yet',
        'Здесь появятся отклики и изменения статусов.':
            'Applications and status changes will appear here.',
        'Ваши чаты с работодателями': 'Your chats with employers',
        'Ваши чаты с кандидатами': 'Your chats with candidates',
        'Нет сообщений': 'No messages yet',
        'У вас пока нет чатов': "You don't have any chats yet",
        'Откликнитесь на стажировку, чтобы начать общение.':
            'Apply for an internship to start a conversation.',
        'Дождитесь откликов студентов.': 'Wait for student applications.',
        'Поиск': 'Search',
        'Категория': 'Category',
        'Все категории': 'All categories',
        'Должность или компания…': 'Position or company…',
        'Найдите идеальную стажировку для старта карьеры':
            'Find the perfect internship to start your career',
        'Редактирование': 'Edit',
        'Редактирование стажировки': 'Edit internship',
        'Публикация стажировки': 'Post an internship',
        'Изменения сразу видны студентам. Снимите галочку «Активна», чтобы закрыть набор.':
            'Changes are visible to students immediately. Uncheck "Active" to close applications.',
        'Заполните детали, чтобы привлечь лучших студентов.':
            'Fill in the details to attract the best students.',
        'видна в каталоге': 'visible in catalog',
        'Отмена': 'Cancel',
        'Сохранить': 'Save',
        'Опубликовать': 'Publish',
        'Конструктор резюме': 'Resume builder',
        'Создание профиля (Резюме)': 'Create profile (Resume)',
        'ФИО': 'Full name',
        'Желаемая должность': 'Desired position',
        'О себе': 'About me',
        'Вуз / Колледж': 'University / College',
        'Специальность': 'Major',
        'Сохранить и посмотреть': 'Save and preview',
        'Чат': 'Chat',
        'Введите сообщение...': 'Type a message...',
    },
}

HEADER = {
    'Project-Id-Version': 'StudCareer',
    'Language': '',
    'MIME-Version': '1.0',
    'Content-Type': 'text/plain; charset=UTF-8',
    'Content-Transfer-Encoding': '8bit',
}


def build():
    for lang, catalog in CATALOGS.items():
        po_dir = os.path.join(LOCALE_DIR, lang, 'LC_MESSAGES')
        os.makedirs(po_dir, exist_ok=True)

        po = polib.POFile()
        po.metadata = {**HEADER, 'Language': lang}
        for msgid, msgstr in sorted(catalog.items()):
            entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
            po.append(entry)

        po_path = os.path.join(po_dir, 'django.po')
        mo_path = os.path.join(po_dir, 'django.mo')
        po.save(po_path)
        po.save_as_mofile(mo_path)
        print(f'{lang}: {len(catalog)} strings -> {po_path} + django.mo')

    print('DONE')


if __name__ == '__main__':
    sys.exit(build())
