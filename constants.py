import os   
import sys
## const 영역
WEB_URL = "https://icomoon.io/app/#/projects"
PROJECT_IMPORT_DIV = '/html/body/div[4]/div/div[3]/div[2]/div'
IMPORT_PROJECT_BUTTON = '/html/body/div[4]/div/div[3]/div[2]/div/mi-file/input'

IMPORT_ICON_DIV = '//*[@id="file"]'
IMPORT_ICON_BUTTON = '//*[@id="file"]/mi-file/input'

NEW_PROJECT_BUTTON = '/html/body/div[4]/div/div[3]/div[2]/button'

GET_FONT_BUTTON = '/html/body/div[4]/div[1]/div[2]/div[2]/div/a[2]' # 파일 추가후에 누르는 Fonts 버튼

FONTS_DOWNLOAD_BUTTON = '/html/body/div[4]/div[2]/div/div[2]/div/span/button[1]' # 폰트 다운로드 버튼

SHOW_LIGATURE_BUTTON = '//*[@id="toolbar"]/div[2]/div[2]/div/label[2]' #Ligature button 클릭

NEW_PROJECT_LOAD_BUTTON = '/html/body/div[4]/div/div[3]/div[1]/ul/li[2]/fieldset/button[3]' # 새 프로젝트 load 버튼

DRAWER_BUTTON = '//*[@id="setH0"]/button' # select_all 누르기 위한 버튼
SELECT_ALL_BUTTON = '//*[@id="setH0"]/ul/li[5]/button[1]' 
## 기타
FOLDER_NAME_FOR_ADDITION = "newfiles" # 새로 넣을 이미지를 가지고 있는 폴더 이름

if getattr(sys, 'frozen', False):
    BASE_PATH = os.path.dirname(sys.executable)
elif __file__:
    BASE_PATH = os.path.dirname(__file__)
    