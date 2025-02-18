import re
import unidecode

def generate_slug(text): 
    # Loại bỏ dấu tiếng Việt, chuyển về ASCII
    vb = unidecode.unidecode(text)
    
    # Chuyển thành chữ thường
    chuthuong = vb.lower()
    
    # Thay khoảng trắng và dấu gạch ngang thừa thành một dấu gạch ngang duy nhất
    bokhoangtrang = re.sub(r'\s+', '-', chuthuong)  # Thay khoảng trắng bằng dấu '-'
    bohaigach = re.sub(r'-+', '-', bokhoangtrang)   # Xóa các dấu gạch ngang thừa

    # Loại bỏ các ký tự không phải là chữ hoặc số
    kytu = re.sub(r'[^a-z0-9-]', '', bohaigach)  # Chỉ giữ lại chữ cái, số và dấu '-'

    # Loại bỏ dấu gạch ngang ở đầu/cuối nếu có
    return kytu.strip('-')

