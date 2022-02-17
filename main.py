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
import constants as const
# TODO
# python3 main.py로 실행하는경우
# multicolor일때 search가 너무 늦음.. +1하는 방식이라 그런것같음.

# Issue
# headless mode로하면 스크롤이 안움직인다. 800 x 600 size여서, 내가 클릭하려는 아이콘 근처에 버튼이 있으면 그게 대신 눌려버리는 문제들이 발생했다.
# window_size를 변경해서 해결했지만, 스크롤을 움직일 수 있는게 좀 더 근본적 해결일것 같음
chromedriver_autoinstaller.install()

## 함수
def setLigatureName() :        
    isElementPresent("//*[@id='glyphSet0']/div[1]/div[1]/div/div/span[2]")
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
    
def addMultipleFiles(folderName) : # headless 정상작동
    dirList = os.listdir(folderName)    
    addedString = ""

    for item in dirList :
        addedString += os.path.join(folderName,item+"\n")
        
    return addedString[0:-1]

def getBrowserDriver() :    
    op = webdriver.ChromeOptions()
    op.add_argument('--disable-dev-shm-usage')
    op.add_argument('--no-proxy-server') 
    op.add_argument('headless')
    op.add_argument("disable-gpu") 
    p = {"download.default_directory": const.BASE_PATH, "safebrowsing.enabled":False, 'download.prompt_for_download': False }
    op.add_experimental_option("prefs", p)
    
    driver = webdriver.Chrome(options=op)    
    
    return driver;

def checkFileDownloaded() :
    sec = 0
    while sec < 20 :
        time.sleep(1)
        for fname in os.listdir(const.BASE_PATH) :
            _,ext = os.path.splitext(fname)
            if ext == ".zip" :
                return fname
        sec += 1
        
    return False
        
def unzip() :
    zipFileName = checkFileDownloaded()
    
    fileName = os.path.join(const.BASE_PATH,zipFileName)
    
    with zipfile.ZipFile(fileName,"r") as zip_ref:
        zip_ref.extractall(os.path.join(const.BASE_PATH,"results"))
    
    if os.path.isfile(fileName): # zip file 삭제
        os.remove(fileName)
        
def isElementClickable(PATH) : # true -> click, false -> exit
    try :
        wait.until(
            EC.element_to_be_clickable((By.XPATH, PATH))).click()
    except Exception as e :
        print(PATH,e)
        return;
    
def isElementPresent(PATH) :
    try :
        elem = wait.until(
            EC.presence_of_element_located((By.XPATH, PATH)))
        return elem
    except Exception as e :
        print(PATH,e)
        return;

def processRequests() : # 최종 실행 함수
    try:
        isElementClickable(const.NEW_PROJECT_BUTTON) # 새 프로젝트 버튼 클릭
        isElementClickable(const.NEW_PROJECT_LOAD_BUTTON) # 프로젝트에서 Load 버튼 클릭
        isElementPresent(const.IMPORT_ICON_DIV) # Import Icon 버튼 체크
        
        addedString = addMultipleFiles(os.path.join(const.BASE_PATH, const.FOLDER_NAME_FOR_ADDITION))
        
        driver.find_element(By.XPATH,const.IMPORT_ICON_BUTTON).send_keys(addedString) # folder안에 있는 파일들 업로드 완료
                           
        isElementPresent(const.DRAWER_BUTTON).click() # Drawbtn 찾아서 클릭
        isElementPresent(const.SELECT_ALL_BUTTON).click() # 전체 선택버튼
        isElementPresent(const.GET_FONT_BUTTON).click() # Click Font Button
        isElementClickable(const.SHOW_LIGATURE_BUTTON) # LigatureBtn 나올때까지 대기
        setLigatureName() # ligature 채움
        isElementClickable(const.FONTS_DOWNLOAD_BUTTON)
            
        unzip()   
    finally:
        print("Update Finished")
        driver.close()
        
## 실행 스크립트
driver = getBrowserDriver()
driver.get(const.WEB_URL)
wait = WebDriverWait(driver, 30)
processRequests()




    
    






