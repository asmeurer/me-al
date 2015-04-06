'''
MeTal - The Decorator
=====================

Synopsis
--------
So, you've fully explored the use of decorators and maybe even
decorators with arguments.  Where do you go from there?  Where you
ask?  You, my friend, need to apply MeTal--as in
[Heavy Metal](http://en.wikipedia.org/wiki/Metal_umlaut).

For example, here is a function:

    # simple.py
    def hello(name):
        print('Hello', name)

Here is the same function with some MeTal indicated:

    # simple.py

    def HellO(name):
        print('Hello', name)

The only remaining step is for you to apply the kind of metal you
desire.  This is done using a standard decorator function:

    # example.py
    import meTal

    # A decorator (aka., "the meTal")
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("Decorator")
            return func(*args, **kwargs)
        return wrapper

    # Apply the meTal to the module
    with meTal(decorator):
        import simple

    # Call the module with the meTal applied
    simple.hello('Guido')

Now, run your program:

    bash % python3 example.py
    Decorator
    Hello Guido
    bash %

You'll see your decorator applied to the functions requesting
meTal. If the above command fails with an ImportError, you're probably
using a Mac. That's an unfortunate choice as you can't really expect a
toy machine like that to be used for serious tasks.  Nevertheless, if
you'd really like to apply meTal anyways, you can still do it by
changing the top level import to the following:

    # example.py
    meTal = __import__('met\u0308al')
    ...

Although, for maximum portability, I'd suggest the following:

    try:
        import meTal
    except ImportError:
        meTal = __import__('met\u0308al')

Closer to the MeTal
-------------------
Our simple example was really just a small taste to get the idea. If
you really want to get serious though, you can use MeTal with a
package such as [Numba](http://numba.pydata.org/):

    import meTal
    from numba import jit

    with meTal(jit):
        import simple

Now, you're starting to get the idea.

MeTal is Different
------------------
MeTal allows different decorators to be applied to the same module on
different import statements--even in the same file!  Observe:

    def decorator1(func):
        def wrapper(*args, **kwargs):
            print("Decorator 1")
            return func(*args, **kwargs)
        return wrapper

    def decorator2(func):
        def wrapper(*args, **kwargs):
            print("Decorator 2")
            return func(*args, **kwargs)
        return wrapper

    # Use a module with decorator1 meTal applied
    with meTal(decorator1):
        import simple
        simple.hello('Guido')

    # Use a module with decorator2 meTal applied
    with meTal(decorator2):
        import simple
        simple.hello('Guido')

    # Use a module with decorator1 and decorator2 meTal applied
    with meTal(decorator1), meTal(decorator2):
        import simple
        simple.hello('Guido')

In fact, completely different modules can import the same module, each
with different meTal applied to it.  Try doing that with normal
decorators!

How it Works
------------
When activated, MeTal monitors all import statements in your program
and looks for identifiers that include an metal umlaut (such names are
said to be "meTalized").  If found, those definitions are firstly
replaced by non-umlaut names.  Thus, if your program looks like this:

    # simple.py
    def HellO(name):
        print('Hello', name)

You don't use the umlauts when calling.  You simply write code like
you always did before.  For example:

    import simple
    simple.hello('Guido')

This behavior allows MeTal to be added to existing programs without
changing any other code--simply put in umlauts in the names of the
functions that support meTalization and they'll be wrapped seamlessly.

If you put the import statements inside a with-statement you can
have a decorator automatically applied to the meTalized definitions
for that import. For example,

    import meTal
    with meTal(decorator):
        import simple

is equivalent to doing the following:

    # simple.py

    @decorator
    def hello(name):
        print('Hello', name)

However, unlike a normal decorator, keep in mind that this wrapping
only applies in the file that actually performed the meTalized import.
If other files have imported simple, they won't see the extra meTal
that's been applied.  Too bad for them--although they could be applying
their own meTal.

If the decorator takes arguments, simply supply them.  For example,

    import meTal
    with meTal(decorator, arg1, arg2):
        import simple

is equivalent to doing this:

    # simple.py

    @decorator(arg1, arg2)
    def hello(name):
        print('Hello', name)

You might be asking how MeTal is able to apply different decorators
to different import statements and keep the resulting functions
separate?  That question is easily answered by reading the source.

MeTal - Better than Explicit
----------------------------
MeTal allows framework builders to explicitly indicate those functions
that could be assisted with the addition of some meTal.  However,
unlike a normal decorator, it puts the power back into the hands of
the end-user where it belongs.  In this arrangement, everyone wins.
For example, if code is running slow, framework authors can simply
tell users to try putting a bit of meTal on it. Users then get the
full say on what meTal they apply.  What's more, different users can
easily apply the meTal of their choice without worrying about
others--no need for bikesheds here! Yes, the benefits are quite clear.

Compatibility
-------------
MeTal only works with Python 3.  If you love Python and you're still
coding in Python 2, well, then fuck you.

Limitations of MeTal
--------------------
None are known or anticipated.

Frequently "Asked" Questions
----------------------------
Q: How do you type the T character?

A: Using the T key. WTF?

Q: Can meTal be installed using pip or easy_install?

A: No.

Q: Why is the Github repo called "me-al"?

A: Reasons.

Author
------
MeTal is the creation of David Beazley (@dabeaz) who officially
disavows all involvement.
'''

import sys
import types
import __builtin__ as builtins
from contextlib import contextmanager

__meTalized__ = []
_meTalizers = []

_builtin_import = __import__
def _meTalizing_import(*args, **kwargs):
    module = _builtin_import(*args, **kwargs)
    if not hasattr(module, '__meTalized__'):
        names = dir(module)
        meTalized_names = [(name, name.lower()) for name in names]
        setattr(module, '__meTalized__', [normed for name, normed in
            meTalized_names if name != normed])
        for name, normed in meTalized_names:
            if name != normed:
                setattr(module, normed, module.__dict__.pop(name))

    if not _meTalizers:
        return module

    meTalized = types.ModuleType(module.__name__)
    meTalized.__dict__.update(module.__dict__)
    for name in module.__meTalized__:
        defn = getattr(meTalized, name)
        for decorate, dargs, dkwargs in reversed(_meTalizers):
            if dargs or dkwargs:
                defn = decorate(*dargs,**dkwargs)(defn)
            else:
                defn = decorate(defn)
        setattr(meTalized, name, defn)
    return meTalized

builtins.__import__ = _meTalizing_import

@contextmanager
def meTalmanager(decorate, dargs, dkwargs):
    _meTalizers.append((decorate, dargs, dkwargs))
    try:
        yield
    finally:
        _meTalizers.pop()

class MeTal(types.ModuleType):
    __ = sys.modules[__name__]
    def __call__(self, decorator, *args, **kwargs):
        return meTalmanager(decorator, args, kwargs)

sys.modules[__name__] = MeTal(__name__)
