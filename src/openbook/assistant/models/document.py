# OpenBook: Interactive Online Textbooks - Server
# © 2026 Sebastian Wolf, Daniel Sachadä
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.

from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from openbook.auth.models.mixins.audit import CreatedModifiedByMixin
from openbook.auth.models.mixins.scope import RoleBasedObjectPermissionsMixin
from openbook.core.models.mixins.file import FileUploadMixin
from openbook.core.models.mixins.uuid import UUIDMixin
from openbook.core.models.utils.file import calc_file_path


class AssistantDocument(
    UUIDMixin,
    FileUploadMixin,
    RoleBasedObjectPermissionsMixin,
    CreatedModifiedByMixin,
):
    """Uploaded source document used by the assistant for retrieval."""

    class IndexStatusChoices(models.TextChoices):
        PENDING = "pending", _("Pending")
        INDEXING = "indexing", _("Indexing")
        INDEXED = "indexed", _("Indexed")
        FAILED = "failed", _("Failed")

    course = models.ForeignKey(
        "openbook_content.Course",
        verbose_name=_("Course"),
        on_delete=models.CASCADE,
        related_name="assistant_documents",
        null=True,
        blank=True,
        help_text=_("Course that owns this assistant document. Empty documents are global."),
    )

    textbook = models.ForeignKey(
        "openbook_content.Textbook",
        verbose_name=_("Textbook"),
        on_delete=models.CASCADE,
        related_name="assistant_documents",
        null=True,
        blank=True,
        help_text=_("Textbook this assistant document was generated from."),
    )

    title = models.CharField(
        verbose_name=_("Title"),
        max_length=255,
        blank=True,
        default="",
    )

    index_status = models.CharField(
        verbose_name=_("Index Status"),
        max_length=16,
        choices=IndexStatusChoices,
        default=IndexStatusChoices.PENDING,
        db_index=True,
    )

    index_error = models.TextField(
        verbose_name=_("Index Error"),
        blank=True,
        default="",
    )

    indexed_at = models.DateTimeField(
        verbose_name=_("Indexed At"),
        null=True,
        blank=True,
    )

    embedding_model = models.CharField(
        verbose_name=_("Embedding Model"),
        max_length=64,
        blank=True,
        default="",
    )

    chunk_count = models.PositiveIntegerField(
        verbose_name=_("Chunk Count"),
        default=0,
    )

    class Meta:
        verbose_name = _("Assistant Document")
        verbose_name_plural = _("Assistant Documents")
        ordering = ("course", "title", "file_name")
        indexes = [
            models.Index(fields=("course", "index_status")),
            models.Index(fields=("textbook", "index_status")),
            models.Index(fields=("course", "textbook", "index_status")),
            models.Index(fields=("title", "file_name")),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=("course", "textbook"),
                condition=Q(textbook__isnull=False),
                name="openbook_assistant_unique_course_textbook_document",
            ),
        ]

    def calc_file_path_hook(self, filename):
        """Store assistant uploads below the assistant app namespace."""
        return calc_file_path(self._meta, self.id, filename)

    def get_scope(self):
        """Use the owning course as object-permission scope."""
        return self.course

    def has_obj_perm(self, user_obj, perm: str) -> bool:
        """Delegate course documents to course permissions."""
        if not self.course_id:
            return False

        if perm == "openbook_assistant.view_assistantdocument":
            if user_obj.has_perm("openbook_content.view_course", self.course):
                return True

        if perm in {
            "openbook_assistant.add_assistantdocument",
            "openbook_assistant.change_assistantdocument",
            "openbook_assistant.delete_assistantdocument",
        }:
            if user_obj.has_perm("openbook_content.change_course", self.course):
                return True

        return super().has_obj_perm(user_obj, perm)

    def mark_indexing(self, embedding_model: str) -> None:
        """Set transient index state before rebuilding chunks."""
        self.index_status = self.IndexStatusChoices.INDEXING
        self.index_error = ""
        self.embedding_model = embedding_model
        self.chunk_count = 0

    def mark_indexed(self, chunk_count: int) -> None:
        """Set successful index state."""
        self.index_status = self.IndexStatusChoices.INDEXED
        self.index_error = ""
        self.chunk_count = chunk_count
        self.indexed_at = timezone.now()

    def mark_index_failed(self, error: Exception | str) -> None:
        """Set failed index state."""
        self.index_status = self.IndexStatusChoices.FAILED
        self.index_error = str(error)
        self.indexed_at = None

    def __str__(self):
        return self.title or self.file_name or str(_("Untitled assistant document"))


class AssistantDocumentChunk(UUIDMixin, RoleBasedObjectPermissionsMixin, CreatedModifiedByMixin):
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

    def get_scope(self):
        """Use the parent document course as object-permission scope."""
        return self.parent.get_scope()

    def has_obj_perm(self, user_obj, perm: str) -> bool:
        """Delegate chunk permissions through the parent document."""
        return self.parent.has_obj_perm(user_obj, perm)


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
