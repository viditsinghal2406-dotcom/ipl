import sqlite3

conn = sqlite3.connect("players.db")
cursor = conn.cursor()

# DROP OLD TABLES
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS players")
cursor.execute("DROP TABLE IF EXISTS bids")


# USERS TABLE (IPL TEAMS WITH WALLET)
cursor.execute("""
CREATE TABLE users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT,
wallet INTEGER
)
""")

teams = [

("Mumbai Indians","mi123",100000000),
("Chennai Super Kings","csk123",100000000),
("Royal Challengers Bangalore","rcb123",100000000),
("Kolkata Knight Riders","kkr123",100000000),
("Delhi Capitals","dc123",100000000),
("Rajasthan Royals","rr123",100000000),
("Punjab Kings","pbks123",100000000),
("Sunrisers Hyderabad","srh123",100000000),
("Lucknow Super Giants","lsg123",100000000),
("Gujarat Titans","gt123",100000000)

]

cursor.executemany(
"INSERT INTO users(username,password,wallet) VALUES(?,?,?)",
teams
)


# PLAYERS TABLE
cursor.execute("""
CREATE TABLE players(
id INTEGER PRIMARY KEY,
name TEXT,
country TEXT,
role TEXT,
team TEXT,
runs INTEGER,
strike_rate REAL,
wickets INTEGER,
matches INTEGER,
current_price INTEGER
)
""")


players = [

(1,"Virat Kohli","India","Batsman","RCB",7263,134.4,4,237,20000000),
(2,"Rohit Sharma","India","Batsman","MI",6211,131.1,15,243,18000000),
(3,"MS Dhoni","India","Wicketkeeper","CSK",5082,135.9,0,250,12000000),
(4,"KL Rahul","India","Batsman","LSG",4163,134.6,0,118,17000000),
(5,"Hardik Pandya","India","All-rounder","GT",2309,145.0,53,123,18000000),

(6,"Jos Buttler","England","Wicketkeeper","RR",3223,144.8,0,96,20000000),
(7,"Ben Stokes","England","All-rounder","CSK",920,134.0,28,45,15000000),

(8,"David Warner","Australia","Batsman","DC",6397,139.7,0,176,15000000),
(9,"Glenn Maxwell","Australia","All-rounder","RCB",2719,156.7,31,124,14000000),

(10,"Kane Williamson","New Zealand","Batsman","GT",2101,126.0,0,77,12000000),
(11,"Trent Boult","New Zealand","Bowler","RR",120,90.0,105,88,14000000),

(12,"Rashid Khan","Afghanistan","Bowler","GT",443,160.0,139,109,18000000),

(13,"Faf du Plessis","South Africa","Batsman","RCB",4133,133.5,0,130,15000000),
(14,"Kagiso Rabada","South Africa","Bowler","PBKS",170,100.0,106,69,15000000),

(15,"Andre Russell","West Indies","All-rounder","KKR",2262,174.0,96,112,16000000)

]

cursor.executemany(
"INSERT INTO players VALUES (?,?,?,?,?,?,?,?,?,?)",
players
)


# BIDS TABLE
cursor.execute("""
CREATE TABLE bids(
id INTEGER PRIMARY KEY AUTOINCREMENT,
player_id INTEGER,
user_id INTEGER,
bid_amount INTEGER,
bid_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")


conn.commit()
conn.close()

print("Database created successfully!")
