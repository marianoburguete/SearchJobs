class AppErrorBaseClass(Exception):
    pass


class ObjectNotFound(AppErrorBaseClass):
    pass

class Forbidden(AppErrorBaseClass):
    pass

class Unauthorized(AppErrorBaseClass):
    pass

class BadRequest(AppErrorBaseClass):
    pass