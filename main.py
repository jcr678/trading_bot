import scrape
import models
import sentiment

def main():
    scrape.scrape()
    scrape.display_information()
    print('Hello, World!')

if __name__ == "__main__":
    main()
