from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Profile
import razorpay as raz
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
import razorpay
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.conf import settings

from users.models import CustomUser , UserSubscription
from .models import Subscription  # your Subscription model
from django.contrib.auth.models import User

client = raz.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

from django.shortcuts import render
import os

def index(request):
    return render(request, "index.html", {
        "RAZORPAY_KEY_ID": os.environ.RAZORPAY_KEY_ID
    })




@csrf_exempt
def verify_payment(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

            # Verify the signature
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            return JsonResponse({'success': True})

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({'success': False, 'error': 'Signature verification failed'}, status=400)

        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            amount = int(request.POST.get("amount"))  # convert to paise
            payment = client.order.create({
                "amount": amount,
                "currency": "INR",
                "payment_capture": 1
            })
            return JsonResponse(payment)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)
    print("Amount : " , amount)
    return JsonResponse({"error": "Invalid request"}, status=405)

@csrf_exempt
@api_view(['POST'])
def update_plan(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            email = body.get('email')
            plan = body.get('plan')

            if not email or not plan:
                return JsonResponse({'success': False, 'message': 'Email or plan missing'}, status=400)

            user = CustomUser.objects.get(email=email)
            subscription, created = UserSubscription.objects.get_or_create(user=user)
            subscription.tier = plan.lower()
            subscription.save()

            return JsonResponse({'success': True, 'message': 'Plan updated'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'User not found'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=500)

    return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)