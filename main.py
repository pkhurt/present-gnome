import csv
import random
import smtplib, ssl
from email.message import EmailMessage
import yaml


def main():
    # read config
    with open("config.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    # read in name csv from config
    with open(config["names"]["names_file"]) as csvfile:
        name_list = read_csv(csvfile)

    # sanitycheck names
    if not sanity_check_names(name_list):
        raise IOError("Input not correct. Look in Readme how it should look like.")

    # random pick letter
    random_letter = get_random_letter()

    # shuffle names
    random.shuffle(name_list)

    # append list by first entry
    name_list.append(name_list[0])

    # sender host mail information
    sender_email = input("Type your email adress and press enter: ")
    password = input("Type your email password and press enter: ")
    
    # loop through list and follow rule: always the current iterator must give present to the next one
    for idx, name in enumerate(name_list[:-1]):
        # print(f"{name[1]} has to give {name_list[idx+1][0]} a present with the letter {random_letter}." )
        send_name_to_mailadress(name[1], name_list[idx+1][0], random_letter, config["mail"]["ssl_port"],
                                config["mail"]["smtp_server"], sender_email, password)

def read_csv(csvfile) -> list:
    """
    :param csvfile: opened csv-file
    :return: 2D list
    """
    namereader = csv.reader(csvfile, delimiter=',')
    name_list = []
    for row in namereader:
        name_list.append(row)

    return name_list


def sanity_check_names(name_list) -> bool:
    if len(name_list) == 0:
        return False

    return True


def get_random_letter() -> str:
    alphabet = "ABCDEFGHIJKLNOPQRSTUVWXYZ"
    enum = random.randint(0, len(alphabet) - 1)
    random_pick = alphabet[enum]
    print(f"THE RANDOM LETTER IS -- {random_pick} --!")

    return random_pick


def send_name_to_mailadress(mail_adress: str, name: str, random_letter: str, ssl_port: int, smpt_server: str, sender_email: str, password: str) -> None:
    """
    :param mail_adress: Receiver email adress
    :param name: Name that gets the gift from the receiver mail adress
    :param random_letter: The gift has to start with this letter
    """
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smpt_server, ssl_port, context=context) as server:
        sender_email = sender_email
        receiver_email = mail_adress

        msg = EmailMessage()
        msg.set_content(f"Wichtelgeschenk: \n\n "
                        f"Du schenkst dieses Jahr -->>{name}<<-- ein tolles Geschenk, das mit einem beliebigen Buchstaben beginnt.\n\n"
                        f"Es wird noch eine WhatsApp Gruppe erstellt, in dem du deinen Wunsch / Ideen äußern kannst."
                        f"Viele Grüße,\n"
                        f"Der Weihnachtsmann")
        msg["Subject"] = "Wichtelgeschenk"
        msg["From"] = f"{sender_email}"
        msg["To"] = f"{receiver_email}"

        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()


if __name__ == '__main__':
    main()
