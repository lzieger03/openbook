# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from openbook.auth.models.mixins.audit import CreatedModifiedByMixin
from openbook.core.models.mixins.file import FileUploadMixin
from openbook.core.models.mixins.uuid import UUIDMixin
from openbook.core.models.utils.file import calc_file_path


class AssistantDocument(UUIDMixin, FileUploadMixin, CreatedModifiedByMixin):
    """Uploaded source document used by the assistant for retrieval."""

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        blank=True,
        default="",
    )

    class Meta:
        verbose_name = _("Assistant Document")
        verbose_name_plural = _("Assistant Documents")
        ordering = ("title", "file_name")
        indexes = [
            models.Index(fields=("title", "file_name")),
        ]

    def calc_file_path_hook(self, filename):
        """Store assistant uploads below the assistant app namespace."""
        return calc_file_path(self._meta, self.id, filename)

    def __str__(self):
        return self.title or self.file_name or str(_("Untitled assistant document"))


class AssistantDocumentChunk(UUIDMixin, CreatedModifiedByMixin):
    """Text chunk and embedding generated from an assistant document."""

    parent = models.ForeignKey(
        "openbook_assistant.AssistantDocument",
        verbose_name=_("Assistant Document"),
        on_delete=models.CASCADE,
        related_name="chunks",
    )

    position = models.PositiveIntegerField(
        verbose_name=_("Position"),
        default=0,
        help_text=_("Order of the chunk inside the uploaded source document."),
    )

    content = models.TextField(
        verbose_name=_("Content"),
        blank=True,
        default="",
    )

    embedding = models.BinaryField(
        verbose_name=_("Embedding"),
        blank=True,
        default=bytes,
        help_text=_("Serialized float32 embedding used by the vector search index."),
    )

    class Meta:
        verbose_name = _("Assistant Document Chunk")
        verbose_name_plural = _("Assistant Document Chunks")
        ordering = ("parent", "position")
        indexes = [
            models.Index(fields=("parent", "position")),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("parent", "position"),
                name="openbook_assistant_unique_document_chunk_position",
            ),
        ]

    def __str__(self):
        return _("{document} chunk {position}").format(
            document=self.parent,
            position=self.position,
        )


@receiver(pre_delete, sender=AssistantDocument)
def delete_document_vector_index(sender, instance, **kwargs) -> None:
    """Remove technical vector index rows when a document is deleted."""
    from openbook.assistant.services.vector_index import delete_document_vectors

    delete_document_vectors(instance.id, using=kwargs["using"])


@receiver(pre_delete, sender=AssistantDocumentChunk)
def delete_chunk_vector_index(sender, instance, **kwargs) -> None:
    """Remove the technical vector index row when a chunk is deleted."""
    from openbook.assistant.services.vector_index import delete_chunk_vector

    delete_chunk_vector(instance.id, using=kwargs["using"])
