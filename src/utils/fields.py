from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.postgres.fields import ArrayField
from django.forms import MultipleChoiceField


class ChoiceArrayField(ArrayField):
    """
    A choices ArrayField that uses the `horizontal_filter` style of an M2M in the Admin

    Usage::

        class MyModel(models.Model):
            tags = ChoiceArrayField(
                models.TextField(choices=TAG_CHOICES),
                verbose_name="Tags",
                help_text="Some tags help",
                blank=True,
                default=list,
            )
    """

    def formfield(self, **kwargs):
        widget = FilteredSelectMultiple(self.verbose_name, False)
        defaults = {
            "form_class": MultipleChoiceField,
            "widget": widget,
            "choices": self.base_field.choices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        return super(ArrayField, self).formfield(**defaults)