import os, csv
import urllib.request
from django.http import HttpResponse
from django.shortcuts import render
from papers.models import university
from .models import college

def import_college_data(request):
    csv_file_path = 'logo_results.csv'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
    }

    if not os.path.isfile(csv_file_path):
        return HttpResponse('Invalid file path. Please provide a valid CSV file path.')

    try:
        with open(csv_file_path, 'r', encoding='utf-8-sig') as file:
            reader = csv.DictReader(file)

            for row in reader:

                college_name = row.get('college_name')
                college_website = row.get('college_website')
                college_logo_url = row.get('college_logo')
                university_name = row.get('university')


                university_obj = university.objects.get(university=university_name)
                
                existing_college = college.objects.filter(college_name=college_name, university=university_obj).exists()
                
                if existing_college:
                    continue


                file_extension = os.path.splitext(college_logo_url)[1]
                filename = f"{college_name}_logo{file_extension}"
                save_path = os.path.join('static/institutes', 'logo', university_name)
                new_file_path = os.path.join(save_path, filename)

                os.makedirs(save_path, exist_ok=True)
                
                if college_logo_url:
                    req = urllib.request.Request(college_logo_url, headers=headers)
                    
                    try:
                        with urllib.request.urlopen(req) as response:
                            with open(new_file_path, 'wb') as out_file:
                                out_file.write(response.read())

                    except urllib.error.URLError:
                        # URL couldn't be fetched, save the entry without the image
                        College_obj = college(college_name=college_name, university=university_obj, college_website=college_website)
                    else:
                        # URL fetched successfully, save the entry with the image
                        College_obj = college(college_name=college_name, university=university_obj, college_website=college_website, college_logo=new_file_path)
                else:
                    # Empty URL, save the entry without the image
                    College_obj = college(college_name=college_name, university=university_obj, college_website=college_website)

                College_obj.save()
                print(College_obj)


        return HttpResponse('Data imported successfully.')

    except university.DoesNotExist:
        return HttpResponse(f'University not found. ')
    
    except Exception as e:
            print('Error occurred while importing data for row:')
            print(row)
            return HttpResponse(f'Error occurred while importing data: {str(e)}')