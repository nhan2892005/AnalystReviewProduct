from crawl_Products_data import crawl_Products_data
from crawl_user_and_review import crawl_user_and_review
import sys

def main():
    if len(sys.argv) != 2:
        print("Usage: python run_all_crawl.py [--product | --review]")
        return

    arg = sys.argv[1]
    if arg == "--product":
        crawl_Products_data()
    elif arg == "--review":
        crawl_user_and_review()
    else:
        print("Invalid argument. Use --product or --review")

if __name__ == "__main__":
    main()
