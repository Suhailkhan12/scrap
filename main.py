from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import json


res = requests.get('https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1681037522&sprefix=ba%2Caps%2C283&ref=sr_pg_1')

print(res)

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1681037522&sprefix=ba%2Caps%2C283&ref=sr_pg_1")


with open("data.json","w") as f:
    json.dump([],f)

def write_json(new_data, filename="data.json"):
    with open(filename,'r+') as file:
        #first we load existing data in dixtionery
        file_data = json.load(file)
        #join new data with file data inside emp details
        file_data.append(new_data)
        #sets file,s current position at offset.
        file.seek(0)
        #convert bachk to json.
        json.dump(file_data, file, indent = 4)


i=0
while i<=1:
    try:
        element = WebDriverWait(driver,10).until(EC.presence_of_element_located(
            (By.XPATH,'//div[@data-component-type="s-search-result"]')))

        elem_list = driver.find_element(By.CSS_SELECTOR,"div.sg-col-20-of-24.s-matching-dir.sg-col-16-of-20.sg-col.sg-col-8-of-12.sg-col-12-of-16")


        items = elem_list.find_elements(By.XPATH,'//div[@data-component-type="s-search-result"]')
        
        print(len(items))
        print("\n")
        print("new entry")
        print("\n")

        for item in  items:
            wait = element = WebDriverWait(driver,10).until(EC.presence_of_element_located(
            (By.CLASS_NAME,"a-size-medium.a-color-base.a-text-normal")))

            title = item.find_element(By.CLASS_NAME,"a-size-medium.a-color-base.a-text-normal").text
            
            price ="none"
            
            img="no image"

            star="None"

            link="none"

            try:
                price = item.find_element(By.CLASS_NAME,"a-price-whole").text
            except:
                pass

            try:
                img=item.find_element(By.CSS_SELECTOR,".s-image").get_attribute("src")
            except:
                pass

            try:
                star = item.find_element(By.CSS_SELECTOR,".a-size-base").text
            except:
                pass

            try:
                link = item.find_element(By.CLASS_NAME,"a-link-normal.s-underline-text.s-underline-link-text.s-link-style.a-text-normal").get_attribute("href")
            except:
                pass

            # print("title:-> "+title)
            # print('price:-> '+price)
            # print('img:-> '+img)
            # print('star out of 5-> '+star)
            # print('product ->' + link + "\n")

            write_json({
                "title":title+str(i),
                "link":link,
                "price":'Rs ' + price,
                "rating":star
            })
        
        btn = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME,"s-pagination-next")))
        driver.find_element(By.CLASS_NAME,"s-pagination-next").click()
    except Exception as e:
        print(e,"main error")
        isNextDisabled= True
    i=i+1