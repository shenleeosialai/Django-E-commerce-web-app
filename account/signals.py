from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from cart.utils import stash_cart_before_auth, restore_cart_after_auth

@receiver(user_logged_in)
def preserve_cart_on_login(sender, request, user, **kwargs):
    cart_backup = request.session.get('pre_login_cart')
    if cart_backup:
        restore_cart_after_auth(request, cart_backup)
        del request.session['pre_login_cart']
