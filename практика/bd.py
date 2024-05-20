import csv
import sqlite3
import telebot

con = sqlite3.connect('Veterinar.bd')
cur = con.cursor()
cur.execute('''
            create table if not exists doctor(
            id integer primary key autoincrement,
            family text,
            name text,
            dolzhnost text,
            stage integer
            )
            ''')
cur.execute('''
            create table if not exists animals(
            id integer primary key autoincrement,
            name text,
            age int,
            anim text )
            ''')
cur.execute('''
            create table if not exists diagnoz(
            id integer primary key autoincrement,
            title text,
            description text )
            ''')
cur.execute('''
            create table if not exists visits(
            id integer primary key autoincrement,
            idAnim integer references animals(id),
            idDoc integer references doctor(id),
            idDiagnoz integer references diagnoz(id),
            dateVisit text)
            ''')
bot = telebot.TeleBot('7185672784:AAFzqUk6RJLBZwFXpQUOLta4qbkCIWDt7-U')
@bot.message_handler(content_types=['text'])
def fillTables(message):
    if message.text == '/start':
        bot.send_message(message.from_user.id,'Выберите таблицу:\nдоктор 1\nживотное 2\nдиагноз 3\nпосещения 4')
        bot.register_next_step_handler(message,fillAnoterTable)

# выбор таблицы

def fillAnoterTable(message):
    global tables
    tables = message.text
    if tables == '1':
        bot.send_message(message.from_user.id,'фамилия доктора')
        bot.register_next_step_handler(message, fillDoctorFamily)
    elif tables == '2':
        bot.send_message(message.from_user.id,'кличка животного')
        bot.register_next_step_handler(message, fillAnimalName)
    elif tables == '3':
        bot.send_message(message.from_user.id,'название диагноза')
        bot.register_next_step_handler(message, fillDiagnozTitle)
    elif tables == '4':
        bot.send_message(message.from_user.id,'id животного')
        bot.register_next_step_handler(message, fillVisitAnim)
    else:
        bot.send_message(message.from_user.id,'Неверное значение! введите корректное значение')
        bot.register_next_step_handler(message,fillAnoterTable)

# Заполнение доктора

def fillDoctorFamily(message):
    global Docfamily
    Docfamily = message.text
    bot.send_message(message.from_user.id, 'имя доктора')
    bot.register_next_step_handler(message, fillDoctorName)
def fillDoctorName(message):
    global Docname
    Docname = message.text
    bot.send_message(message.from_user.id, 'должность доктора')
    bot.register_next_step_handler(message, fillDoctorDolzhnost)
def fillDoctorDolzhnost(message):
    global Docdolzhnost
    Docdolzhnost = message.text
    bot.send_message(message.from_user.id, 'стаж доктора')
    bot.register_next_step_handler(message, fillDoctorStage)
def fillDoctorStage(message):
    global Docstage
    Docstage = message.text
    con = sqlite3.connect('Veterinar.bd')
    cur = con.cursor()
    cur.execute('INSERT INTO doctor(family, name, dolzhnost, stage) VALUES (?, ?, ?, ?)', (Docfamily, Docname, Docdolzhnost, Docstage))
    con.commit()
    cur.execute('''select * from doctor''')
    print(Docfamily, Docname, Docdolzhnost, Docstage)
    with open("outDoctors.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", lineterminator='\r')
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)
    bot.send_message(message.from_user.id, 'продолжить заполнение 1\n выбрать другую таблицу по номеру')
    if message.text == '1':
        bot.send_message(message.from_user.id,'фамилия доктора')
        bot.register_next_step_handler(message,fillDoctorFamily)
    else:
        bot.register_next_step_handler(message, fillAnoterTable)


# Заполнение животного

def fillAnimalName(message):
    global Animname
    Animname = message.text
    bot.send_message(message.from_user.id, 'возраст животного')
    bot.register_next_step_handler(message, fillAnimalAge)
def fillAnimalAge(message):
    global Animage
    Animage = message.text
    bot.send_message(message.from_user.id, 'вид животного')
    bot.register_next_step_handler(message, fillAnimalType)
def fillAnimalType(message):
    global Amintype
    Amintype = message.text
    con = sqlite3.connect('Veterinar.bd')
    cur = con.cursor()
    cur.execute('INSERT INTO animals(name, age, anim) VALUES (?, ?, ?)',(Animname, Animage, Amintype))
    con.commit()
    cur.execute('''select * from animals''')
    with open("outAnimals.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", lineterminator='\r')
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)
    bot.send_message(message.from_user.id, 'продолжить заполнение 1')
    print(Animname, Animage, Amintype)
    if message.text == '1':
        bot.send_message(message.from_user.id,'кличка животного')
        bot.register_next_step_handler(message,fillAnimalName)
    else:
        bot.register_next_step_handler(message,fillAnoterTable)

# заполнение диагноза

def fillDiagnozTitle(message):
    global title
    title = message.text
    bot.send_message(message.from_user.id, 'описание диагноза')
    bot.register_next_step_handler(message, fillDiagnozdescription)
def fillDiagnozdescription(message):
    global description
    description = message.text
    con = sqlite3.connect('Veterinar.bd')
    cur = con.cursor()
    cur.execute('INSERT INTO diagnoz(title, description) VALUES (?, ?)',(title, description))
    con.commit()
    cur.execute('''select * from diagnoz''')
    with open("outDiagnoz.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", lineterminator='\r')
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)
    bot.send_message(message.from_user.id, 'продолжить заполнение 1\n выбрать другую таблицу по номеру')
    print(title, description)
    if message.text == '1':
        bot.send_message(message.from_user.id,'название диагноза')
        bot.register_next_step_handler(message, fillDiagnozTitle)
    else:
        bot.register_next_step_handler(message,fillAnoterTable)

# заполнение визита

def fillVisitAnim(message):
    global AnimId
    AnimId = message.text
    bot.send_message(message.from_user.id, 'id доктора')
    bot.register_next_step_handler(message, fillVisitDoc)
def fillVisitDoc(message):
    global DocId
    DocId = message.text
    bot.send_message(message.from_user.id, 'id диагноза')
    bot.register_next_step_handler(message, fillVisitDiag)
def fillVisitDiag(message):
    global DiagnozId
    DiagnozId = message.text
    bot.send_message(message.from_user.id, 'дата визита')
    bot.register_next_step_handler(message, fillVisitdate)
def fillVisitdate(message):
    global DateVisit
    DateVisit = message.text
    con = sqlite3.connect('Veterinar.bd')
    cur = con.cursor()
    cur.execute('INSERT INTO visits(idAnim, idDoc, idDiagnoz, dateVisit) VALUES (?, ?, ?, ?)', (AnimId, DocId, DiagnozId, DateVisit))
    con.commit()
    cur.execute('''select * from visits''')
    print(AnimId, DocId, DiagnozId, DateVisit)
    with open("outVisits.csv", 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=",", lineterminator='\r')
        csv_writer.writerow([i[0] for i in cur.description])
        csv_writer.writerows(cur)
    bot.send_message(message.from_user.id, 'продолжить заполнение 1\n выбрать другую таблицу по номеру')
    if message.text == '1':
        bot.send_message(message.from_user.id,'id животного')
        bot.register_next_step_handler(message,fillVisitAnim)
    else:
        bot.register_next_step_handler(message,fillAnoterTable)



bot.polling(none_stop=True)