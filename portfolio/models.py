from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField()
    annual_income = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    
    RISK_CHOICES = [
        ('conservative', 'Conservative'),
        ('moderate', 'Moderate'),
        ('aggressive', 'Aggressive'),
    ]
    
    GOAL_CHOICES = [
        ('retirement', 'Retirement Planning'),
        ('wealth', 'Wealth Accumulation'),
        ('education', 'Children Education'),
        ('house', 'House Purchase'),
        ('other', 'Other'),
    ]
    
    risk_tolerance = models.CharField(max_length=20, choices=RISK_CHOICES)
    investment_goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    time_horizon = models.IntegerField(help_text="Investment horizon in years")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"

class Investment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    allocation_data = models.JSONField(default=dict)
    expected_returns = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - ₹{self.amount}"

class PortfolioRecommendation(models.Model):
    investment = models.OneToOneField(Investment, on_delete=models.CASCADE)
    equity_recommendations = models.JSONField(default=list)
    debt_recommendations = models.JSONField(default=list)
    gold_recommendations = models.JSONField(default=list)
    cash_recommendations = models.JSONField(default=list)
    insights = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)  # ADD THIS LINE
    
    def __str__(self):
        return f"Recommendations for {self.investment.user.username}"