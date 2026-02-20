import click
from dotenv import load_dotenv

secrets = load_dotenv()


@click.command()
def run():
    pass


if __name__ == "__main__":
    run()
