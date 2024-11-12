from caption_emailing.wrapper import email_on_failure

from settings import TASK_NAME


@email_on_failure(TASK_NAME)
def main():
    print("Hello world.")


if __name__ == "__main__":
    main()
