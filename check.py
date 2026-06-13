def Kiem_tra_so(arr):
    for i in arr:
        if(i < '0' or i > '9'):
            return 1
    return 0

def Kiem_tra_ten(arr):
    for i in arr:
        is_lowercase = (i >= 'a' and i <= 'z')
        is_uppercase = (i >= 'A' and i <= 'Z')
        is_space = (i == ' ')
        if not (is_lowercase or is_uppercase or is_space):
            return 1
    return 0

def Kiem_tra_email(email):
    if not email or len(email) == 0:
        return 1
    if "@" in email:
        return 1
    for i in email:
        is_lowercase = (i >= 'a' and i <= 'z')
        is_uppercase = (i >= 'A' and i <= 'Z')
        is_digit = (i >= '0' and i <= '9')
        is_valid_char = (i in '._-')
        if not (is_lowercase or is_uppercase or is_digit or is_valid_char):
            return 1
    return 0

def Kiem_tra_sdt_ton_tai(sdt):
    try:
        database = BD()
        danh_sach_tk = database._doc_file()
        for tk in danh_sach_tk:
            if tk.so_dien_thoai == sdt:
                return 1
        return 0
    except:
        return 0
def check_mat_khau(arr):
    co_chu_thuong = False
    co_chu_hoa = False
    co_so = False
    co_ky_tu_dac_biet = False
    for i in arr:
        if(i >= 'a' and i <= 'z'):
            co_chu_thuong = True
        elif(i >= '0' and i <= '9'):
            co_so = True
        elif(i >= 'A' and i <= 'Z'):
            co_chu_hoa = True
        elif(i >= '!' and i <= '@'):
            co_ky_tu_dac_biet = True
    if(co_chu_thuong and co_chu_hoa and co_so and co_ky_tu_dac_biet):
        return 0
    else:
        return 1