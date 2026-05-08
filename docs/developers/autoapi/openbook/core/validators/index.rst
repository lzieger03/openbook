openbook.core.validators
========================

.. py:module:: openbook.core.validators


Classes
-------

.. autoapisummary::

   openbook.core.validators.ValidateImage


Functions
---------

.. autoapisummary::

   openbook.core.validators.validate_library_name_part
   openbook.core.validators.validate_version_number
   openbook.core.validators.validate_version_expression
   openbook.core.validators.validate_library_fqn
   openbook.core.validators.validate_library_version_fqn
   openbook.core.validators.split_library_fqn
   openbook.core.validators.split_library_version_fqn


Module Contents
---------------

.. py:class:: ValidateImage(max_size=1024 * 1024)

   Validate image uploads so that only image files with an allowed maximum
   size are accepted.


   .. py:attribute:: max_size
      :value: 1048576



.. py:function:: validate_library_name_part(part)

   Each part of a library name must be alpha-numeric and at least three characters long.


.. py:function:: validate_version_number(version)

   Check that version numbers use semver with numeric major, minor, patch
   and optional -prerelease and +build tags.


.. py:function:: validate_version_expression(version_expression)

   Check that the expression contains a valid semver, optionally with one of the following
   operators supported by the `semver` package:

   * `<`:  smaller than
   * `>`:  greater than
   * `<=`: smaller or equal than
   * `>=`: greater or equal than
   * `==`: equal
   * `!=`: not equal

   See: https://python-semver.readthedocs.io/en/latest/usage/compare-versions-through-expression.html


.. py:function:: validate_library_fqn(fqn)

   Check that the fully qualified name of a library roughly follows the same guidelines as
   for Node.js packages in npmjs.org: `@organization/package`, whereas each part must be at
   least three characters long and may only contain alpha-numerics, underline, minus or dot.

   Note: Unlike on npmjs.org the organization is mandatory for us.


.. py:function:: validate_library_version_fqn(fqn)

   Validate fully qualified library version: `@organization/library 1.0.0`.


.. py:function:: split_library_fqn(fqn)

   Split fully qualified library name into organization (without `@`) and library name.
   Raises a `ValidationError` if the input string doesn't match the expected format.


.. py:function:: split_library_version_fqn(fqn)

   Split fully qualified library version into organization (without `@`), library name and version.
   Raises a `ValidationError` if the input string doesn't match the expected format.


