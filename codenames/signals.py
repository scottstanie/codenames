import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Game


@receiver(post_save, sender=Game)
def notify(sender, **kwargs):
    game = kwargs['instance']
    if game.current_guess_number > 0:
        # Mid turn guessing, don't notify
        return

    users = list(game.all_players())
    url = 'http://codenames.scottstaniewicz.com/game/%s' % game.unique_id

    try:
        server = smtplib.SMTP('smtp.mail.yahoo.com:587')
        username = "axemesumpin@yahoo.com"
        password = os.environ.get('EMAIL_PASSWORD')

        server.starttls()
        server.login(username, password)
    except Exception as e:
        print "Failed to login to smtp: %s" % e
        return

    msg = MIMEMultipart()

    if kwargs['created']:
        # New game, notify all participants
        message = "You joined {} with {}, {}, {}, and {}!".format(url, *users)
        msg.attach(MIMEText(message, 'plain'))
        try:
            email_to = ','.join([u.email for u in users])
            msg["To"] = email_to
            msg["From"] = username
            msg["Subject"] = message
            server.sendmail(username, email_to.split(','), msg.as_string())
        except Exception as e:
            print 'Error sending message to %s: %s' % (email_to, e)

    else:
        email_to = game.current_player().email
        message = "{} with {}, {}, {}, and {} is waiting on you!".format(url, *users)
        try:
            msg.attach(MIMEText(message, 'plain'))
            msg["To"] = email_to
            msg["From"] = username
            msg["Subject"] = message
            server.sendmail(username, [email_to], msg.as_string())
        except Exception as e:
            print "Could not email %s: %s" % (email_to, e)

    try:
        server.quit()
    except Exception as e:
        print "Could not quit server %s" % e
