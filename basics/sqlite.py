import sqlite3

conn = sqlite3.connect("PLBet.db")

# # create a cursor
with conn:
    c = conn.cursor()
    c.execute("select * from INFO_Teams")
    x = c.fetchall()
    # x is a list of tuples
    print(x)
    # first record
    print(x[0])
    # loop all records, unpack the tuple
    resultList = []
    for record in x:
        team_id, team_short_name, team_name, = record
        resultList.append(team_name)
    print(resultList)

# use placeholders
myteam = "Liverpool"
# 1. generic placeholder
# sql = "select Team_id, st_name, lg_name from INFO_Teams where lg_name = '{}' ".format(
#     myteam
# )

# with conn:
#     c = conn.cursor()
#     c.execute(sql)
#     x = c.fetchone()
#     print(x)

# 2. sqlite built-in placeholder, use tuple
with conn:
    c = conn.cursor()
    c.execute(
        """select Team_id, st_name,lg_name 
         FROM info_teams where lg_name = ?""",
        (myteam,),
    )
    x = c.fetchone()
    print(x)


# 3. most-readable placeholders, use dictionary
with conn:
    c = conn.cursor()
    c.execute(
        """select Team_id, st_name, lg_name 
         FROM info_teams where lg_name = :lg_name
         """,
        {"lg_name": myteam},
    )
    x = c.fetchone()
    print(x)
# team_id, team_name_short, team_name_long = x
# print(team_id)
# print(c.fetchmany(1))

# conn.close()
