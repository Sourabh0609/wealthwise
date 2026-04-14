from django.contrib import admin
from .models import UserProfile, Investment, PortfolioRecommendation

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'annual_income', 'risk_tolerance', 'investment_goal']
    list_filter = ['risk_tolerance', 'investment_goal']

@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = ['user', 'amount', 'created_at']
    list_filter = ['created_at']

@admin.register(PortfolioRecommendation)
class PortfolioRecommendationAdmin(admin.ModelAdmin):
    list_display = ['investment']  # REMOVED 'created_at' from here