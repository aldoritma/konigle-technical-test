from celery import shared_task
from django.core.mail import send_mail
from celery.utils.log import get_task_logger

from unity.models import Subscriber

logger = get_task_logger(__name__)


@shared_task
def report_scheduler():
    seller_emails = ['seller@example.com']
    logger.info("Sending report.......................")
    subscriber = Subscriber()

    # Sending mail to admin
    message = (
        "Total emails: {}\nTotal unsubscribers: {}\nTotal emails this month: {}".format(
            subscriber.total_emails(),
            subscriber.total_unsubscribers(),
            subscriber.total_emails_this_month(),
        )
    )
    logger.info(message)
    send_mail(
        "Report",
        message,
        "from@example.com",
       seller_emails,
        fail_silently=False,
    )

    return f"Sent emails"
