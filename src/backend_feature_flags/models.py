from django.db import models


class Feature(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=False)
    desciption = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    succeeded = models.BooleanField(default=False, help_text="Feature confirmed working.")
    remove_old_func = models.BooleanField(default=False, verbose_name="Remove old functionality", help_text="Feature change was successful and old code can be removed.")
    created_by = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_by = models.CharField(max_length=100)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Feature Flag"
        verbose_name_plural = "Feature Flags"

    def __str__(self):
        return self.name
    
    # def save(self, *args, **kwargs):
    #     if self
    #     super(Feature, self).save(*args, **kwargs)