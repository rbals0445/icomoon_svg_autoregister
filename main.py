from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.keys import Keys
import os
import chromedriver_autoinstaller
import zipfile
import time
import re

# TODO
# python3 main.py로 실행하는경우
# multicolor일때 search가 너무 늦음.. +1하는 방식이라 그런것같음.

# Issue
# headless mode로하면 스크롤이 안움직인다. 800 x 600 size여서, 내가 클릭하려는 아이콘 근처에 버튼이 있으면 그게 대신 눌려버리는 문제들이 발생했다.
# window_size를 변경해서 해결했지만, 스크롤을 움직일 수 있는게 좀 더 근본적 해결일것 같음
chromedriver_autoinstaller.install()

## const 영역
WEB_URL = "https://icomoon.io/app/#/projects"
PROJECT_IMPORT_DIV = '/html/body/div[4]/div/div[3]/div[2]/div'
IMPORT_PROJECT_BUTTON = '/html/body/div[4]/div/div[3]/div[2]/div/mi-file/input'

IMPORT_ICON_DIV = '//*[@id="file"]'
IMPORT_ICON_BUTTON = '//*[@id="file"]/mi-file/input'

IMPORT_FILE_NAME = 'selection.json' # selection.json가 보통 기본 파일명임
LOAD_PROJECT_BUTTON = '/html/body/div[4]/div/div[3]/div[1]/ul/li[2]/fieldset/button[3]'

GET_FONT_BUTTON = '/html/body/div[4]/div[1]/div[2]/div[3]/div/a[2]' # 파일 추가후에 누르는 Fonts 버튼

FONTS_DOWNLOAD_BUTTON = '/html/body/div[4]/div[2]/div/div[2]/div/span/button[1]' # 폰트 다운로드 버튼

SHOW_LIGATURE_BUTTON = '//*[@id="toolbar"]/div[2]/div[2]/div/label[2]' #Ligature button 클릭

## 기타
BASE_PATH = os.path.dirname(__file__)
FOLDER_NAME_FOR_ADDITION = "newfiles" # 새로 넣을 이미지를 가지고 있는 폴더 이름

## 함수
def setLigatureName(wait) :    
    wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='glyphSet0']/div[1]/div[1]/div/div/span[2]"))) # div버튼 나왔는지 확인
    x = 1
    while(True) :
        try:
            ligatureNameXpath = "//*[@id='glyphSet0']/div["+str(x)+"]/div[1]/div/div/span[2]"
            ligatureInputXpath = "//*[@id='glyphSet0']/div["+str(x)+"]/div[2]/div[2]/label/input" 
            ligatureName = driver.find_element(By.XPATH, ligatureNameXpath).text
            ligatureName = re.sub('[^0-9a-zA-Z_]', '', ligatureName)
            
            driver.find_element(By.XPATH, ligatureInputXpath).send_keys(ligatureName)            
            x += 1
        except ElementNotInteractableException :
            x += 1
        except Exception as e:
            break

def iterateChildSvgComponents(wait) : # 추가된 컴포넌트를 클릭해주는 함수
    
    wait.until(
            EC.visibility_of_element_located((By.XPATH, "//*[@id='set0']/mi-box-selector/div/mi-box[1]"))) # div버튼 나왔는지 확인

    for item in driver.find_elements_by_tag_name('mi-box') :
        if not item.is_selected() :
            item.click()
    
def addMultipleFiles(folderName) : # headless 정상작동
    dirList = os.listdir(folderName)    
    addedString = ""

    for item in dirList :
        addedString += os.path.join(folderName,item+"\n")
        
    return addedString[0:-1]

def getBrowserDriver() :    
    op = webdriver.ChromeOptions()
    #op.add_argument('--disable-dev-shm-usage')
    #op.add_argument('--no-proxy-server') 
    #op.add_argument("--proxy-server='direct://'");
    #op.add_argument("--proxy-bypass-list=*");
    #op.add_argument("--start-maximized")    
    op.add_argument("window-size=2560,1440")
    op.add_argument('headless')
    op.add_argument("disable-gpu") 
    p = {"download.default_directory": BASE_PATH, "safebrowsing.enabled":False, 'download.prompt_for_download': False }
    op.add_experimental_option("prefs", p)
    
    driver = webdriver.Chrome(options=op)    
    print(driver.get_window_size())
    
    return driver;

def checkFileDownloaded() :
    sec = 0
    while sec < 20 :
        time.sleep(1)
        for fname in os.listdir(BASE_PATH) :
            _,ext = os.path.splitext(fname)
            if ext == ".zip" :
                return fname
        sec += 1
        
    return False
        
def unzip() :
    zipFileName = checkFileDownloaded()
    
    fileName = os.path.join(BASE_PATH,zipFileName)
    
    with zipfile.ZipFile(fileName,"r") as zip_ref:
        zip_ref.extractall(os.path.join(BASE_PATH,"results"))
    
    if os.path.isfile(fileName): # zip file 삭제
        os.remove(fileName)

def processRequests() : # 최종 실행 함수
    try:
        wait = WebDriverWait(driver, 30)
        
        wait.until(
            EC.visibility_of_element_located((By.XPATH, PROJECT_IMPORT_DIV)))
        
        TEST_FILENAME = os.path.join(BASE_PATH, IMPORT_FILE_NAME)
        

        driver.find_element(By.XPATH,IMPORT_PROJECT_BUTTON).send_keys(TEST_FILENAME) # input tag 찾아서 파일 넣음.
        
        wait.until(
            EC.element_to_be_clickable((By.XPATH, LOAD_PROJECT_BUTTON))).click() # Load button click
        
        wait.until(
            EC.visibility_of_element_located((By.XPATH, IMPORT_ICON_DIV))) # Import Icon 버튼 체크
        
        addedString = addMultipleFiles(os.path.join(BASE_PATH, FOLDER_NAME_FOR_ADDITION))
        #print(addedString)
        driver.find_element(By.XPATH,IMPORT_ICON_BUTTON).send_keys(addedString) # folder안에 있는 파일들 업로드 완료
        
        wait.until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="set0"]/mi-box-selector/div'))) # div버튼 나왔는지 확인
            
        iterateChildSvgComponents(wait) 
        
        wait.until(
            EC.element_to_be_clickable((By.XPATH, GET_FONT_BUTTON))).click() # Click Font Button
        
        wait.until(
            EC.element_to_be_clickable((By.XPATH, SHOW_LIGATURE_BUTTON))) # LigatureBtn 나올때까지 대기
        
        elem = driver.find_element(By.XPATH, SHOW_LIGATURE_BUTTON)        
        if not elem.is_selected() :
            elem.click()
        
        setLigatureName(wait) # ligature 채움
        
        
        wait.until(
            EC.element_to_be_clickable((By.XPATH, FONTS_DOWNLOAD_BUTTON))).click() # download button click
        
        unzip()
        
    finally:
        print("Update Finished")
        driver.close()
        
## 실행 스크립트
driver = getBrowserDriver()
driver.get(WEB_URL)
processRequests()




    
    






