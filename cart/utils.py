from copy import deepcopy

def stash_cart_before_auth(request):
    return deepcopy(request.session.get('cart', {}))

def restore_cart_after_auth(request, cart_backup):
    request.session['cart'] = cart_backup
    request.session.modified = True
