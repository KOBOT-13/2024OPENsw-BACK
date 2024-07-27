from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email
from allauth.account.models import EmailAddress
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
from django.contrib import messages

def user_pk_to_url_str(user):
    return urlsafe_base64_encode(force_bytes(user.pk))

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_confirmation_mail(self, request, emailconfirmation, signup):
        # 커스텀 템플릿 경로 설정
        current_site = request.get_host()
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        context = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
        }
        # 커스텀 템플릿 사용
        subject = render_to_string("account/email/email_confirmation_signup_subject.txt", context)
        subject = ''.join(subject.splitlines())  # remove superfluous line breaks
        message = render_to_string("account/email/email_confirmation_signup_message.txt", context)
        html_message = render_to_string("account/email/email_confirmation_signup_message.html", context)


         # Django의 EmailMultiAlternatives 사용
        email = EmailMultiAlternatives(
            subject,
            message,
            to=[emailconfirmation.email_address.email]
        )
        email.attach_alternative(html_message, "text/html")
        email.send()
    
        # self.send_mail("account/email/email_confirmation_signup_message.html", emailconfirmation.email_address.email, context)
    
    def send_email_confirmation(self, request, user, signup=False, email=None):
        email_address = None
        if not email:
            email = user_email(user)
        if not email:
            email_address = (
                EmailAddress.objects.filter(user=user).order_by("verified", "pk").first()
            )
            if email_address:
                email = email_address.email

        if email:
            if email_address is None:
                try:
                    email_address = EmailAddress.objects.get_for_user(user, email)
                except EmailAddress.DoesNotExist:
                    pass
            if email_address is not None:
                if not email_address.verified:
                    send_email = self.should_send_confirmation_mail(
                        request, email_address, signup
                    )
                    if send_email:
                        email_address.send_confirmation(request, signup=signup)
                else:
                    send_email = False
            else:
                send_email = True
                email_address = EmailAddress.objects.add_email(
                    request, user, email, signup=signup, confirm=True
                )
                assert email_address
            # At this point, if we were supposed to send an email we have sent it.
            if send_email:
                self.add_message(
                    request,
                    messages.INFO,
                    "templates/account/email/email_confirmation_signup_message.html",
                    {"email": email, "login": not signup, "signup": signup},
                )
        if signup:
            self.stash_user(request, user_pk_to_url_str(user))
