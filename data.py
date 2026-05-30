import os
import random

class TaiKhoan:
    #Khuôn mẫu cho đối tượng tài khoản người dùng
    def __init__(self, so_dien_thoai, ho_ten, mat_khau, email, cccd, so_tai_khoan, so_du=0, ma_pin=""):
        self.so_dien_thoai = str(so_dien_thoai)
        self.ho_ten = ho_ten
        self.mat_khau = mat_khau
        self.email = email
        self.cccd = cccd
        self.so_tai_khoan = str(so_tai_khoan)
        self.so_du = int(so_du)
        self.ma_pin = ma_pin


class BankDatabase:
    def __init__(self, db_file="data.json"):
        self.db_file = db_file
        # Nếu file chưa tồn tại hoặc rỗng, tạo một file mới với nội dung là một object JSON rỗng
        if not os.path.exists(self.db_file) or os.path.getsize(self.db_file) == 0:
            with open(self.db_file, "w", encoding="utf-8") as f:
                f.write("{}")

    def _doc_file(self):
        #Parse thủ công file JSON để tạo ra một mảng phẳng chứa các đối tượng tài khoản người dùng
        danh_sach_tk = []
        try:
            with open(self.db_file, "r", encoding="utf-8") as f:
                chuoi_json = f.read()
        except Exception:
            return danh_sach_tk

        tokens = []
        i = 0
        while i < len(chuoi_json):
            char = chuoi_json[i]
            
            # 1. Gặp " thì nhặt chuỗi ký tự bên trong"
            if char == '"':
                token_str = ""
                i += 1
                while i < len(chuoi_json) and chuoi_json[i] != '"':
                    token_str = token_str + chuoi_json[i]
                    i += 1
                tokens = tokens + [token_str]
                
            # 2. Gặp ký tự đặc biệt thì coi là một token riêng
            elif char in (':', '{', '}', ','):
                tokens = tokens + [char]
                
            # 3. Gặp số thì nhặt chuỗi số liên tiếp
            elif char in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                num_str = ""
                while i < len(chuoi_json) and chuoi_json[i] in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                    num_str = num_str + chuoi_json[i]
                    i += 1
                tokens = tokens + [num_str]
                continue
                
            i += 1

        # Trích xuất dữ liệu từ mảng tokens phẳng
        t = 0
        while t < len(tokens):
            # Tìm kiếm token là sđt (chuỗi 10 ký tự số)
            is_sdt = len(tokens[t]) == 10
            if is_sdt:
                for char in tokens[t]:
                    if char not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                        is_sdt = False
                        break
            
            # Nếu đúng là sđt và sau nó là dấu ':' và '{'
            if is_sdt and (t + 2 < len(tokens)) and tokens[t+1] == ':' and tokens[t+2] == '{':
                sdt = tokens[t]
                
                # Khởi tạo giá trị default
                ho_ten = mat_khau = email = cccd = so_tai_khoan = ma_pin = ""
                so_du = 0
                
                # Quét các cặp thuộc tính
                t = t + 3
                while t < len(tokens) and tokens[t] != '}':
                    
                    if t + 2 < len(tokens) and tokens[t+1] == ':':
                        key_con = tokens[t]
                        val_con = tokens[t+2]
                        
                        if key_con == "ho_ten": ho_ten = val_con
                        elif key_con == "mat_khau": mat_khau = val_con
                        elif key_con == "email": email = val_con
                        elif key_con == "cccd": cccd = val_con
                        elif key_con == "so_tai_khoan": so_tai_khoan = val_con
                        elif key_con == "ma_pin": ma_pin = val_con
                        elif key_con == "so_du": so_du = int(val_con)
                        
                        t = t + 3
                    else:
                        t = t + 1
                        
                #Tạo đối tượng tk và thêm vào mảng
                tk_moi = TaiKhoan(sdt, ho_ten, mat_khau, email, cccd, so_tai_khoan, so_du, ma_pin)
                danh_sach_tk = danh_sach_tk + [tk_moi]
            else:
                t = t + 1

        return danh_sach_tk

    def _ghi_file(self, danh_sach_tk):
        #Lắp ráp chuỗi json
        chuoi_json = "{\n"
        for i in range(len(danh_sach_tk)):
            tk = danh_sach_tk[i]
            user_str = (
                f'    "{tk.so_dien_thoai}": {{\n'
                f'        "ho_ten": "{tk.ho_ten}",\n'
                f'        "mat_khau": "{tk.mat_khau}",\n'
                f'        "email": "{tk.email}",\n'
                f'        "cccd": "{tk.cccd}",\n'
                f'        "so_tai_khoan": "{tk.so_tai_khoan}",\n'
                f'        "so_du": {tk.so_du},\n'
                f'        "ma_pin": "{tk.ma_pin}"\n'
                f'    }}'
            )
            if i == 0:
                chuoi_json = chuoi_json + user_str
            else:
                chuoi_json = chuoi_json + ",\n" + user_str

        chuoi_json = chuoi_json + "\n}"
        with open(self.db_file, "w", encoding="utf-8") as f:
            f.write(chuoi_json)

    def them_tai_khoan_moi(self, ho_ten, so_dien_thoai, mat_khau, email, cccd, ma_pin):
        danh_sach_tk = self._doc_file()

        #Kiểm tra trùng sđt
        for i in range(len(danh_sach_tk)):
            if danh_sach_tk[i].so_dien_thoai == str(so_dien_thoai):
                return False

        #Tạo số tài khoản không trùng lặp
        while True:
            stk_goi_y = str(random.randint(10000000, 99999999))
            trung_stk = False
            for i in range(len(danh_sach_tk)):
                if danh_sach_tk[i].so_tai_khoan == stk_goi_y:
                    trung_stk = True
                    break
            if not trung_stk:
                so_tai_khoan = stk_goi_y
                break

        #Thêm tài khoản mới
        tk_moi = TaiKhoan(so_dien_thoai, ho_ten, mat_khau, email, cccd, so_tai_khoan, 0, ma_pin)
        danh_sach_tk = danh_sach_tk + [tk_moi]
        
        self._ghi_file(danh_sach_tk)
        return so_tai_khoan

    def lay_thong_tin_user(self, so_dien_thoai):
        danh_sach_tk = self._doc_file()
        for i in range(len(danh_sach_tk)):
            if danh_sach_tk[i].so_dien_thoai == str(so_dien_thoai):
                return danh_sach_tk[i]
        return None
