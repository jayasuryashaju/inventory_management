# barcode_scanner/scanner/views.py
import io
import json
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

def home(request):
    return render(request, 'scanner.html')

@csrf_exempt
def upload_excel(request):
    if request.method == 'POST':
        excel_file = request.FILES['excel_file']
        df = pd.read_excel(excel_file, engine='openpyxl')

        # Add a new column 'checked' with default value False
        df['checked'] = False

        # Convert DataFrame to JSON
        excel_data = df.to_json(orient='records')

        # You can return the modified DataFrame as JSON to the frontend
        return JsonResponse({'excel_data': excel_data})

    return HttpResponse('Failed to upload Excel file')


@csrf_exempt
def check_barcode(request):
    if request.method == 'POST':
        print('i am workiking')
        # Retrieve the scanned barcode from the request data
        scanned_barcode = request.POST.get('scanned_barcode')

        # Retrieve the JSON data from the frontend
        json_data = request.POST.get('excel_data')
        excel_data = json.loads(json_data)
        print(excel_data)

        # Find the row in the Excel data with the matching barcode
        matching_row = next((row for row in excel_data if str(row.get('Unnamed: 1')) == scanned_barcode), None)

        if matching_row:
            # Mark the row by changing the 'checked' property to true
            matching_row['checked'] = True

            # Perform any other desired action

            return JsonResponse({'success': True, 'excel_data': excel_data})

    return JsonResponse({'success': False})



from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

@csrf_exempt
def download_pdf(request):
    # Retrieve the JSON data from the request
    excel_data = request.POST.get('excel_data')

    # Replace 'null' with None and 'true' with True, 'false' with False in the JSON string
    cleaned_json = excel_data.replace('null', 'None').replace('true', 'True').replace('false', 'False')

    # Convert the cleaned JSON string to a Python list
    excel_data_list = eval(cleaned_json)

    # Create a PDF document
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="excel_data.pdf"'

    # Create the PDF content
    p = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Rename columns
    for obj in excel_data_list:
        obj['Tracking Number'] = obj.pop('Unnamed: 1', None)
        obj['Order No.'] = obj.pop('Unnamed: 2', None)
        obj['Customer Name'] = obj.pop('Unnamed: 5', None)

    # Create a list to store table data
    table_data = [['Checked', 'Tracking Number', 'Order No.', 'Customer Name']]

    # Add each object to the table data
    for obj in excel_data_list:
        if obj.get("Customer Name") is not None:
            row = [obj.get("checked", ""), obj.get("Tracking Number", ""), obj.get("Order No.", ""), obj.get("Customer Name", "")]
            table_data.append(row)

    # Create the table and set style
    table = Table(table_data, colWidths=[60, 120, 80, 180], rowHeights=20)  # Adjust colWidths as needed
    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])

    # Add style for each row based on the "checked" column
    for i in range(1, len(table_data)):
        if table_data[i][0] == True:
            style.add('BACKGROUND', (0, i), (-1, i), colors.green)
        elif table_data[i][0] == False:
            style.add('BACKGROUND', (0, i), (-1, i), colors.red)

    table.setStyle(style)

    # Add the table to the PDF
    elements.append(table)

    # Build the PDF
    p.build(elements)

    return response
