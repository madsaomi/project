---
name: data_models_reference
description: Полная шпаргалка по всем полям всех моделей проекта. Используй как справочник чтобы не читать исходный код моделей.
---

# Справочник по моделям (Data Models Reference)

> Используй этот файл как единый источник истины по схеме базы данных. Не нужно открывать `models.py`.

---

## `accounts.User` (CustomUser)
| Поле | Тип | Описание |
|---|---|---|
| `email` | EmailField (unique) | Логин (USERNAME_FIELD) |
| `username` | CharField | Вспомогательное поле |
| `role` | CharField | `student`, `employer`, `admin` |
| `phone` | CharField | Телефон, необязательное |
| `avatar` | ImageField | Аватарка (upload: `avatars/`) |
| `preferred_language` | CharField | `ru`, `uz`, `en` |
| `is_verified` | BooleanField | Email подтвержден? |
| `is_banned` | BooleanField | Заблокирован ли юзер? |
| `accepted_terms` | BooleanField | Принял ли ToS? |
| `created_at` | DateTimeField | Авто-время создания |

---

## `profiles.StudentProfile`
| Поле | Тип | Описание |
|---|---|---|
| `user` | OneToOneField → User | Связь с аккаунтом |
| `full_name` | CharField | ФИО |
| `photo` | ImageField | Фото профиля |
| `headline` | CharField | "Python Developer Intern" |
| `about` | TextField | О себе |
| `institution` | CharField | Вуз / Колледж |
| `course` | PositiveSmallIntegerField | Курс (1-6) |
| `specialty` | CharField | Специальность |
| `location` | CharField | Город |
| `phone` | CharField | Телефон (публичный) |
| `portfolio_url` | URLField | Ссылка на портфолио |
| `github_url` | URLField | GitHub |
| `linkedin_url` | URLField | LinkedIn |
| `behance_url` | URLField | Behance |
| `resume_theme` | CharField | `classic`, `modern`, `minimal` |
| `is_public` | BooleanField | Профиль открыт всем? |

## `profiles.Skill`
| Поле | Тип | Описание |
|---|---|---|
| `profile` | ForeignKey → StudentProfile | related_name=`skills` |
| `name` | CharField | Название навыка |
| `level` | PositiveSmallIntegerField | Уровень 1-5 |

## `profiles.LanguageSkill`
| Поле | Тип | Описание |
|---|---|---|
| `profile` | ForeignKey → StudentProfile | related_name=`language_skills` |
| `name` | CharField | Язык (Русский, Английский) |
| `level` | CharField | `A1`, `B2`, `Native` |

## `profiles.InternshipExperience`
> ⚠️ Создается АВТОМАТИЧЕСКИ при завершении стажировки (`InternshipParticipant.status = COMPLETED`)
| Поле | Тип | Описание |
|---|---|---|
| `profile` | ForeignKey → StudentProfile | related_name=`internship_experiences` |
| `internship` | OneToOneField → Internship | Источник опыта |
| `company_name` | CharField | Копия названия компании |
| `position` | CharField | Должность |
| `start_date` / `end_date` | DateField | Период стажировки |
| `description` | TextField | Описание |

---

## `companies.Company`
| Поле | Тип | Описание |
|---|---|---|
| `user` | OneToOneField → User | Работодатель |
| `name` | CharField | Название компании |
| `logo` | ImageField | Логотип |
| `description` | TextField | О компании |
| `website` | URLField | Сайт |
| `industry` | CharField | Отрасль |
| `size` | CharField | `1-10`, `11-50`, `51-200`, `200+` |
| `founded_year` | PositiveIntegerField | Год основания |
| `verification_status` | CharField | `pending`, `verified`, `rejected` |

---

## `internships.Internship`
| Поле | Тип | Описание |
|---|---|---|
| `company` | ForeignKey → Company | related_name=`internships` |
| `title` | CharField | Название стажировки |
| `slug` | SlugField (unique) | URL-идентификатор |
| `description` | TextField | Описание |
| `internship_type` | CharField | `internship`, `part_time`, `project` |
| `work_format` | CharField | `office`, `remote`, `hybrid` |
| `category` | ForeignKey → Category | Категория |
| `is_paid` | BooleanField | Оплачиваемая? |
| `salary_amount` | PositiveIntegerField | Сумма зарплаты |
| `currency` | CharField | Валюта (default: `UZS`) |
| `duration_months` | PositiveSmallIntegerField | Длительность в месяцах |
| `deadline` | DateField | Дедлайн подачи заявок |
| `is_active` | BooleanField | Опубликована? |
| `is_featured` | BooleanField | Закрепленная/Featured? |

## `internships.InternshipParticipant`
| Поле | Тип | Описание |
|---|---|---|
| `internship` | ForeignKey → Internship | related_name=`participants` |
| `student` | ForeignKey → User | related_name=`internship_participations` |
| `status` | CharField | `pending`, `active`, `completed`, `cancelled` |
| `start_date` / `end_date` | DateField | Даты стажировки |
| `position` | CharField | Должность на стажировке |

> Unique together: `(internship, student)` — студент не может дважды откликнуться на одну стажировку.
> Property `conversation` → Conversation студента с компанией (или None).

## `messaging.Conversation`
| Поле | Тип | Описание |
|---|---|---|
| `student` | ForeignKey → User | related_name=`student_conversations` |
| `company` | ForeignKey → Company | related_name=`conversations` |
| `created_at` / `updated_at` | DateTimeField | |

> Unique together: `(student, company)`. Создаётся автоматически при отклике (apply).
> `Message` — FK conversation, sender, content, is_read.

## `notifications.Notification`
| Поле | Тип | Описание |
|---|---|---|
| `recipient` | ForeignKey → User | related_name=`notifications` |
| `message` | CharField(255) | Текст уведомления |
| `url` | CharField(255) | Куда вести по клику (может быть пустым) |
| `is_read` | BooleanField | По умолчанию False |
| `created_at` | DateTimeField | auto_now_add, сортировка `-created_at` |

> Создаются сигналом internships: новый отклик → работодателю, смена статуса → студенту.
> Бейдж в navbar через context processor `unread_notifications`.
