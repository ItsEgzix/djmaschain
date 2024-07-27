from django.shortcuts import render
import requests
import json
import os

def fetchdata(request):
    if request.method == 'POST':
        model = request.POST.get('model')
        color = request.POST.get('color')
        images = request.FILES.getlist('images')  # Handling file uploads
        car_Chasses_Number = request.POST.get('car_Chasses_Number')
        manfuctureer = request.POST.get('manfuctureer')
        Year = request.POST.get('Year')
        Distance = request.POST.get('Distance')

        url = 'https://service-testnet.maschain.com/api/audit/audit'
        client_id = 'b8350d8791d9bba95a36ce9dac93a1ac459836207afe55cc01158071f0eb9b47'
        client_secret = 'sk_63190aebf1aa950ad33abcd9b1558d03cba39be2f629f0ff3adfb767fb410500'

        headers = {
            'client_id': client_id,
            'client_secret': client_secret,
        }

        # Prepare the metadata and files for the API request
        metadata = {
            'wallet_address': '0x50a15E05393DcAD29092c308D4128C27c7EE669f',
            'contract_address': '0x8a9FfB105bC9645D5703DfE9b22279bB490c2a92',
            'metadata[]': f'{car_Chasses_Number}, {manfuctureer}, {model}, {Year}, {Distance}, {color}',
            'callback_url': 'https://service-testnet.maschain.com/'
        }

        files = [('images', (image.name, image.read(), image.content_type)) for image in images]

        try:
            response = requests.post(url, headers=headers, data=metadata, files=files)
            response.raise_for_status()
            result = response.json()

            file_path = os.path.join('C:\\djmaschain', 'data.json')

            with open(file_path, 'a') as json_file:
                json_file.write(json.dumps(result) + "\n")

        except requests.exceptions.RequestException as e:
            result = {'error': str(e)}

        return render(request, 'fetchdata.html', {'data': result})

    return render(request, 'fetchdata.html')

