from django.core.mail.backends.smtp import EmailBackend
from django.conf import settings


class UnicodeEmailBackend(EmailBackend):
    def send_messages(self, email_messages):

        try:
            # Преобразуем все текстовые данные в Unicode
            for message in email_messages:
                message.subject = str(message.subject)
                message.body = str(message.body)
                if hasattr(message, 'alternatives'):
                    message.alternatives = [
                        (str(content), mimetype)
                        for content, mimetype in message.alternatives
                    ]

            return super().send_messages(email_messages)
        except Exception as e:
            if settings.DEBUG:
                print(f"Email sending error: {str(e)}")
            raise