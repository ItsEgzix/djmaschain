from django.shortcuts import render
import requests
import json
import os
from django.conf import settings

def landing_page(request):
    return render(request, 'index.html')
def notfound(request):
    return render(request, '404.html')

from datetime import datetime
import json
import os
import requests
from django.conf import settings
from django.shortcuts import render

def fetchdata(request):
    if request.method == 'POST':
        model = request.POST.get('model')
        color = request.POST.get('color')
        # images = request.FILES.getlist('images')
        car_Chasses_Number = request.POST.get('car_Chasses_Number')
        manfuctureer = request.POST.get('manfuctureer')
        Year = request.POST.get('Year')
        Distance = request.POST.get('Distance')
        discription = request.POST.get('discription')

        # Generate the timestamp automatically
        time_stamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        print(discription)

        url = 'API_URL'
        client_id = 'id'
        client_secret = 'id'

        headers = {
            'client_id': client_id,
            'client_secret': client_secret,
        }

        # Prepare the metadata and files for the API request
        metadata = {
            'wallet_address': 'id',
            'contract_address': 'id',
            'metadata[]': f'{car_Chasses_Number}, {manfuctureer}, {model}, {Year}, {Distance}, {color}, {time_stamp}, {discription}',
            'callback_url': 'https://service-testnet.maschain.com/'
        }

        try:
            response = requests.post(url, headers=headers, data=metadata)
            response.raise_for_status()
            result = response.json()

            file_path = os.path.join(settings.BASE_DIR, 'data.json')

            with open(file_path, 'a') as json_file:
                json_file.write(json.dumps(result) + "\n")

        except requests.exceptions.RequestException as e:
            result = {'error': str(e)}

        return render(request, 'fetchdata.html', {'data': result})

    return render(request, 'fetchdata.html')


def search(request):
    if request.method == 'POST':
        search_chassis_number = request.POST.get('search_chassis_number')

        url = f'API_URL'
        client_id = 'id'
        client_secret = 'id'

        headers = {
            'client_id': client_id,
            'client_secret': client_secret,
        }

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status() # Raise an error for bad responses
            data = response.json()
            

            results = []
            result_items = data.get('result', None)

            print("-----------------")
            print(result_items)

            if result_items:
                for item in result_items:
                    metadata = item.get('metadata', '[]')
                    metadata_list = json.loads(metadata)
                    # Check if the chassis number matches
                    if search_chassis_number in metadata_list[0]:
                        results.append({
                            'metadata': metadata_list,
                            'transaction_hash': item.get('transactionHash'),
                            'status': item.get('status'),
                            'upload_date': item.get('upload_date', 'Unknown')
                        })
            else:
                # file_path = os.path.join(settings.BASE_DIR, 'data.json')

                # with open(file_path, 'r') as json_file:
                #     data = json_file.readlines()
                #     print(data)
                results = fetch_data_by_chassis_number(search_chassis_number)
                print("results: ", results)

        except requests.exceptions.RequestException as e:
            results = {'error': str(e)}

        return render(request, 'search.html', {'results': results})
    
    return render(request, 'search.html')

def fetch_data_by_chassis_number(chassis_number):
    file_path = os.path.join(settings.BASE_DIR, 'data.json')
    results = []

    with open(file_path, 'r') as json_file:
        lines = json_file.readlines()

    for line in lines:
        try:
            record = json.loads(line)
            metadata = record.get('result', {}).get('metadata', '')

            metadata_list = json.loads(metadata)
            if metadata_list[0].split(",")[0] == str(chassis_number):
                results.append(metadata_list[0].split(","))
        except json.JSONDecodeError:
            continue  # Skip lines that are not valid JSON

    return results if results else None



