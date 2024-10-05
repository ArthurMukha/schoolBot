from aiogram import Bot, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.input_media import InputMedia

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy import or_, and_
from reate_db import Base, User, Team

import asyncio, time

engine = create_engine('sqlite:///database.db')
Base.metadata.create_all(engine)

# database = SQLAlchemy(app)
Session = sessionmaker(bind=engine)
session = Session()

TOKEN = "7673059163:AAF_-Sie6EyAb0pylUs4KPTllXwnIm3Frhk"
status = "start"
is_solved = [0] * 10

admins = []

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


def get_team(user_id):
    with session as new_session:
        # print(new_session.query(User).all())
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        # print(user)
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
        # print(team)

        return team.to_json()
def change_status(user_id, status):
    with session as new_session:

        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
        team.status = status
        new_session.commit()
def change_ex_num(user_id, ex_num):
    with session as new_session:

        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
        team.ex_num = ex_num
        new_session.commit()


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    global status
    if status != 'start':
        await bot.send_message(message.from_user.id, "Ты уже зарегестрировал команду")
        return
    # print(message.from_user.id)

    hello_message = "Hello, world! Если ты это читаешь, у тебя сейчас самый лучший урок информатики в твоей жизни.\
 Радуйтесь, такое раз в жизни бывает! А подкидывать вам смешные задачки и проверять ответы сегодня будет этот бот\
 от самых лучших восхитительных прекрасных гениальных 1.5 программистов. Если вам будет что сказать учителям по\
 окончании урока, благодарности и восхищения все писать Артуру:\n@Nob0dy7\nпожелания и предложения Ирине:\n@rena_gm\nпретензии и обвинения Вадиму:\n@V_Rand"

    await bot.send_message(message.from_user.id, hello_message)

    team_name_message = "Чтож, начнём. Для начала соревнования зарегистрируйте свою команду. Напишите название своей команды"

    await asyncio.sleep(1)
    await bot.send_message(message.from_user.id, team_name_message)

    team_name = f"{message.from_user.id}"

    newUser = User(
        user_id=message.from_user.id,
        teamName=team_name
    )
    newTeam = Team(
        teamName=team_name,
        score=0,
        lastPointTime=0,
        compound={},
        status="team_name",
        ex_num=1, ex_1=False, ex_2=False,ex_3=False,ex_4=False, ex_5=False, ex_6=False
    )
    print(newTeam.to_json())
    with session as new_session:
        new_session.add(newUser)
        new_session.add(newTeam)
        new_session.commit()
        # print(new_session.query(User).all())
        print(new_session.query(Team).all())

@dp.message_handler(lambda message: get_team(message.from_user.id)["status"] == "team_name")
async def reg_team(message: types.Message):
    # leaderboard.append({'teamName' : message.text, "score" : 0}, ignore_index=True)

    user_id = message.from_user.id
    with session as new_session:
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
        team.status = "compound"
        team.teamName = message.text
        user.teamName = message.text
        # print(team.to_json())
        new_session.commit()

    user_id = message.from_user.id
    await bot.send_message(
        user_id,
        "Напишите <b>состав вашей команды</b> в формате:\n\nКостина Ирина\nЗапевалов Вадим\nLanus Елизавета\n\n\n"
        "<b>Подсказка: чтобы сделать перенос строки в телеграмена компьютере зажмите Ctrl и нажмите Enter</b>",
        parse_mode="html"
    )


@dp.message_handler(lambda message: get_team(message.from_user.id)["status"] == "compound")
async def compound_team(message: types.Message):
    team_compound = message.text.split("\n")
    # print(team)

    user_id = message.from_user.id
    with session as new_session:
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
        team.compound = {str(comp) : comp for comp in team_compound}
        team.status = "password"
        print(team.to_json())
        new_session.commit()

    print(session.query(Team).all()); print()

    await bot.send_message(message.from_user.id, "Введите пароль")

@dp.message_handler(lambda message: get_team(message.from_user.id)["status"] == "password")
async def exercise_password(message: types.Message):
    nombers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october',
              'november', 'december']

    def romanToInt(s):
        translations = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000
        }
        number = 0
        s = s.replace("IV", "IIII").replace("IX", "VIIII")
        s = s.replace("XL", "XXXX").replace("XC", "LXXXX")
        s = s.replace("CD", "CCCC").replace("CM", "DCCCC")
        for char in s:
            if char in translations:
                number += translations[char]
        return number

    password = message.text
    if len(password) < 7:
        await bot.send_message(message.from_user.id, "Ваш пароль слишком короткий")
    else:
        summ = 0
        for i in range(10):
            g = password.count(nombers[i])
            summ += int(nombers[i]) * g
        if summ % 23 != 0 and summ > 0:
            await bot.send_message(message.from_user.id, "Сумма цифр в вашем пароле должна делиться на 23")
        else:
            fl = 0
            for k in range(12):
                if months[k] in password:
                    fl = 1
            if fl != 1:
                await bot.send_message(message.from_user.id,
                                       "В вашем пароле должно быть название месяца на английском строчными буквами")
            else:
                if romanToInt(password) != 114:
                    await bot.send_message(message.from_user.id,
                                           "В вашем пароле должны содержаться римские цифры, сумма которых равна 114")
                else:
                    if 'KELL' not in password:
                        await bot.send_message(message.from_user.id,
                                               "В вашем пароле должна быть аббревиатура лицея заглавными буквами на английском языке")
                    else:
                        await bot.send_message(message.from_user.id, "Норм пароль лол")

                        global status
                        status = "exes"  # меняю статус, чтобы код понимал, чем должен заниматься

                        global keyboard
                        keyboard = types.ReplyKeyboardMarkup(
                            resize_keyboard=True,
                            input_field_placeholder="Выберите задачу для решения"
                        )
                        keyboard.row(
                            types.KeyboardButton(text="Задача 2"),
                            types.KeyboardButton(text="Задача 3"),
                            types.KeyboardButton(text="Задача 4")
                        )
                        keyboard.row(
                            types.KeyboardButton(text="Задача 5"),
                            types.KeyboardButton(text="Задача 6")
                        )
                        keyboard.add(KeyboardButton(text="Вывести лидерборд"))

                        await message.answer("Выберите задачу для решения", reply_markup=keyboard)

                        user_id = message.from_user.id
                        with session as new_session:
                            user = new_session.query(User).filter_by(user_id=user_id).all()[0]
                            user_team = user.teamName

                            team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
                            if not team.ex_1:
                                team.ex_1 = True
                                team.status = "ex"
                                team.score += 1
                                team.lastPointTime = int(time.time())
                            new_session.commit()

@dp.message_handler(lambda message : message.text=="Вывести лидерборд")
async def print_leaderboard(message: types.Message):
    leaders = []
    with session as new_session:
        teams = [obj.to_json() for obj in new_session.query(Team).all()]
    for team in teams:
        leaders.append((team['score'], team['lastPointTime'], team['teamName']))
    leaders.sort()
    leaders_string = "<b>Текущий лидерборд:</b>\n\n"
    for team_idx in range(min(5, len(leaders))):
        # if leaders[team_idx][2] == 'admins':
        #     continue
        leaders_string += f"<b>{team_idx + 1} место.</b> {leaders[team_idx][2]} {leaders[team_idx][0]} points"


    await bot.send_message(
        message.from_user.id,
        leaders_string,
        parse_mode="html"
    )


@dp.message_handler(lambda message : message.text.split()[0] == 'Задача' and len(message.text.split()) > 1)
async def change_ex(message: types.Message):
    num = int(message.text.split()[-1])
    if 2 <= num <= 7:
        global exercise_number
        exercise_number = num
        change_ex_num(message.from_user.id, exercise_number)
        print("ex number changed")

        id_ = message.from_user.id

        if num == 2:
            await bot.send_message(
                id_,
                "<b>2. Не знакомлюсь</b>\n\nПс, по секрету, каждый из сегодняшних учителей информатики написал о себе в нашей любимой соц сети пару символов... Слабо расшифровать послание (в порядке ВАИ)?",
                parse_mode="html"
            )
        elif num == 3:
            photo = InputFile(r'C:\Users\artur\PycharmProjects\tgBots\картинка для робота.JPG')

            await bot.send_photo(
                chat_id=id_,
                photo=photo,
                caption="<b>3. Ты точно не робот?</b>\n\nЕвгений Александрович всё видит...\n*картинка на задачу робот с пешеходными переходами. если найдём другую, надо поменять описание",
                parse_mode="html"
            )
        elif num == 4:
            await bot.send_message(
                id_,
                "<b>4. Японская клава</b>\n\nДа уж, купил называется японскую клавую... Как теперь сдавать дз по английскому?",
                parse_mode="html"
            )
        elif num == 5:
            await bot.send_message(
                id_,
                "<b>5. 105.5</b>\n\nМне тут бабушка звонила, рассказывала, что по радио передавали, что в Выборге появились страшные преступники. Как будто случайно проливают кофе на глупых программистов, просила быть осторожнее... Не знаешь, что за глупость она слушает?",
                parse_mode="html"
            )
        elif num == 6:
            await bot.send_message(
                id_,
                "<b>6. Во всём виноват Хилл</b>\n\nКу, бро, недавно что-то бот начал шалить, вместо задачи выдаёт шифр. Я долго ломал голову над тем, что с этим делать, весь стол завалил черновиками на которых пытался расшифровать это. Весь стол! Большой, из 305! Представляешь?! Но потом я уронил ручку, а когда ее поднимал из-под, стола меня осенило! Во всём виноват Хилл!",
                parse_mode="html"
            )

answers = {
    2 : "fst",
    3 : "snd",
    4 : "trd",
    5 : "penis",
    6 : "aga",

}

def get_place(user_id):
    pass

@dp.message_handler(lambda message : get_team(message.from_user.id)["ex_num"] == 2)
async def exercise_2(message: types.Message):
    answer = message.text

    user_id = message.from_user.id
    with session as new_session:
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]


    if answer == answers[team.ex_num]:
        # Увеличили score команды

        if not team.ex_2:
            team.ex_2 = True
            team.lastPointTime = int(time.time())
            team.score += 1
        new_session.commit()

        leaders = []
        teams = [obj.to_json() for obj in new_session.query(Team).all()]
        for team_ in teams:
            leaders.append((team_['score'], team_['lastPointTime'], team_['teamName']))
        leaders.sort()
        for place_, team_ in enumerate(leaders):
            if team_[2] == team.teamName:
                place = place_ + 1
                break
        await bot.send_message(
            message.from_user.id,
            f"Молодцы! Это правильный ответ\nВы решили {exercise_number} задачу\nВы находитесь на {place} месте в рейтинге")
    else:
        await bot.send_message(
            message.from_user.id,
            f"2 задача. Ваш ответ <b>{message.text}</b> не является верным",
            parse_mode="html")

@dp.message_handler(lambda message : get_team(message.from_user.id)["ex_num"] == 3)
async def exercise_3(message: types.Message):
    answer = message.text

    user_id = message.from_user.id
    with session as new_session:
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]

    if answer == answers[team.ex_num]:
        # Увеличили score команды

        if not team.ex_2:
            team.ex_2 = True
            team.lastPointTime = int(time.time())
            team.score += 1
        new_session.commit()

        leaders = []
        teams = [obj.to_json() for obj in new_session.query(Team).all()]
        for team_ in teams:
            leaders.append((team_['score'], team_['lastPointTime'], team_['teamName']))
        leaders.sort()
        for place_, team_ in enumerate(leaders):
            if team_[2] == team.teamName:
                place = place_ + 1
                break
        await bot.send_message(
            message.from_user.id,
            f"Молодцы! Это правильный ответ\nВы решили {exercise_number} задачу\nВы находитесь на {place} месте в рейтинге")
        user_id = message.from_user.id
        with session as new_session:
            user = new_session.query(User).filter_by(user_id=user_id).all()[0]
            user_team = user.teamName

            team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
            if not team.ex_3:
                team.ex_3 = True
                team.lastPointTime = int(time.time())
                team.score += 1
            new_session.commit()
    else:
        await bot.send_message(
            message.from_user.id,
            f"3 задача. Ваш ответ <b>{message.text}</b> не является верным",
            parse_mode="html")

@dp.message_handler(lambda message : get_team(message.from_user.id)["ex_num"] == 4)
async def exercise_4(message: types.Message):
    answer = message.text

    user_id = message.from_user.id
    with session as new_session:
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]

    if answer == answers[team.ex_num]:
        # Увеличили score команды

        if not team.ex_2:
            team.ex_2 = True
            team.lastPointTime = int(time.time())
            team.score += 1
        new_session.commit()

        leaders = []
        teams = [obj.to_json() for obj in new_session.query(Team).all()]
        for team_ in teams:
            leaders.append((team_['score'], team_['lastPointTime'], team_['teamName']))
        leaders.sort()
        for place_, team_ in enumerate(leaders):
            if team_[2] == team.teamName:
                place = place_ + 1
                break
        await bot.send_message(
            message.from_user.id,
            f"Молодцы! Это правильный ответ\nВы решили {exercise_number} задачу\nВы находитесь на {place} месте в рейтинге")
        user_id = message.from_user.id
        with session as new_session:
            user = new_session.query(User).filter_by(user_id=user_id).all()[0]
            user_team = user.teamName

            team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
            if not team.ex_4:
                team.ex_4 = True
                team.lastPointTime = int(time.time())
                team.score += 1
            new_session.commit()
    else:
        await bot.send_message(
            message.from_user.id,
            f"4 задача. Ваш ответ <b>{message.text}</b> не является верным",
            parse_mode="html")

@dp.message_handler(lambda message : get_team(message.from_user.id)["ex_num"] == 5)
async def hardEx_1(message: types.Message):
    answer = message.text

    user_id = message.from_user.id
    with session as new_session:
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]

    if answer == answers[team.ex_num]:
        # Увеличили score команды

        if not team.ex_2:
            team.ex_2 = True
            team.lastPointTime = int(time.time())
            team.score += 1
        new_session.commit()

        leaders = []
        teams = [obj.to_json() for obj in new_session.query(Team).all()]
        for team_ in teams:
            leaders.append((team_['score'], team_['lastPointTime'], team_['teamName']))
        leaders.sort()
        for place_, team_ in enumerate(leaders):
            if team_[2] == team.teamName:
                place = place_ + 1
                break
        await bot.send_message(
            message.from_user.id,
            f"Молодцы! Это правильный ответ\nВы решили {exercise_number} задачу\nВы находитесь на {place} месте в рейтинге")
        user_id = message.from_user.id
        with session as new_session:
            user = new_session.query(User).filter_by(user_id=user_id).all()[0]
            user_team = user.teamName

            team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
            if not team.ex_5:
                team.ex_5 = True
                team.lastPointTime = int(time.time())
                team.score += 3
            new_session.commit()
    else:
        await bot.send_message(
            message.from_user.id,
            f"5 задача. Ваш ответ <b>{message.text}</b> не является верным",
            parse_mode="html")

@dp.message_handler(lambda message : get_team(message.from_user.id)["ex_num"] == 6)
async def hardEx_2(message: types.Message):
    answer = message.text

    user_id = message.from_user.id
    with session as new_session:
        user = new_session.query(User).filter_by(user_id=user_id).all()[0]
        user_team = user.teamName

        team = new_session.query(Team).filter_by(teamName=user_team).all()[0]

    if answer == answers[team.ex_num]:
        # Увеличили score команды

        if not team.ex_2:
            team.ex_2 = True
            team.lastPointTime = int(time.time())
            team.score += 1
        new_session.commit()

        leaders = []
        teams = [obj.to_json() for obj in new_session.query(Team).all()]
        for team_ in teams:
            leaders.append((team_['score'], team_['lastPointTime'], team_['teamName']))
        leaders.sort()
        for place_, team_ in enumerate(leaders):
            if team_[2] == team.teamName:
                place = place_ + 1
                break
        await bot.send_message(
            message.from_user.id,
            f"Молодцы! Это правильный ответ\nВы решили {exercise_number} задачу\nВы находитесь на {place} месте в рейтинге")

        user_id = message.from_user.id
        with session as new_session:
            user = new_session.query(User).filter_by(user_id=user_id).all()[0]
            user_team = user.teamName

            team = new_session.query(Team).filter_by(teamName=user_team).all()[0]
            if not team.ex_6:
                team.ex_6 = True
                team.lastPointTime = int(time.time())
                team.score += 3
            new_session.commit()
    else:
        await bot.send_message(
            message.from_user.id,
            f"6 задача. Ваш ответ <b>{message.text} не является верным</b>",
            parse_mode="html")



if __name__ == '__main__':
    executor.start_polling(dp)
