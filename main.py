import random
from datacenter.models import (Schoolkid, Mark, Chastisement, Lesson, Commendation)

COMMENDATION_TEXT = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Гораздо лучше, чем я ожидал!',
    'Ты меня приятно удивил!',
    'Великолепно!',
    'Прекрасно!',
    'Ты меня очень обрадовал!',
    'Именно этого я давно ждал от тебя!',
    'Сказано здорово – просто и ясно!',
    'Ты, как всегда, точен!',
    'Очень хороший ответ!',
    'Талантливо!',
    'Ты сегодня прыгнул выше головы!',
    'Я поражен!',
    'Уже существенно лучше!',
    'Потрясающе!',
    'Замечательно!',
    'Прекрасное начало!',
    'Так держать!',
    'Ты на верном пути!',
    'Здорово!',
    'Это как раз то, что нужно!',
    'Я тобой горжусь!',
    'С каждым разом у тебя получается всё лучше!',
    'Мы с тобой не зря поработали!',
    'Я вижу, как ты стараешься!',
    'Ты растешь над собой!',
    'Ты многое сделал, я это вижу!',
    'Теперь у тебя точно все получится!'
]


def get_schoolkid(schoolkid_name):
    if not schoolkid_name:
        print('Введите имя и фамилию ученика')

    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=schoolkid_name)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print(f'Ученика с такими данными не существует')
        return
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников по введенным данным')
        return


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    marks = Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)
    return marks


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    chastisements = Chastisement.objects.filter(schoolkid=schoolkid).delete()
    return chastisements


def create_commendation(schoolkid_name, lesson_name):
    schoolkid = get_schoolkid(schoolkid_name)

    lesson = Lesson.objects.filter(subject__title=lesson_name, group_letter=schoolkid.group_letter,
                                   year_of_study=schoolkid.year_of_study).order_by('?').first()
    if not lesson:
        print('Уроков по введенному предмету не найдено')
        return
    commendation_text = random.choice(COMMENDATION_TEXT)
    commendations = Commendation.objects.create(text=commendation_text, created=lesson.date, schoolkid=schoolkid,
                                                subject=lesson.subject, teacher=lesson.teacher)
    return commendations

