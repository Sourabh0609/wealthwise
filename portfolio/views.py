from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import UserProfileForm, InvestmentForm
from .ml_analyzer import MLPortfolioAnalyzer
from .models import UserProfile, Investment, PortfolioRecommendation
from django.contrib.auth import logout
from django.shortcuts import redirect

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Auto-login after registration
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Account created successfully! Welcome, {username}!')
                return redirect('profile')
            else:
                messages.error(request, 'There was an error logging you in after registration.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserCreationForm()
    
    return render(request, 'portfolio/register.html', {'form': form})

@login_required
def profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'portfolio/profile.html', {'form': form})

@login_required
def dashboard(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        investments = Investment.objects.filter(user=request.user).order_by('-created_at')[:5]
        
        context = {
            'user_profile': user_profile,
            'investments': investments,
        }
    except UserProfile.DoesNotExist:
        messages.info(request, 'Please complete your profile to get started.')
        return redirect('profile')
    
    return render(request, 'portfolio/dashboard.html', context)

@login_required
def analyze_portfolio(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        messages.error(request, 'Please complete your profile before analyzing your portfolio.')
        return redirect('profile')
    
    if request.method == 'POST':
        form = InvestmentForm(request.POST)
        if form.is_valid():
            try:
                investment_amount = form.cleaned_data['investment_amount']
                
                # Initialize analyzer
                analyzer = MLPortfolioAnalyzer()
                
                # Prepare user data with defaults
                user_data = {
                    'age': user_profile.age or 30,
                    'risk_tolerance': user_profile.risk_tolerance or 'moderate',
                    'time_horizon': user_profile.time_horizon or 10,
                    'annual_income': float(user_profile.annual_income) if user_profile.annual_income else 500000.0
                }
                
                # Calculate allocation
                allocation = analyzer.calculate_optimal_allocation(user_data)
                
                # Run simulations
                projections, final_values = analyzer.monte_carlo_simulation(
                    allocation, float(investment_amount), user_data['time_horizon']
                )
                
                # Generate recommendations
                recommendations = analyzer.generate_recommendations(allocation, user_data['risk_tolerance'])
                insights = analyzer.generate_insights(user_data, allocation, projections)
                
                # Save to database
                investment = Investment.objects.create(
                    user=request.user,
                    amount=investment_amount,
                    allocation_data=allocation,
                    expected_returns=projections
                )
                
                PortfolioRecommendation.objects.create(
                    investment=investment,
                    equity_recommendations=recommendations['equity'],
                    debt_recommendations=recommendations['debt'],
                    gold_recommendations=recommendations['gold'],
                    cash_recommendations=recommendations['cash'],
                    insights=insights
                )
                
                messages.success(request, 'Portfolio analysis completed successfully!')
                
                # Prepare context for template
                context = {
                    'allocation': allocation,
                    'projections': projections,
                    'recommendations': recommendations,
                    'insights': insights,
                    'investment_amount': investment_amount,
                    'time_horizon': user_data['time_horizon'],
                    'user_profile': user_profile,
                }
                
                return render(request, 'portfolio/results.html', context)
                
            except Exception as e:
                messages.error(request, f'Error during portfolio analysis: {str(e)}')
                return redirect('analyze_portfolio')
        else:
            messages.error(request, 'Please correct the errors below.')
    
    else:
        form = InvestmentForm()
    
    context = {
        'form': form,
        'user_profile': user_profile
    }
    return render(request, 'portfolio/analyze.html', context)
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
@login_required
def investment_recommendations(request):
    try:
        latest_investment = Investment.objects.filter(user=request.user).latest('created_at')
        recommendation = PortfolioRecommendation.objects.get(investment=latest_investment)
        user_profile = UserProfile.objects.get(user=request.user)
        
        context = {
            'investment': latest_investment,
            'recommendation': recommendation,
            'user_profile': user_profile,
        }
    except (Investment.DoesNotExist, PortfolioRecommendation.DoesNotExist, UserProfile.DoesNotExist):
        messages.info(request, 'Please complete a portfolio analysis first.')
        return redirect('analyze_portfolio')
    
    return render(request, 'portfolio/recommendations.html', context)

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'portfolio/index.html')
from django.contrib.auth import logout
from django.contrib import messages

from django.contrib.auth import logout
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

def debug_logout(request):
    print(f"User before logout: {request.user}")
    print(f"User is authenticated: {request.user.is_authenticated}")
    logout(request)
    print(f"User after logout: {request.user}")
    print(f"User is authenticated after logout: {request.user.is_authenticated}")
    return redirect('home')

from django.contrib.auth import logout
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect

@require_POST
@csrf_protect
def custom_logout(request):
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')
    