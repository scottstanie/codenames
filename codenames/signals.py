import os
import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from django.core.mail import send_mail
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Game


@receiver(post_save, sender=Game)
def notify(sender, **kwargs):
    game = kwargs['instance']


#     if game.current_guess_number > 0:
#         # Mid turn guessing, don't notify
#         return
#
#     users = list(game.all_players())
#     if os.environ.get("DEBUG"):
#         base_url = "localhost:8000/game/"
#     else:
#         base_url = "https://codenames.scottstaniewicz.com/game/"
#     url = base_url + game.unique_id
#
#     if kwargs['created']:
#         # New game, notify all participants
#         subject = "You joined {} with {}, {}, {}, and {}!".format(game.unique_id, *users)
#         email_to = [u.email for u in users]
#     else:
#         email_to = game.current_player().email
#         subject = "{} with {}, {}, {}, and {} is waiting on you!".format(url, *users)
#
#     message = Mail(
#         from_email="codenames@scottstaniewicz.com",
#         to_emails=email_to,
#         subject=subject,
#         html_content='<strong> Start playing! </strong>',
#     )
#     try:
#         sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
#         response = sg.send(message)
#         print(response.status_code)
#         print(response.body)
#         print(response.headers)
#     except Exception as e:
#         print(e.message)