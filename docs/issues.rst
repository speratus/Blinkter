Known Issues
============
The issues listed below are ones which have been discovered but for which there is no immediate fix planned.
They are most likely not bugs. Careful coding may in some cases allow you to avoid some of them, while others may
be unavoidable for the time being.

Although there may be no fixes planned for these issues in the immediate future, that does not mean that they are not
being worked on. At the time of writing, all the issues in this list have planned fixes, but which due to the complexity
of the fixes, work has not yet begun on  implementing them.

**NOTE:** This list is separate from the list on `the Github issues <https://github.com/speratus/Blinkter/issues>`_ page.
It's purpose is to provide a list of issues which, while known, are not currently being worked on and the reasoning
for the decision not to work on them. The issues found here may be listed on Github but are not necessarily listed there.
This page may be removed in the future, should the `Github issues <https://github.com/speratus/Blinkter/issues>`_ prove
sufficient.

1. Simultaneous pixel blinking lags noticeably
---------------------------------------------
**Description:** Attempting to cause all the pixels to blink simultaneously results in noticeable lag.

This is issue is unavoidable. Due to the way in which multi-threaded blinking is handled, this issue is currently
unavoidable.

Cause
~~~~~
Thread locking. Each blink thread blocks while it waits for the lock on the :class:`BlinktBoard` to be released. Once
The lock is released, the next thread in line acquires it and draws to to the :class:`BlinktBoard`.

Solution
~~~~~~~~
Do not attempt to blink more than two or three pixels at a time for the time being. There is a probable fix for this
issue in the planning stage, but it is not likely to be implemented soon.

2. Multiple :meth:`Pixel.draw` calls from different interpreters cancel each other out
--------------------------------------------------------------------------------------
**Description:** If two or more interpreters create instances of :class:`BlinktBoard` and draw to the blinkt,
they will overwrite each other such that only the most recent call is displayed.

This issue is unavoidable. The only solution is to ensure that only one interpreter has an instance of :class:`BlinktBoard`
at a time.

Cause
~~~~~
This issue is not caused by a design flaw in ``blinkter``'s code, but in a design flaw in the |blinkt| code. Due to the
way in which |blinkt| writes to the GPIO, this problem will always occur when one has multiple interpreters open.

Solution
~~~~~~~~
As mentioned above, the only workaround to this issue is to make sure that only one interpreter accesses :class:`BlinktBoard`.
There are a couple of possible fixes for this problem but both are complicated and development has begun on neither.
