from django import forms

def validate_numbers_range(value):
    # Split the input string by comma and convert to integers
    numbers = [int(num.strip()) for num in value.split(',') if num.strip().isdigit()]

    # Check if all numbers are within the range [1, 77]
    for number in numbers:
        if number < 1 or number > 77:
            raise forms.ValidationError('Numbers must be between 1 and 77.')

    # Check if exactly two numbers are provided
    if len(numbers) != 2:
        raise forms.ValidationError('Exactly two numbers are required.')

    return value

class LotteryPlayForm(forms.Form):
    numbers = forms.CharField(
        label='Enter two numbers separated by a comma',
        max_length=100,
        validators=[validate_numbers_range],
        help_text='Numbers must be between 1 and 77, separated by a comma'
    )
    amount_played = forms.FloatField(
        label='Amount Played',
        min_value=200.0,
        help_text='Minimum amount to play is 200.0'
    )

