from openbook.admin import admin_site

from .. import models
from .document import AssistantDocumentAdmin
from .document import AssistantDocumentChunkAdmin

admin_site.register(models.AssistantDocument, AssistantDocumentAdmin)
admin_site.register(models.AssistantDocumentChunk, AssistantDocumentChunkAdmin)
