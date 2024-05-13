#INSTALL
#pip install pdfkit

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np
import re
import pdfkit


excel_file = 'msbt_previos.xlsx'
excel_sheet_name = 'Sheet1'

##CHROME OPTIONS
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
options.add_argument("--disable-extensions")
##

## DRIVER
driver_path = "../chromedriver/chromedriver-mac-arm64-v124/chromedriver"
driver = webdriver.Chrome(driver_path,chrome_options=options)
##

# Opción para guardar el PDF
options = {
    'page-size': 'Letter',
    'encoding': "UTF-8",
}

css = 'styles.css'

def get_file_name(url):
    match = re.search(r'/([^/]+)\.html', url)
    if match:
        result = match.group(1)
        return result
    return None

def get_html_text(link):
    
    driver.get(link)

    try:
        
        
        # Encuentra todos los elementos de título de sección
        section_titles = driver.find_elements(By.CSS_SELECTOR, "div.sectionTitle")
        
        # Encuentra todos los contenidos de sección
        section_contents = driver.find_elements(By.CSS_SELECTOR, "div.sectionContent")
        
        # Encuentra todas las preguntas de sección
        section_questions = driver.find_elements(By.CSS_SELECTOR, "div.sectionQuestion")
        
        # Ahora combina y ordena según la jerarquía
        content_dict = {
            # "Titles": [title.text for title in section_titles],
            # "Contents": [content.text for content in section_contents],
            "Questions": [question.text for question in section_questions]
        }
                
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.column.column2"))
        )
        columns = driver.find_elements(By.CSS_SELECTOR, "div.column.column2")

        

        columns_dict = {
            "Content": [column.get_attribute('innerHTML') for column in columns]
        }
        
        all_html_text = ''
        for index,value in enumerate(content_dict['Questions']):
            
            question = 'QUESTION: ' + str(content_dict['Questions'][index])
            content = str(columns_dict['Content'][index+3])
            
            content = 'Not Applicable' if "How can we improve?" in content else content
            content = 'Not Applicable' if '<span class="columnContent"></span>' in content else content
                       
            all_html_text = all_html_text + '<br><br><br>' + question + '<br>How can we improve? ' + content
                    
    except Exception as e:
        print(f"Error: {e}")

    
    return all_html_text

if __name__ == "__main__":
    
    df_excel = pd.read_excel(excel_file,
                             sheet_name=excel_sheet_name,
                             dtype={'id':str,'score':str,'total_possible_score':str,'referrer':str,'created_at':str,'survey_id':str})
    
    df_excel = df_excel.replace(np.nan, None)
                           
    for i,row in df_excel.iterrows():
        id = row["id"]	
        country = row["country"]	
        industry = row["industry"]	
        questions = row["questions"]	
        score = row["score"]	
        total_possible_score = row["total_possible_score"]	
        referrer = str(row["referrer"])
        report_url = row["report_url"]	
        created_at = row["created_at"]	
        survey_id = row["survey_id"]
        
        print(f"working on: {report_url}")
        
        all_html_text = get_html_text(report_url)
        file_name = get_file_name(report_url)
            
        
        cabecera_pdf = ""
        
        cabecera_pdf = cabecera_pdf + "<h1>Modern Slavery Benchmarking Tool</h1>"
        cabecera_pdf = cabecera_pdf + "<h2>Performance Results and Recommendations</h2>"
        
        cabecera_pdf = cabecera_pdf + '<hr>'
        
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">ID: </span>' + id + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Country: </span>' + country + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Industry: </span>' + industry + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Score: </span>' + score + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Total possible score: </span>' + total_possible_score + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Referrer: </span>' + referrer + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Report URL: </span>' + '<a href="' + report_url + '">' + report_url + '</a>' + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Created at: </span>' + created_at + '</p>'
        cabecera_pdf = cabecera_pdf + '<p><span class="thick">Survery ID: </span>' + survey_id + '</p>'
        
        cabecera_pdf = cabecera_pdf + '<hr>'
        
        all_html_text = cabecera_pdf  + all_html_text
        
        pdfkit.from_string(all_html_text, 'pdf_surveys_recommendations/'+file_name + '.pdf', options=options, css = css)
            

    print('\nDONE!')