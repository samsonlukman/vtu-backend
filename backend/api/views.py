"""
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import requests
from django.http import JsonResponse
from django.db.models import Q
from backend.models import *
from .serializers import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.middleware.csrf import get_token
from rest_framework import filters, viewsets, status, filters, generics, permissions
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def data_api(request):
    if request.method == 'POST':
        # Extract data from the request body
        data = request.data
        api_key =  "e4b0e625664510ef4ea5c3f88734a2"
        network = data.get('network')
        phone_number = data.get('phone_number')
        product_code = data.get('product_code')

        # Construct the URL with the extracted data
        url = f"https://vtu.com.ng/API/DATA/?api_key={api_key}&network={network}&phone={phone_number}&product_code={product_code}"
        print(url)
        # Send a POST request with the data to vtu.com.ng
        response = requests.post(url)

        # Check if the request was successful
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Failed to fetch data from vtu.com.ng'}, status=response.status_code)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def vtu_api(request):
    if request.method == 'POST':
        # Extract data from the request body
        data = request.data
        api_key = "tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"
        amount = data.get('amount')
        number = data.get('number')
        product_code = data.get('product_code')

        url = f"https://quickvtu.ng/api/v1/buy-airtime?api_key={api_key}"

        payload={'amount': amount,
        'product_code': product_code,
        'number': number}
        files=[

        ]
        headers = {
        'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)
        return Response(response.json())

@api_view(['GET'])  
def data_plans(request):
    url = "https://quickvtu.ng/api/v1/data-plans?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"
    payload={}
    files={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    coverted_response = response.json()
    mtn_data = []
    mtn_product_code = []
    airtel_data = []
    airtel_product_code = []
    glo_data = []
    glo_product_code = []
    nineMobile_data = []
    nineMobile_product_code = []

    data = {"mtn": {"mtn_data": mtn_data, "product_code": mtn_product_code}, "airtel": {"airtel_data": airtel_data, "product_code": airtel_product_code }, 
            "glo": {"glo_data": glo_data, "product_code": glo_product_code},
              "nineMobile": {"nineMobile_data": nineMobile_data, "product_code": nineMobile_product_code}}
    
    for plans in coverted_response["data"]["direct_data_mtn"]:
        mtn_data.append(plans["service_name"])
    
    for plans in coverted_response["data"]["direct_data_mtn"]:
        mtn_product_code.append(plans["product_code"])
    
    for plans in coverted_response["data"]["direct_data_airtel"]:
        airtel_data.append(plans["service_name"])

    for plans in coverted_response["data"]["direct_data_airtel"]:
        airtel_product_code.append(plans["product_code"])
    
    for plans in coverted_response["data"]["direct_data_glo"]:
        glo_data.append(plans["service_name"])

    for plans in coverted_response["data"]["direct_data_glo"]:
        glo_product_code.append(plans["product_code"])

    for plans in coverted_response["data"]["direct_data_9mobile"]:
        nineMobile_data.append(plans["service_name"])
    
    for plans in coverted_response["data"]["direct_data_9mobile"]:
        nineMobile_product_code.append(plans["product_code"])

    
    return Response(data)


@api_view(['POST'])
def buy_data(request):
    if request.method == 'POST':
        # Extract data from the request body
        product_code = request.data.get('product_code')
        number = request.data.get('number')

        # Validate the data
        if not product_code or not number:
            return Response({'error': 'Product code and number are required'}, status=400)
        
        # Modify the product code to replace spaces with underscores and strip leading and trailing whitespace
        modified_product_code = product_code.strip().lower().replace(' ', '_')

        # Prepare the payload for the POST request
        payload = {
            'product_code': modified_product_code,
            'number': number
        }
        
        print(payload)
        # Specify the URL and API key
        url = "https://quickvtu.ng/api/v1/buy-data?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"

        # Set the headers
        headers = {
            'Accept': 'application/json'
        }

        # Send the POST request
        try:
            response = requests.post(url, headers=headers, json=payload)

            # Check the response status code
            if response.status_code == 200:
                return Response(response.json())
            else:
                return Response({'error': 'Failed to process the request'}, status=response.status_code)
        except Exception as e:
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    return Response({'error': 'Method not allowed'}, status=405)

"""

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

import requests
from django.http import JsonResponse
from django.db.models import Q
from backend.models import *
from .serializers import *
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.middleware.csrf import get_token
from rest_framework import filters, viewsets, status, filters, generics, permissions
from rest_framework.views import APIView
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print(user)
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)

    
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user = request.user
    serializer = UserSerializer(user)
    return Response(serializer.data)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def user_logout(request):
    logout(request)
    return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)

class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
def data_api(request):
    if request.method == 'POST':
        # Extract data from the request body
        data = request.data
        api_key =  "e4b0e625664510ef4ea5c3f88734a2"
        network = data.get('network')
        phone_number = data.get('phone_number')
        product_code = data.get('product_code')

        # Construct the URL with the extracted data
        url = f"https://vtu.com.ng/API/DATA/?api_key={api_key}&network={network}&phone={phone_number}&product_code={product_code}"
        print(url)
        # Send a POST request with the data to vtu.com.ng
        response = requests.post(url)

        # Check if the request was successful
        if response.status_code == 200:
            return Response(response.json())
        else:
            return Response({'error': 'Failed to fetch data from vtu.com.ng'}, status=response.status_code)

    return Response({'error': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def vtu_api(request):
    if request.method == 'POST':
        # Extract data from the request body
        data = request.data
        api_key = "tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"
        amount = data.get('amount')
        number = data.get('number')
        product_code = data.get('product_code')

        url = f"https://quickvtu.ng/api/v1/buy-airtime?api_key={api_key}"

        payload={'amount': amount,
        'product_code': product_code,
        'number': number}
        files=[

        ]
        headers = {
        'Accept': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, files=files)

        print(response.text)
        return Response(response.json())
    
@api_view(['GET'])  
def data_plans(request):
    url = "https://quickvtu.ng/api/v1/data-plans?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"
    payload={}
    files={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    coverted_response = response.json()
    mtn_data = []
    mtn_product_code = []
    airtel_data = []
    airtel_product_code = []
    glo_data = []
    glo_product_code = []
    nineMobile_data = []
    nineMobile_product_code = []

    data = {"mtn": {"mtn_data": mtn_data, "product_code": mtn_product_code}, "airtel": {"airtel_data": airtel_data, "product_code": airtel_product_code }, 
            "glo": {"glo_data": glo_data, "product_code": glo_product_code},
              "nineMobile": {"nineMobile_data": nineMobile_data, "product_code": nineMobile_product_code}}
    
    for plans in coverted_response["data"]["direct_data_mtn"]:
        mtn_data.append(plans["service_name"])
    
    for plans in coverted_response["data"]["direct_data_mtn"]:
        mtn_product_code.append(plans["product_code"])
    
    for plans in coverted_response["data"]["direct_data_airtel"]:
        airtel_data.append(plans["service_name"])

    for plans in coverted_response["data"]["direct_data_airtel"]:
        airtel_product_code.append(plans["product_code"])
    
    for plans in coverted_response["data"]["direct_data_glo"]:
        glo_data.append(plans["service_name"])

    for plans in coverted_response["data"]["direct_data_glo"]:
        glo_product_code.append(plans["product_code"])

    for plans in coverted_response["data"]["direct_data_9mobile"]:
        nineMobile_data.append(plans["service_name"])
    
    for plans in coverted_response["data"]["direct_data_9mobile"]:
        nineMobile_product_code.append(plans["product_code"])

    
    return Response(data)


@api_view(['GET'])  
def sme_plans(request):
    url = "https://quickvtu.ng/api/v1/sme-plans?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"
    payload={}
    files={}
    headers = {
    'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)
    coverted_response = response.json()
    mtn_data = []   
    airtel_data = []   
    glo_data = []
    nineMobile_data = []
   

    data = {"mtn": {"mtn_data": mtn_data}, "airtel": {"airtel_data": airtel_data}, 
            "glo": {"glo_data": glo_data},
              "nineMobile": {"nineMobile_data": nineMobile_data}}
    
    for plans in coverted_response["data"]["mtn_corporate_data"]:
        mtn_data.append(plans["service_name"])
    
    
    
    for plans in coverted_response["data"]["shared_data_airtel"]:
        airtel_data.append(plans["service_name"])

    
    
    for plans in coverted_response["data"]["glo_corporate_data"]:
        glo_data.append(plans["service_name"])

    

    for plans in coverted_response["data"]["shared_data_9mobile"]:
        nineMobile_data.append(plans["service_name"])
    
    

    print(response.text)

    
    return Response(data)


@api_view(['POST'])
def buy_data(request):
    if request.method == 'POST':
        # Extract data from the request body
        product_code = request.data.get('product_code')
        number = request.data.get('number')

        # Validate the data
        if not product_code or not number:
            return Response({'error': 'Product code and number are required'}, status=400)
        
        # Modify the product code to replace spaces with underscores and strip leading and trailing whitespace
        modified_product_code = product_code.strip().lower().replace(' ', '_').replace(".", "_")

        # Prepare the payload for the POST request
        payload = {
            'product_code': modified_product_code,
            'number': number
        }
        
        print(payload)
        # Specify the URL and API key
        url = "https://quickvtu.ng/api/v1/buy-data?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"

        # Set the headers
        headers = {
            'Accept': 'application/json'
        }

        # Send the POST request
        try:
            response = requests.post(url, headers=headers, json=payload)

            # Check the response status code
            if response.status_code == 200:
                print(response.text)
                return Response(response.json())
            else:
                print(response.text)
                return Response({'error': 'Failed to process the request'}, status=response.status_code)
        except Exception as e:
            print(response.text)
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    return Response({'error': 'Method not allowed'}, status=405)

@api_view(['POST'])
def buy_sme_data(request):
    if request.method == 'POST':
        # Extract data from the request body
        product_code = request.data.get('product_code')
        number = request.data.get('number')

        # Validate the data
        if not product_code or not number:
            return Response({'error': 'Product code and number are required'}, status=400)
        
        # Modify the product code to replace spaces with underscores and strip leading and trailing whitespace
        modified_product_code = product_code.strip().lower().replace(' ', '_').replace(".", "_")

        # Prepare the payload for the POST request
        payload = {
            'product_code': modified_product_code,
            'number': number
        }
        
        print(payload)
        # Specify the URL and API key
        url = "https://quickvtu.ng/api/v1/buy-sme?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"

        # Set the headers
        headers = {
            'Accept': 'application/json'
        }

        # Send the POST request
        try:
            response = requests.post(url, headers=headers, json=payload)

            # Check the response status code
            if response.status_code == 200:
                print(response.text)
                return Response(response.json())
            else:
                print(response.text)
                return Response({'error': 'Failed to process the request'}, status=response.status_code)
        except Exception as e:
            print(response.text)
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    return Response({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])  
def phcn_plans(request):
    url = "https://quickvtu.ng/api/v1/phcn-plans?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)
    converted_response = response.json()
    
    data = []

    for distribution_company, plans in converted_response["data"].items():
        for item in plans:
            service_name = item.get("service_name", "")
            product_code = item.get("product_code", "")
            data.append({"service_name": service_name, "product_code": product_code})

    return Response(data)


@api_view(['POST'])
def buy_phcn(request):
    if request.method == 'POST':
        # Extract data from the request body
        product_code = request.data.get('product_code')
        number = request.data.get('number')
        amount = request.data.get('amount')

        # Validate the data
        if not product_code or not number:
            return Response({'error': 'Product code and number are required'}, status=400)
        

        # Prepare the payload for the POST request
        payload = {
            'product_code': product_code,
            'number': number,
            'amount': amount
        }
        
        print(payload)
        # Specify the URL and API key
        url = "https://quickvtu.ng/api/v1/buy-phcn?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"

        # Set the headers
        headers = {
            'Accept': 'application/json'
        }

        # Send the POST request
        try:
            response = requests.post(url, headers=headers, json=payload)

            # Check the response status code
            if response.status_code == 200:
                print(response.text)
                return Response(response.json())
            else:
                print(response.text)
                return Response({'error': 'Failed to process the request'}, status=response.status_code)
        except Exception as e:
            print(e.text)
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    return Response({'error': 'Method not allowed'}, status=405)

@api_view(['GET'])  
def tv_plans(request):
    url = "https://quickvtu.ng/api/v1/tv-plans?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"
    headers = {'Accept': 'application/json'}

    response = requests.get(url, headers=headers)
    converted_response = response.json()
    
    data = []

    for package, plans in converted_response["data"].items():
        for item in plans:
            service_name = item.get("service_name", "")
            product_code = item.get("product_code", "")
            price = item.get("service_default_price", "")
            data.append({"service_name": service_name, "product_code": product_code, "price": price})

    return Response(data)

@api_view(['POST'])
def buy_tv(request):
    if request.method == 'POST':
        # Extract data from the request body
        product_code = request.data.get('product_code')
        number = request.data.get('number')
        

        # Validate the data
        if not product_code or not number:
            return Response({'error': 'Product code and number are required'}, status=400)
        

        # Prepare the payload for the POST request
        payload = {
            'product_code': product_code,
            'number': number,
            
        }
        
        print(payload)
        # Specify the URL and API key
        url = "https://quickvtu.ng/api/v1/buy-tv-plan?api_key=tHSaFJ1KppsuvLjewhUUbFNzWYyfRg"

        # Set the headers
        headers = {
            'Accept': 'application/json'
        }

        # Send the POST request
        try:
            response = requests.post(url, headers=headers, json=payload)

            # Check the response status code
            if response.status_code == 200:
                print(response.text)
                return Response(response.json())
            else:
                print(response.text)
                return Response({'error': 'Failed to process the request'}, status=response.status_code)
        except Exception as e:
            print(e.text)
            return Response({'error': f'An error occurred: {str(e)}'}, status=500)

    return Response({'error': 'Method not allowed'}, status=405)

class AirtimeListCreateView(generics.ListCreateAPIView):
    queryset = Airtime.objects.all()
    serializer_class = AirtimeSerializer


class AirtimeListCreateView(generics.ListCreateAPIView):
    queryset = Airtime.objects.all()
    serializer_class = AirtimeSerializer