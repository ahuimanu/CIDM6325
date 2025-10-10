from django import forms
from .models import HomeDetails

class HomeDetailsForm(forms.ModelForm):
    BUILDING_METHOD_CHOICES = [
        ('On-site construction (Stick-built)', 'On-site construction (Stick-built)'),
        ('Modular construction', 'Modular construction'),
        ('Panelized construction', 'Panelized construction'),
        ('3D-printed construction', '3D-printed construction'),
    ]

    PRIMARY_BUILDING_MATERIAL_CHOICES = [
        ('Wood frame', 'Wood frame'),
        ('Log or timber frame', 'Log or timber frame'),
        ('Steel frame', 'Steel frame'),
        ('Concrete masonry units (CMUs or blocks)', 'Concrete masonry units (CMUs or blocks)'),
        ('Insulated Concrete Forms (ICFs)', 'Insulated Concrete Forms (ICFs)'),
        ('Masonry (Brick or stone)', 'Masonry (Brick or stone)'),
        ('Alternative materials (Straw bale, cob, rammed earth)', 'Alternative materials (Straw bale, cob, rammed earth)'),
    ]

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
    ]

    username = forms.CharField(label="Username", max_length=255, required=True)
    building_method = forms.ChoiceField(choices=BUILDING_METHOD_CHOICES, required=True)
    primary_building_material = forms.ChoiceField(choices=PRIMARY_BUILDING_MATERIAL_CHOICES, required=True)
    climate_zone = forms.ChoiceField(choices=CLIMATE_ZONE_CHOICES, required=True)
    year_built = forms.IntegerField(label="Year Built", required=True)
    square_feet = forms.IntegerField(label="Square Feet", required=True)

    class Meta:
        model = HomeDetails
        fields = ['username', 'year_built', 'climate_zone', 'number_of_appliances', 'building_method', 'primary_building_material', 'square_feet']

    def clean_year_built(self):
        year_built = self.cleaned_data.get('year_built')
        if year_built < 1800 or year_built > 2025:  # Adjust the range as needed
            raise forms.ValidationError("Please enter a valid year between 1800 and 2025.")
        return year_built

    def clean_number_of_appliances(self):
        number_of_appliances = self.cleaned_data.get('number_of_appliances')
        if number_of_appliances < 0:
            raise forms.ValidationError("Number of appliances cannot be negative.")
        return number_of_appliances

    def clean_square_feet(self):
        square_feet = self.cleaned_data.get('square_feet')
        if square_feet < 0:
            raise forms.ValidationError('Square Feet must be a non-negative number.')
        return square_feet

    def clean(self):
        cleaned_data = super().clean()

        for field, value in cleaned_data.items():
            if value == "Blank" or value == "" or value is None:
                raise forms.ValidationError(f"The field '{field}' cannot be blank.")

        return cleaned_data