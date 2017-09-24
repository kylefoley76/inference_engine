from django.db import models


# Create your models here.


class InstructionFile(models.Model):
    name = models.CharField(max_length=100, default='name')
    data = models.FileField(upload_to='./static/inference2/')
    FILE_TYPE_CHOICES = (
        ('0', 'rules_in_depth'),
        ('1', 'downloadable_file'),
        ('2', 'rules_in_brief'),
    )
    COLOR_CHOICES = (
        ('red', 'red'),
        ('green', 'green'),
        ('blue', 'blue'),
        ('white', 'white'),
    )
    file_type = models.CharField(
        max_length=1, choices=FILE_TYPE_CHOICES, default='0')
    color_type = models.CharField(
        max_length=10, choices=COLOR_CHOICES, default='white')

    def save(self, *args, **kwargs):
        super(InstructionFile, self).save(*args, **kwargs)
        filename = self.data.url


class Archives(models.Model):
    archives_date = models.DateField()
    algorithm = models.CharField(max_length=300, blank=False, null=False)
    dictionary = models.CharField(max_length=300, blank=False, null=False, default='')

    def __unicode__(self):
        return u'{0}, {1}'.format(self.archives_date, self.algorithm)

    def __str__(self):
        return u'{0}, {1}'.format(self.archives_date, self.algorithm)

    class Meta:
        managed = True
        db_table = 'archives'


class Define3Notes(models.Model):
    notes = models.TextField()

    def __str__(self):
        return u'{0}'.format(self.id)


class Define3(models.Model):
    extra = models.CharField(max_length=1000, blank=True, null=True)
    type = models.CharField(max_length=1000, blank=True, null=True)
    word = models.CharField(max_length=1000, blank=True, null=True)
    rel = models.CharField(max_length=1000, blank=True, null=True)
    definition = models.CharField(max_length=1000, blank=True, null=True)
    subject = models.CharField(max_length=1000, blank=True, null=True)
    def_object = models.CharField(max_length=1000, blank=True, null=True)
    archives = models.ForeignKey(Archives, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'define3'


class Input(models.Model):
    col1 = models.CharField(max_length=5, blank=True, null=True)
    col2 = models.CharField(max_length=1000, blank=True, null=True)
    col3 = models.CharField(max_length=300, blank=True, null=True)
    archives = models.ForeignKey(Archives, on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'input'


class Output(models.Model):
    col1 = models.CharField(max_length=200, blank=True, null=True)
    col2 = models.CharField(max_length=1000, blank=True, null=True)
    col3 = models.CharField(max_length=300, blank=True, null=True)
    archives = models.ForeignKey(Archives)

    class Meta:
        managed = True
        db_table = 'output'
        verbose_name = "Argument"
        verbose_name_plural = "Arguments"

    def __str__(self):
        return u'{0}'.format(self.id)


class Algorithm(models.Model):
    def validate_file_extension(value):
        from django.core.exceptions import ValidationError
        if not value.name.endswith('.py'):
            raise ValidationError(
                u'Only files with py extenstion are supported.')

    name = models.CharField(max_length=200)
    notes = models.TextField(null=True, blank=True)
    data = models.FileField(upload_to='./inference2/Proofs/', validators=[])
    dictionary = models.FileField(upload_to='./inference2/Proofs/', validators=[])
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        super(Algorithm, self).save(*args, **kwargs)


class Profile(models.Model):
    name = models.CharField(max_length=200)
    about = models.TextField()
    hobbies = models.CharField(max_length=500, null=True, blank=True)
    skills = models.CharField(max_length=500, null=True, blank=True)
    facebook = models.CharField(max_length=200, null=True, blank=True)
    twitter = models.CharField(max_length=200, null=True, blank=True)
    instagram = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return u'{0}'.format(self.id)
