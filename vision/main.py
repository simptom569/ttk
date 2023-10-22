import pytesseract
import easyocr
import fitz
import json
import cv2
import re
import os

path_parts = [os.getcwd(), 'tesseract', 'tesseract.exe']
path = os.path.join(*path_parts)
raw_path = r'' + path
pytesseract.pytesseract.tesseract_cmd = raw_path



def pdf_to_jpg(pdf_path, output_folder):
    doc = fitz.open(pdf_path)
    # Загружаем только первую страницу
    page = doc.load_page(0)
    # Рендерим страницу в пиксельное изображение (масштаб x2)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2))
    print(1)
    pix.save(f"{output_folder}/page_1.jpg")


def is_image_or_pdf(file_path):
    extension = os.path.splitext(file_path)[1].lower()
    if extension in ['.png', '.jpg', '.jpeg']:
        return False
    elif extension == '.pdf':
        return True
    else:
        raise ValueError(f"Unknown file extension: {extension}")
    

def contains_symbols(image_path, symbols="<<<"):
    # Создаем экземпляр для распознавания
    reader = easyocr.Reader(['ru'])

    # Распознаем текст на изображении
    results = reader.readtext(image_path)

    # Объединяем весь распознанный текст в одну строку
    full_text = ' '.join([item[1] for item in results])

    # Проверяем, содержит ли текст искомые символы
    return symbols in full_text


#============================= ДЛЯ ПАСПОРТА ===============================#
def correct_misreadings(text):
    # Замена некорректно распознанных символов
    corrections = {
        'A': 'А',
        'B': 'Б',
        'V': 'В',
        'G': 'Г',
        'D': 'Д',
        'E': 'Е',
        '2': 'Ё',
        'J': 'Ж',
        'Z': 'З',
        'I': 'И',
        'Q': 'Й',
        'K': 'К',
        'L': 'Л',
        'M': 'М',
        'N': 'Н',
        'O': 'О',
        'P': 'П',
        'R': 'Р',
        'S': 'С',
        'T': 'Т',
        'U': 'У',
        'F': 'Ф',
        'H': 'Ч',
        'C': 'Ц',
        '3': 'Ч',
        '4': 'Ш',
        'W': 'Щ',
        'X': 'Ъ',
        'Y': 'Ы',
        '9': 'Ь',
        '6': 'Э',
        '7': 'Ю',
        '8': 'Я',
        '0': 'О'
    }

    for wrong_char, correct_char in corrections.items():
        text = text.replace(wrong_char, correct_char)

    return text

def save_to_json(data, filename='result.json'):
    """Сохраняет данные в JSON-файл."""
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def recognize_data(image_path):
    reader = easyocr.Reader(['ru'])
    
    # Первое сканирование для ФИО
    results_FIO = reader.readtext(image_path, allowlist='1234567890QWERTYUIOPASDFGHJKLZXCVBNM<')
    full_text_FIO = ' '.join([detection[1] for detection in results_FIO])
    
    # Извлечение Фамилии, Имени и Отчества
    match_FIO = re.search(r'RUS(?P<last_name>[A-Z0-9]+)<<{0,1}(?P<first_name>[A-Z0-9]+)<(?P<surname>[A-Z0-9]+)<<<', full_text_FIO)

    # Поворот изображения
    image = cv2.imread(image_path)
    rotated_image = cv2.transpose(image)
    rotated_image = cv2.flip(rotated_image, flipCode=0)
    cv2.imwrite('rotated_image.jpg', rotated_image)

    # Второе сканирование для серии и номера паспорта
    results_passport = reader.readtext('rotated_image.jpg', allowlist='1234567890')
    full_text_passport = ''.join([detection[1] for detection in results_passport[:3]])  # Берем первые 3 строки
    
    if match_FIO:
        data = match_FIO.groupdict()
        for key, value in data.items():
            data[key] = correct_misreadings(value)
        
        data["series_number"] = full_text_passport
        data["type"] = "pasport"
        
        # Сохранение данных в JSON-файл
        save_to_json(data)
        print(f"Данные сохранены в файл result.json")
    else:
        print("Не удалось извлечь ФИО.")
#============================= ДЛЯ ПАСПОРТА ===============================#


#============================= ДЛЯ БИЛЕТОВ ================================#
def recognize_text_with_easyocr(image_path):
    reader = easyocr.Reader(['ru'])
    results = reader.readtext(image_path, allowlist='1234567890АБВГДЕЖИЙКЛМНОПРСЙУЧШЫЬЭЯабвгдежийклмнопрсйучшыьэя')
    # results = reader.readtext(image_path, allowlist='йцукенгшщзхъфывапролджэячсмитьбюЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ')

    # Извлечение текста
    recognized_texts = [detection[1] for detection in results]

    data = {}
    for i in range(len(recognized_texts) - 2):
        train_candidate = recognized_texts[i].replace('О', '0')  # Замена возможного неверного символа
        if re.match(r"^\d{3}[А-Яа-я]{0,1}$", train_candidate) and \
           re.match(r"^\d{2}$", recognized_texts[i+1]) and \
           re.match(r"^\d{3}$", recognized_texts[i+2]):
            
            data["train"] = train_candidate
            data["van"] = recognized_texts[i+1]
            data["place"] = recognized_texts[i+2]
            data["type"] = "ticket"
            break

    if not data:
        print("Не удалось найти все необходимые строки.")
        return

    # Сохраняем результат в JSON
    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
#============================= ДЛЯ БИЛЕТОВ ================================#

def get_text(file_path) -> dict:
    output_folder = 'src/img'
    if is_image_or_pdf(file_path):
        pdf_to_jpg(file_path, output_folder)
    else:
        if contains_symbols(file_path):
            # Паспорт
            recognize_data(file_path)
        else:
            # Билет
            recognize_text_with_easyocr(file_path)
    
    with open("result.json", encoding="utf-8") as f:
        data = json.load(f)
        return data