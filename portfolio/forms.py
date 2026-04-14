from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    age = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '18',
            'max': '100'
        }),
        required=True
    )
    
    annual_income = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '₹ Annual Income'
        }),
        required=True
    )
    
    risk_tolerance = forms.ChoiceField(
        choices=UserProfile.RISK_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    investment_goal = forms.ChoiceField(
        choices=UserProfile.GOAL_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    time_horizon = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '1',
            'max': '50',
            'placeholder': 'Years'
        }),
        required=True
    )
    
    class Meta:
        model = UserProfile
        fields = ['age', 'annual_income', 'risk_tolerance', 'investment_goal', 'time_horizon']

class InvestmentForm(forms.Form):
    investment_amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': '₹ Investment Amount',
            'min': '1000'
        }),
        required=True
    )