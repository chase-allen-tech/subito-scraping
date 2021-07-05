from django.db import models

# Create your models here.
class Subito(models.Model):
    UserID = models.CharField(max_length=100, default='000', blank=True)
    Title = models.CharField(max_length=200, default='', blank=True)
    Description = models.CharField(max_length=2000, default='', blank=True)
    Images = models.CharField(max_length=1000, default='', blank=True)
    Mobile = models.CharField(max_length=200, default='', blank=True)   # IF
    Age = models.PositiveIntegerField(default=0, blank=True)            # IF
    Price = models.CharField(max_length=200, default='', blank=True)    # IF
    Location = models.CharField(max_length=200, default='', blank=True) # IF

    CountryID = models.IntegerField(default=0, blank=True)              # Given
    StateID = models.IntegerField(default=0, blank=True)                # Given
    CityID = models.IntegerField(default=0, blank=True)                 # Given
    CityURL = models.CharField(max_length=200, default='', blank=True)  # Given

    Section = models.IntegerField(default=0, blank=True)                # Given
    Category = models.IntegerField(default=0, blank=True)               # Given
    CategoryURL = models.CharField(max_length=200, default='', blank=True)   # Given

    Scrap = models.PositiveIntegerField(default=2, blank=True)          # Default
    Status = models.PositiveIntegerField(default=1, blank=True)         # Default
    StartDate = models.DateTimeField(auto_now=True)                     # Today