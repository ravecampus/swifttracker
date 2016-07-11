from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
class AuthViewMixins(object):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self, *args, **kwargs):

        return super(AuthViewMixins, self).dispatch(*args, **kwargs)