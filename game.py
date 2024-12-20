import sqlite3
conn = sqlite3.connect('Flash_Card_Game.sqlite')
cursor = conn.cursor()

# getting all data of perticular intrest initial , so we can use it easily
cursor.execute("SELECT * FROM history_questions")
history_data = cursor.fetchall()
cursor.execute("SELECT * FROM sport_questions")
sports_data = cursor.fetchall()
cursor.execute("SELECT * FROM gk_questions")
gk_data = cursor.fetchall()
cursor.execute("SELECT * FROM math_questions")
math_data = cursor.fetchall()
cursor.execute("SELECT * FROM poetry_questions")
poetry_data = cursor.fetchall()


for data in math_data:
    print(data[0],data[1])
    print("Options: ",data[2])
    print("Correct opton: ",data[3])
    print(" ")
    
conn.close()