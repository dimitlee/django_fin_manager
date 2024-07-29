from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


def weekday_validator(value):
    if value >= 7 or value < 0:
        raise ValidationError(
            f"{value} is not a weekday number (0-6)"
        )


def monthday_validator(value):
    if value >= 32 or value < 1:
        raise ValidationError(
            f"{value} is not a monthday number"
        )
        

class Category(models.Model):
    """Model representing category of operation (e.g. Salary, Food, Entertainment, etc.)"""
    name = models.CharField(
        max_length=200,
        help_text="Enter category of operation (e.g. Salary, Food, Entertainment, etc.)"
    )
    description = models.TextField(
        max_length=1000,
        help_text="Describe this category shortly",
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    
    def __str__(self):
        """String representing category"""
        return self.name
    
    def get_absolute_url(self):
        """Returns the url to access a particular category instance"""
        return reverse('category-detail', args=[str(self.id)])
    
    def get_add_to_user_url(self):
        """Returns the url to add this category to an authenticated user"""
        return reverse('add-category', args=[str(self.id)])
    
    def is_default(self):
        return not self.user
    
    is_default.short_description = 'Default?'
    
    class Meta:
        unique_together = ('name', 'user')
        

class Transaction(models.Model):
    """Model representing a single transaction"""
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )
    description = models.CharField(
        max_length=200,
        help_text="Describe this transaction",
        blank=True,
        default=''
    )
    sum = models.BigIntegerField(
        null=False,
        help_text="Enter the sum of the transaction"
    )
    time = models.DateTimeField(
        null=False
    )
    
    def __str__(self):
        """String representing single transaction"""
        return f"{str(self.category) + ' ' or ''}{self.sum}"
    
    def get_absolute_url(self):
        """Returns the url to access a particular transaction instance"""
        return reverse('transaction-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['-time']
    

class ScheduledTransaction(models.Model):
    """Model defines scheduled transactions (e.g. mortgage, salary, subscription, etc.)"""
    name = models.CharField(
        max_length=100,
        help_text="Give a short name for this transaction"
    )
    
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=False
    )
    description = models.CharField(
        max_length=200,
        help_text="Describe this transaction",
        blank=True,
        default=''
    )
    sum = models.BigIntegerField(
        null=False,
        help_text="Enter the sum of the transaction"
    )
    
    SCHEDULE_TYPE = (
        ('w', 'Weekly'),
        ('m', 'Monthly'),
        ('y', 'Yearly'),
        ('d', 'Daily'),
    )
    
    frequency = models.CharField(
        max_length=1,
        choices=SCHEDULE_TYPE,
        default='m',
        help_text='How often is the transaction occuring?'
    )
    
    WEEKDAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )
    
    weekday = models.IntegerField(
        null=True,
        blank=True,
        choices=WEEKDAYS,
        validators=[weekday_validator]
    )
    monthday = models.IntegerField(
        null=True,
        blank=True,
        validators=[monthday_validator]
    )
    year_date = models.DateField(
        null=True,
        blank=True
    )
    
    def __str__(self):
        """String representing single scheduled transaction"""
        return f"{str(self.name) or '-'} | {str(self.category) or '-'} | {self.sum or '-'}"
    
    def get_absolute_url(self):
        """Returns the url to access a particular scheduled transaction instance"""
        return reverse('scheduled-transaction-detail', args=[str(self.id)])