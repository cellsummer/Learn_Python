"""
Creating a sample application GUI
"""

from gooey import Gooey, GooeyParser
import time
import sqlite3
import pandas as pd

# from message import display_message


@Gooey(dump_build_config=True, program_name="Premier League Results Look Up")
def main():
    desc = "look up historical Premier League results"
    conn = sqlite3.connect("england.db")
    with conn:
        c = conn.cursor()
        c.execute("select name from teams")
        teams_tups = c.fetchall()
        teams = [team_tup[0] for team_tup in teams_tups]

        c.execute("select distinct season from games")
        seasons_tups = c.fetchall()
        seasons = [seasons_tup[0] for seasons_tup in seasons_tups]

    # print(teams)

    my_cool_parser = GooeyParser(description=desc)

    my_cool_parser.add_argument(
        "team",
        metavar="Choose your team",
        help="Choose the team you want to look up the results",
        choices=teams,
        default=teams[0],
    )

    my_cool_parser.add_argument(
        "--season",
        metavar="Choose your season",
        help="Choose the season you want to look up the results",
        choices=seasons + ["All seasons"],
        default="All seasons",
    )

    my_cool_parser.add_argument(
        "--opponent",
        metavar="Choose your opponent",
        help="Choose the opponent you want to look up the results",
        choices=teams + ["All teams"],
        default="All teams",
    )
    # my_cool_parser.add_argument(
    #     "Liability inforce file", help=file_help_msg, widget="FileChooser"
    # )
    # my_cool_parser.add_argument(
    #     "Assumption directory", help=file_help_msg, widget="DirChooser"
    # )
    # my_cool_parser.add_argument(
    #     "Output directory", help=file_help_msg, widget="FileSaver"
    # )
    # my_cool_parser.add_argument(
    #     "Scenario files", nargs="*", help=file_help_msg, widget="MultiFileChooser"
    # )
    # my_cool_parser.add_argument("Log directory", help="Directory to store running log")

    # my_cool_parser.add_argument(
    #     "-d",
    #     "--duration",
    #     default=2,
    #     type=int,
    #     help="Duration (in seconds) of the program output",
    # )
    # my_cool_parser.add_argument(
    #     "-s",
    #     "--cron-schedule",
    #     type=int,
    #     help="datetime when the cron should begin",
    #     widget="DateChooser",
    # )
    # my_cool_parser.add_argument(
    #     "--cron-time", help="datetime when the cron should begin", widget="TimeChooser"
    # )
    # my_cool_parser.add_argument(
    #     "-c", "--showtime", action="store_true", help="display the countdown timer"
    # )
    # my_cool_parser.add_argument(
    #     "-p", "--pause", action="store_true", help="Pause execution"
    # )
    # my_cool_parser.add_argument("-v", "--verbose", action="count")
    # my_cool_parser.add_argument(
    #     "-o",
    #     "--overwrite",
    #     action="store_true",
    #     help="Overwrite output file (if present)",
    # )
    # my_cool_parser.add_argument(
    #     "-r", "--recursive", choices=["yes", "no"], help="Recurse into subfolders"
    # )
    # my_cool_parser.add_argument(
    #     "-w", "--writelog", default="writelogs", help="Dump output to local file"
    # )
    # my_cool_parser.add_argument(
    #     "-e", "--error", action="store_true", help="Stop process on error (default: No)"
    # )
    # verbosity = my_cool_parser.add_mutually_exclusive_group()
    # verbosity.add_argument(
    #     "-t",
    #     "--verbozze",
    #     dest="verbose",
    #     action="store_true",
    #     help="Show more details",
    # )
    # verbosity.add_argument(
    #     "-q", "--quiet", dest="quiet", action="store_true", help="Only output on error"
    # )

    args = my_cool_parser.parse_args()

    for index, row in get_results(args.team, args.opponent, args.season).iterrows():
        # (season, home_team, home_score, away_score, away_team) = result
        print(
            f"{row.season}: {row.home_team}  {row.home_score} - {row.away_score}  {row.away_team}"
        )


def get_results(team, opponent, season):
    conn = sqlite3.connect("england.db")
    filter_opponent = True
    filter_season = True

    if opponent == "All teams":
        filter_opponent = False

    if season == "All seasons":
        filter_season = False

    with conn:
        df_results = pd.read_sql_query("select * from games", conn)

        filterred_results = df_results[
            (df_results["home_team"] == team) | (df_results["away_team"] == team)
        ]

        if filter_opponent:
            filterred_results = filterred_results[
                (filterred_results["home_team"] == opponent)
                | (filterred_results["away_team"] == opponent)
            ]

        if filter_season:
            filterred_results = filterred_results[filterred_results["season"] == season]

    return filterred_results


if __name__ == "__main__":
    main()
    # print(get_results("Liverpool FC", "All teams", "All seasons"))
    # print(get_results("Liverpool FC", "Chelsea FC", "All seasons"))
