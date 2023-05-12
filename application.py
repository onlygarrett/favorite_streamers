if __name__ == "__main__":
    from src import generate_user_info
    from configparser import ConfigParser
    parser = ConfigParser()
    generate_user_info.generate(parser=parser)