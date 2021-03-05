"""
First use pandas to process the raw data
Then store the cleaned data to the sqlite3 database called england.db
"""
import pandas as pd
import sqlite3
import os
from pathlib import Path
import re
from datetime import date
from fuzzywuzzy import process, fuzz


def main():
    # create_db()
    # # create_teams()
    init_db()
    create_teams()
    creat_all_games()
    # test_read_data()
    standardize_team_names()


def creat_all_games():
    years = range(2013, 2020)
    seasons = [f"{year}-{year-2000+1}" for year in years]
    suffices = ["", "-i", "-ii"]
    for season in seasons:
        for suffix in suffices:
            create_games(season, suffix=suffix)


def init_db():
    conn = sqlite3.connect("england.db")
    with conn:
        c = conn.cursor()
        tables = ["teams", "games"]
        for table in tables:
            sql = f"DROP TABLE IF EXISTS {table}"
            c.execute(sql)
        conn.commit()
    return 0


def parse_game_result(line):
    # line = "  FC Liverpool            4-1 Norwich City"
    # find the score line
    pattern = re.compile(r"\d+-\d+")
    matches = re.search(pattern, line)
    result = None
    if matches != None:
        score = matches.group(0)
        home_score = score.split("-")[0]
        away_score = score.split("-")[1]

        # find the home team & away team
        teams = line.split(score)
        home_team = teams[0].strip()
        away_team = teams[1].strip()

        result = {}
        result.update(
            {
                "home_team": home_team,
                "home_score": home_score,
                "away_team": away_team,
                "away_score": away_score,
            }
        )

    return result


def create_db():
    conn = sqlite3.connect("england.db")
    print(str(conn))
    return 0


def create_teams():
    data_folder = Path("dataset_PL/clubs")
    csv_file = data_folder / "clubs.props.txt"
    df = pd.read_csv(csv_file, comment="#", skipinitialspace=True)
    conn = sqlite3.connect("england.db")
    df.to_sql("teams", conn, if_exists="replace")
    return 0


def create_games(season, suffix=""):
    data_folder = Path(f"dataset_PL/{season}")
    game_file = data_folder / f"1-premierleague{suffix}.txt"

    if not os.path.isfile(game_file):
        return 0

    print(f"creating games for season {season}{suffix}...")

    df_games = pd.DataFrame(
        columns=["season", "home_team", "home_score", "away_team", "away_score",]
    )
    try:
        with open(game_file) as f:
            for line in f:
                result = parse_game_result(line)
                if result != None:
                    df_games = df_games.append(
                        {**{"season": season}, **result,}, ignore_index=True,
                    )
    except Exception as e:
        print(f"{e}: No records were added.")
    else:
        conn = sqlite3.connect("england.db")
        df_games.to_sql("games", conn, if_exists="append")

    finally:
        return 0


def standardize_names(names, standard):
    new_names = [process.extractOne(name, standard)[0] for name in names]
    return new_names


def test_read_data():
    conn = sqlite3.connect("england.db")
    with conn:
        c = conn.cursor()
        # sql = "select * from games where home_team =: team or away_team =: team"
        c.execute(
            "select * from games where home_team like :team or away_team like :team",
            {"team": "%Liverpool%"},
        )
        df = pd.read_sql_query(
            "select * from games where home_team like :team or away_team like :team",
            conn,
            params={"team": "%Liverpool%"},
        )

        # df_full = pd.read_sql_query("select * from games", conn)
        c.execute("select season, count(*) from games group by season")
        # print(c.fetchall())
        # print(df.shape)
        print(df)

        c.execute(
            "select distinct season, home_team from games where home_team not in (select name from teams)"
        )
        print(c.fetchall())


def standardize_team_names():
    conn = sqlite3.connect("england.db")
    with conn:
        df_games = pd.read_sql("select * from games", conn, index_col="index")
        df_teams = pd.read_sql("select * from teams", conn, index_col="index")

        df_games.home_team = df_games.home_team.apply(
            lambda x: process.extractOne(x, df_teams["Name"])[0]
        )

        df_games.away_team = df_games.away_team.apply(
            lambda x: process.extractOne(x, df_teams["Name"])[0]
        )
        # print(df_games.shape)
        # print(df_games)
        df_games.to_sql("games", conn, if_exists="replace")


if __name__ == "__main__":
    main()

