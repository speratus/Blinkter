Version Information
===================
This page describes the meaning of the version number in addition to laying out what has changed in each release.

Blinkter follows the `Semantic Versioning system <semver.org>`_ described on `semver.org <semver.org>`_. This means that
the first element of the version number is the major version. When this number changes, it means that newer versions
introduce backwards incompatible changes. The second element indicates that backwards compatible changes have been
added to newer versions. Finally, the third number indicates that backwards compatible bug fixes have been introduced
in newer versions.

In other words, if you are worried that updating Blinkter will break your code, remember that everything should work
the same for you as long as the major version has not changed.

Changelog
---------

1.0.0
~~~~~~~~

- Removed inconsistent behavior in :meth:`blinkter.Pixel.increment` and :meth:`blinkter.Pixel.decrement` when dealing with value overflow.
- Added ``wrap_around`` parameter to :meth:`blinkter.Pixel.increment` and :meth:`blinkter.Pixel.decrement` to allow for previous behavior
  if desired
- Blinking methods now consistently end on the color they started with
- Brightness parameters in blinking methods have implementations
- Added :meth:`Pixel.set_brightess` to precisely control the total brightness of a pixel.
- Added features that allows previous brightness value to be remembered in addition to the previous color.

1.0.0-rc1
~~~~~~~~~

- Changed Versioning system to use `Semantic Versioning <semver.org>`_.
- Rewrote the docs to be clearer and more descriptive.
- Added information to the readme and docs about contacting the repository owner.