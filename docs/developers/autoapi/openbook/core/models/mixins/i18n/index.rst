openbook.core.models.mixins.i18n
================================

.. py:module:: openbook.core.models.mixins.i18n


Exceptions
----------

.. autoapisummary::

   openbook.core.models.mixins.i18n.TranslationMissing


Classes
-------

.. autoapisummary::

   openbook.core.models.mixins.i18n.TranslatableMixin


Functions
---------

.. autoapisummary::

   openbook.core.models.mixins.i18n.LanguageField
   openbook.core.models.mixins.i18n.get_translations


Module Contents
---------------

.. py:function:: LanguageField()

   A special model field for language codes. Technically this is a simple foreign key to
   the `Language` model of the core app.


.. py:class:: TranslatableMixin(*args, **kwargs)

   Bases: :py:obj:`django.db.models.Model`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.i18n.TranslatableMixin
      :parts: 1


   Mixin for translation models that provide translated texts for a parent model.
   Given a model named `Example`, this is how translations can be added to it:

   ```python
   class Example_T(models.Model, TranslatableMixin):
       parent = models.ForeignKey(Example, on_delete=models.CASCADE, related_name="translations")

       text1  = models.CharField(verbose_name=_("Some Text 1"), max_length=255, null=False, blank=False)
       text2  = models.CharField(verbose_name=_("Some Text 2"), max_length=255, null=False, blank=False)
       text3  = models.CharField(verbose_name=_("Some Text 3"), max_length=255, null=False, blank=False)

       class Meta(TranslatableMixin.Meta):
           verbose_name        = _("My Model: Translation")
           verbose_name_plural = _("My Model: Translations")
   ```

   The translation model simply needs a foreign key to the parent model (usually called `parent`
   with related name `translations`) and char fields for the translatable texts.

   This class can be combined with the `UUIDMixin`, if the parent class used it, too.


   .. py:attribute:: language


   .. py:class:: Meta

      .. py:attribute:: abstract
         :value: True



      .. py:attribute:: ordering
         :value: ('parent', 'language')



      .. py:attribute:: indexes



.. py:function:: get_translations(object, language = '', attr_id = 'id', attr_translations = 'translations', attr_t_parent = 'parent', attr_t_language = 'language')

   Mixin method to get translations of a model with translations. By default translations are
   stored in a second model, that installs an `translations` ("attr_translations") related attribute.
   The text model usually has the properties `parent` ("attr_t_parent") pointing to the original
   model and `language` ("attr_t_language") with the language code.

   Tries to find translations for the given language (default: language of the current thread)
   or the `LANGUAGE_CODE` setting as fallback, if different.

   Returns the best found translation or None, if none exists.


.. py:exception:: TranslationMissing

   Bases: :py:obj:`Exception`

   .. autoapi-inheritance-diagram:: openbook.core.models.mixins.i18n.TranslationMissing
      :parts: 1


   An exception that can be thrown, when a translation for something is missing.
   Note, that the `get_translations()` function doesn't throw this exception but
   rather returns `None`.


