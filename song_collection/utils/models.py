from django.db import models

class AbstractDateTime(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True


# class CreatedUpdatedBy(AbstractDateTime):
#     created_by = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="created_by")
#     updated_by = models.ForeignKey("user.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="updated_by")

#     class Meta:
#         abstract=True