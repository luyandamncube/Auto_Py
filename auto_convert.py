from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
import sys
import os
import time
import platform


'''
    TODO:
        - Add wait systme for download
        - rename files in output
'''


def readData(argv):
    errorflag = True
    try:
        if (len(argv) != 3):
            print('USAGE: python auto_convert.py .\input_directory .\output_directory')
            exit()
        elif (os.path.isfile(argv[1]) or len(argv) != 3):
            print('ERROR: first argument should be a directory\nUSAGE: python auto_convert.py .\input_directory .\output_directory')
            exit()
        elif (os.path.isfile(argv[2])):
            print('ERROR: second argument should be a directory\nUSAGE: python auto_convert.py .\input_directory .\output_directory')
            exit()
        print('Checking files...')
        for filename in os.listdir(argv[1]):
            if (not filename.endswith('.csv')): 
                print(f'[x] {filename}')
                errorflag = False
            else:
                print(f'[✓] {filename}')
    except AssertionError as error:
        print('Reading data could not be completed')
    finally:
        return(errorflag)
        
def configDriver(outputDirectory):
    driverName = 'chromedriver.exe'
    # try:
    outputDir = os.path.abspath(outputDirectory)
    options = Options()
    options.add_argument("--log-level=3")
        # Runs Chrome in headless mode.
    options.add_argument("--headless") 
    preferences = {'download.default_directory': outputDir}
    options.add_experimental_option("prefs",preferences)
    if (not os.path.isfile('./driver/'+driverName)):
        print(f'ERROR: driver {driverName} not found')
        exit()
    driver = webdriver.Chrome('./driver/chromedriver.exe',chrome_options=options)
    driver.maximize_window()
    driver.get('https://www.gpsvisualizer.com/convert_input')
    return(driver)
      
def blockAdverts(driver):
    # block ads
    # element = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@class='nonmobile_body']/table/tbody/tr/td[3]")
    # driver.execute_script("""var element = arguments[0];element.parentNode.removeChild(element);""", element)
    driver.execute_script("document.getElementById('header_strip').outerHTML = '';")
    driver.execute_script("document.getElementById('sidebar').outerHTML = '';")

def fillForm(driver):
    selectTextDataType = Select(driver.find_element_by_name('force_type'))
    selectTextDataType.select_by_visible_text('trackpoints')
    selectTextDelimeter = Select(driver.find_element_by_name('convert_delimiter'))
    selectTextDelimeter.select_by_visible_text('comma')
    selectTextDelimeter = Select(driver.find_element_by_name('units'))
    selectTextDelimeter.select_by_visible_text('Metric')
    driver.execute_script("document.getElementById('convert_add_course_checkbox').checked = true;")
    driver.execute_script("document.getElementById('convert_add_slope_checkbox').checked = true;")
    selectElevationModel = Select(driver.find_element_by_name('add_elevation'))
    selectElevationModel.select_by_visible_text('best available source')
    driver.execute_script("document.getElementById('advanced_options').style.display = 'block';")
    formTickmarkInterval = driver.find_element_by_name('tickmark_interval')
    formTickmarkInterval.send_keys('0.01')

def downloadOutput(driver):
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)
    blockAdverts(driver)
    downloadLink = driver.find_element_by_xpath("/html/body/table/tbody/tr/td[@class='nonmobile_body']/p[3]/a")
    downloadLink.click()

def convertData(index, inputDirectory, outputDirectory):
    inputDir = os.path.abspath(inputDirectory)
    inputFiles = os.listdir(inputDir)
    driver = configDriver(outputDirectory)
    blockAdverts(driver)
    uploadBox = driver.find_element_by_name("uploaded_file_1")
    if (platform.system() == 'Windows' ):
        escapeCharacter = '\\' 
    else:
        escapeCharacter = '//' 
    uploadBox.send_keys(inputDir + escapeCharacter + inputFiles[index])
    fillForm(driver)
    submitButton = driver.find_element_by_class_name('gpsv_submit').click()
    downloadOutput(driver)
    time.sleep(10)
    driver.close()

if __name__ == "__main__":
    argv = sys.argv
    isValid = readData(sys.argv)
    if (isValid == True):
        print('SUCCESS: Filecheck complete.\nConverting data...')
        try:
            inputFiles = os.listdir(argv[1])
            if (len(inputFiles) < 1):
                print("ERROR: no input files detected")
                exit()
            for index, value in enumerate(inputFiles):
                convertData(index, argv[1], argv[2])
            for item in os.listdir(argv[2]):
                if (item.endswith(".tmp") or item.endswith(".crdownload")):
                    os.remove(os.path.join(argv[2], item))
        except Exception as e:
            print(f'ERROR: {e}')
            exit() 
        
    else:
        print('ERROR: One or more files were not in csv format')
        exit()
    print('Conversion complete!')
    
    


