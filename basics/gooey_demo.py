"""
Creating a sample application GUI
"""

from gooey import Gooey, GooeyParser
import time

# from message import display_message


@Gooey(dump_build_config=True, program_name="Asset Liability Projection System")
def main():
    desc = "sample projection system graphic interface"
    file_help_msg = "Specify your input directory"

    my_cool_parser = GooeyParser(description=desc)

    my_cool_parser.add_argument(
        "Asset inforce file", help=file_help_msg, widget="FileChooser"
    )
    my_cool_parser.add_argument(
        "Liability inforce file", help=file_help_msg, widget="FileChooser"
    )
    my_cool_parser.add_argument(
        "Assumption directory", help=file_help_msg, widget="DirChooser"
    )
    my_cool_parser.add_argument(
        "Output directory", help=file_help_msg, widget="FileSaver"
    )
    my_cool_parser.add_argument(
        "Scenario files", nargs="*", help=file_help_msg, widget="MultiFileChooser"
    )
    my_cool_parser.add_argument("Log directory", help="Directory to store running log")

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
    time.sleep(2)
    print(f"Asset inforce file: {getattr(args,'Asset inforce file')}")
    print(f"Liability inforce file: {getattr(args,'Liability inforce file')}")


def here_is_more():
    pass


if __name__ == "__main__":
    main()
