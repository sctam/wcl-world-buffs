import os
from dotenv import load_dotenv, dotenv_values

def main():
    load_dotenv()

    env_vars = dotenv_values(".env")
    print( env_vars )

if __name__ == "__main__":
    main()