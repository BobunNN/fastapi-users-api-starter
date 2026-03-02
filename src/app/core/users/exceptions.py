class UserAlreadyExists(Exception):
    ...


class UserNotFound(Exception):
    ...


class SuperUserSelfDeleteForbidden(Exception):
    ...


class SelfDeleteNotAllowedHere(Exception):
    ...