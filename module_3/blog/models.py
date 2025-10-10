from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

def validate_non_negative(value):
    if value < 0:
        raise ValidationError('Square Feet must be a non-negative number.')

class HomeDetails(models.Model):
    id = models.AutoField(primary_key=True)  # Added a unique ID field for each home
    username = models.CharField(max_length=255, null=False, default="Blank")  # Default value set to 'Blank'
    year_built = models.PositiveIntegerField(default=2000, null=False)  # Default value retained
    
    CLIMATE_ZONE_CHOICES = [
        ('Humid continental', 'Humid continental'),
        ('Humid subtropical', 'Humid subtropical'),
        ('Mediterranean', 'Mediterranean'),
        ('Oceanic (Marine west coast)', 'Oceanic (Marine west coast)'),
        ('Desert', 'Desert'),
        ('Semi-arid', 'Semi-arid'),
        ('Subarctic', 'Subarctic'),
        ('Tundra', 'Tundra'),
        ('Ice cap', 'Ice cap'),
        ('Tropical', 'Tropical'),
        ('Highland/Alpine', 'Highland/Alpine'),
    ]

    climate_zone = models.CharField(max_length=50, choices=CLIMATE_ZONE_CHOICES, null=False, default="Blank")  # Default value set to 'Blank'
    number_of_appliances = models.PositiveIntegerField(null=False, default=0)  # Default value set to 0

    BUILDING_METHOD_CHOICES = [
        ('On-site construction (Stick-built)', 'On-site construction (Stick-built)'),
        ('Modular construction', 'Modular construction'),
        ('Panelized construction', 'Panelized construction'),
        ('3D-printed construction', '3D-printed construction'),
    ]
    building_method = models.CharField(max_length=50, choices=BUILDING_METHOD_CHOICES, null=False, default="Blank")  # Default value set to 'Blank'

    PRIMARY_BUILDING_MATERIAL_CHOICES = [
        ('Wood frame', 'Wood frame'),
        ('Log or timber frame', 'Log or timber frame'),
        ('Steel frame', 'Steel frame'),
        ('Concrete masonry units (CMUs or blocks)', 'Concrete masonry units (CMUs or blocks)'),
        ('Insulated Concrete Forms (ICFs)', 'Insulated Concrete Forms (ICFs)'),
        ('Masonry (Brick or stone)', 'Masonry (Brick or stone)'),
        ('Alternative materials (Straw bale, cob, rammed earth)', 'Alternative materials (Straw bale, cob, rammed earth)'),
    ]
    primary_building_material = models.CharField(max_length=250, choices=PRIMARY_BUILDING_MATERIAL_CHOICES, null=False, default="Blank")  # Default value set to 'Blank'
    square_feet = models.PositiveIntegerField(validators=[validate_non_negative], default=0)  # Non-negative square feet

    def __str__(self):
        return self.username
