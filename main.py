import csv
import random
import smtplib, ssl
from email.message import EmailMessage
import yaml


def main():
    # read config
    with open("config.yaml", "r") as stream:
        config = yaml.load(stream, Loader=yaml.FullLoader)

    # read in name csv
    with open("names.csv") as csvfile:
        name_list = read_csv(csvfile)

    # sanitycheck names
    if not sanity_check_names(name_list):
        raise IOError("Input not correct. Look in Readme how it should look like.")

    # random pick letter
    random_letter = get_random_letter()

    # shuffle names
    random.shuffle(name_list)

    # create pairs of names
    # swap names and adresses per pair
    # example:
    # peter | petersmail
    # paul | paulsmail
    # -------->
    # peter | paulsmail
    # paul | petersmail
    new_pairs = []
    for idx in range(0, len(name_list), 2):
        new_pairs.append([name_list[idx][0], name_list[idx+1][1]])
        new_pairs.append([name_list[idx+1][0], name_list[idx][1]])

    # send email to names
    sender_email = input("Type your email adress and press enter: ")
    password = input("Type your email password and press enter: ")

    for pair in new_pairs:
        send_name_to_mailadress(pair[1], pair[0], random_letter, config["mail"]["ssl_port"],
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

    if len(name_list) % 2 != 0:
        return False
    return True


def get_random_letter() -> str:
    alphabet = "ABCDEFGHIJKLNOPQRSTUVWXYZ"
    enum = random.randint(0, len(alphabet) - 1)
    random_pick = alphabet[enum]
    print(f"THE RANDOM LETTER IS -- {random_pick} --!")

    return random_pick


def send_name_to_mailadress(mail_adress, name, random_letter, ssl_port, smpt_server, sender_email, password) -> None:
    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(smpt_server, ssl_port, context=context) as server:
        sender_email = sender_email
        receiver_email = mail_adress

        msg = EmailMessage()
        msg.set_content(f"Wichtelgeschenk: Zufallsbuchstabe ----> {random_letter} \n\n "
                        f"Du schenkst dieses Jahr -->>{name}<<-- ein tolles Geschenk, das mit dem Buchstaben -->> {random_letter} <<-- beginnt.\n\n"
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
