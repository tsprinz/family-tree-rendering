from django.db import models
from django.core.exceptions import ValidationError

"""

"""


"""
Validates birth and death dates to be sequential
"""
def validate_dates(date1, date2):
    if date2 < date1:
        raise ValidationError(
            'Death date is before the birth date',
            params={
                'birth_date': date1,
                'death_date': date2,
            },
        )

class Relationship(models.Model):
    
    RELATIONSHIP_CHOICES = [
        ('p', 'partnered'),
        ('e', 'engaged'),
        ('m', 'married'),
        ('d', 'divorced'),
        ('o', 'other'),
    ]
    relation_type = models.CharField(max_length=1, choices=RELATIONSHIP_CHOICES)
    person_a = models.ForeignKey('Person', on_delete = models.PROTECT, related_name = 'persona', verbose_name = 'Partner')
    person_b = models.ForeignKey('Person', on_delete = models.PROTECT, related_name = 'personb', verbose_name = 'Partner')

    def __str__(self):
        return "%s & %s, %s" % (self.person_a, self.person_b, self.get_relation_type_display())

class Person(models.Model):
    class Meta:
        verbose_name_plural = "people"
    
    first_name = models.CharField(max_length=20)
    middle_names = models.CharField(max_length=83, blank = True, default = '')
    last_name = models.CharField(max_length=20)
    birth_name = models.CharField(max_length=20, blank = True, null = True)
    display_name = models.CharField(max_length=131, blank = True, null = True)

    birth_date = models.DateField()
    death_date = models.DateField(null=True, blank=True, validators=[validate_dates])
    parents = models.ForeignKey('Relationship', on_delete = models.SET_NULL, null = True, blank = True, related_name = 'parents', verbose_name = 'Parent Relation')
    
    image = models.ImageField(upload_to='photos/', blank = True, verbose_name = 'Upload photo')

    GENDER_CHOICES = [
        ('m', 'male'),
        ('f', 'female'),
        ('d', 'diverse'),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null = True, blank = True)

    def __str__(self):
        return "%s, %s, * %s" % (self.last_name.upper(), self.first_name, self.birth_date.year)
