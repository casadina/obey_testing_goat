import sys
from accounts.models import ListUser, Token


class PasswordlessAuthenticationBackend(object):

    @staticmethod
    def authenticate(self, uid):
        print("uid", uid, file=sys.stderr)
        if not Token.objects.filter(uid=uid).exists():
            print("no token", file=sys.stderr)
            return None
        token = Token.objects.get(uid=uid)
        print('got token', file=sys.stderr)
        try:
            user = ListUser.objects.get(email=token.email)
            print('got user', file=sys.stderr)
            return user
        except ListUser.DoesNotExist:
            print('new user', file=sys.stderr)
            return ListUser.objects.create(email=token.email)

    @staticmethod
    def get_user(self, email):
        return ListUser.objects.get(email=email)
