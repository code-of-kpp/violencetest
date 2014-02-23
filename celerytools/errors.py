import abc

import six


class _ErrorsMeta(abc.ABCMeta):
    def __new__(meta, *args):
        cls = super(_ErrorsMeta, meta).__new__(meta, *args)
        cls._funcmap = dict()
        return cls

    def register(cls, subclass, func):
        super(_ErrorsMeta, cls).register(subclass)
        cls._funcmap[subclass] = func

    def __instancecheck__(cls, inst):
        if super(_ErrorsMeta, cls).__instancecheck__(inst):
            instcls = inst.__class__
            while instcls is not None and instcls not in cls._funcmap:
                instcls = instcls.__base__
            func = cls._funcmap.get(instcls)
            if func is not None:
                return func(inst)
            else:
                return True
        return False


class RecoverableError(six.with_metaclass(_ErrorsMeta, RuntimeError)):
    """If this exception was rised, the task should be retried"""
    pass


class AutoRecoverableError(
        six.with_metaclass(_ErrorsMeta, RecoverableError)):
    """If this exception was rised,
    the task should be retried automatically
    """
    pass


class FastAutoRecoverableError(
        six.with_metaclass(_ErrorsMeta, AutoRecoverableError)):
    """If this exception was rised,
    the task should be immediately automatically retried
    """
    pass


class ManualRecoverableError(
        six.with_metaclass(_ErrorsMeta, RecoverableError)):
    """If this exception was rised, the task should be retried
    after sending alarm
    """
    pass


class FatalError(six.with_metaclass(_ErrorsMeta, Exception)):
    """If this exception was rised, it should be ignored
    """
    pass


class IgnorableError(six.with_metaclass(_ErrorsMeta, Exception)):
    """If this exception is raised, it should be silently ignored
    """
    pass


def register_auto(cls, func=None):
    """ Makes exception of type cls a virtual subclass
    of AutoRecoverableError.

    >>> class E(ValueError): pass
    >>> register_auto(E)
    >>> isinstance(E(), RecoverableError)
    True
    >>> isinstance(E(), AutoRecoverableError)
    True
    >>> isinstance(E(), ManualRecoverableError)
    False
    >>> isinstance(E(), FatalError)
    False
    >>> isinstance(E(), IgnorableError)
    False
    >>> class G(object):
    ...     attribute = True
    >>> exc1 = G()
    >>> exc2 = G()
    >>> exc2.attribute = False
    >>> register_auto(G, lambda inst: inst.attribute)
    >>> isinstance(exc1, AutoRecoverableError)
    True
    >>> isinstance(exc2, AutoRecoverableError)
    False
    >>> class H():
    ...     attribute = True
    >>> exc3 = H()
    >>> exc4 = H()
    >>> exc4.attribute = False
    >>> register_auto(H, lambda inst: inst.attribute)
    >>> isinstance(exc3, AutoRecoverableError)
    True
    >>> isinstance(exc4, AutoRecoverableError)
    False
    >>> register_auto(None)
    Traceback (most recent call last):
        ...
    TypeError: Can only register classes
    >>> register_auto(type(None))  # but actually it's crazy
    >>> isinstance(None, AutoRecoverableError)
    True
    """
    RecoverableError.register(cls, func)
    AutoRecoverableError.register(cls, func)


def register_fast(cls, func=None):
    """ Makes exception of type cls a virtual subclass
    of FastAutoRecoverableError.

    >>> class E(ValueError): pass
    >>> register_fast(E)
    >>> isinstance(E(), RecoverableError)
    True
    >>> isinstance(E(), AutoRecoverableError)
    True
    >>> isinstance(E(), FastAutoRecoverableError)
    True
    >>> isinstance(E(), ManualRecoverableError)
    False
    >>> isinstance(E(), FatalError)
    False
    >>> isinstance(E(), IgnorableError)
    False
    """
    RecoverableError.register(cls, func)
    AutoRecoverableError.register(cls, func)
    FastAutoRecoverableError.register(cls, func)


def register_manual(cls, func=None):
    """ Makes exception of type cls a virtual subclass
    of ManualRecoverableError.

    >>> class E(ValueError): pass
    >>> register_manual(E)
    >>> isinstance(E(), RecoverableError)
    True
    >>> isinstance(E(), AutoRecoverableError)
    False
    >>> isinstance(E(), ManualRecoverableError)
    True
    >>> isinstance(E(), FatalError)
    False
    >>> isinstance(E(), IgnorableError)
    False
    """
    RecoverableError.register(cls, func)
    ManualRecoverableError.register(cls, func)


def register_fatal(cls, func=None):
    """ Makes exception of type cls a virtual subclass of FatalError

    >>> class E(ValueError): pass
    >>> register_fatal(E)
    >>> isinstance(E(), RecoverableError)
    False
    >>> isinstance(E(), AutoRecoverableError)
    False
    >>> isinstance(E(), ManualRecoverableError)
    False
    >>> isinstance(E(), FatalError)
    True
    >>> isinstance(E(), IgnorableError)
    False
    """
    FatalError.register(cls, func)


def register_ignore(cls, func=None):
    """ Makes exception of type cls a virtual subclass of IgnorableError

    >>> class E(ValueError): pass
    >>> register_ignore(E)
    >>> isinstance(E(), RecoverableError)
    False
    >>> isinstance(E(), AutoRecoverableError)
    False
    >>> isinstance(E(), ManualRecoverableError)
    False
    >>> isinstance(E(), FatalError)
    False
    >>> isinstance(E(), IgnorableError)
    True
    """
    IgnorableError.register(cls, func)
