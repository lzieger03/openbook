openbook.drf.tests
==================

.. py:module:: openbook.drf.tests


Classes
-------

.. autoapisummary::

   openbook.drf.tests.APISchemaTestCase


Module Contents
---------------

.. py:class:: APISchemaTestCase(methodName='runTest')

   Bases: :py:obj:`django.test.TestCase`

   .. autoapi-inheritance-diagram:: openbook.drf.tests.APISchemaTestCase
      :parts: 1


   Similar to TransactionTestCase, but use `transaction.atomic()` to achieve
   test isolation.

   In most situations, TestCase should be preferred to TransactionTestCase as
   it allows faster execution. However, there are some situations where using
   TransactionTestCase might be necessary (e.g. testing some transactional
   behavior).

   On database backends with no transaction support, TestCase behaves as
   TransactionTestCase.


   .. py:method:: test_get_schema()

      Don't crash when downloading the API schema.



