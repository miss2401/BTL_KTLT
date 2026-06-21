import Tao_tai_khoan as TTK
import Dang_nhap as DN

while True:
    user_input = input("1.Dang nhap \n2.Tao tai khoan \n3.Thoat \nNhập lựa chọn: ").strip()
    try:
        answer = int(user_input)
    except ValueError:
        print("Lua chon khong hop le! Vui long nhap 1, 2 hoac 3.")
        continue
    if answer not in [1, 2, 3]:
        print("Lua chon khong hop le! Vui long nhap 1, 2 hoac 3.")
        continue
    match answer:
        case 1:
            DN.Dang_nhap()
        case 2:
            TTK.Tao_tai_khoan()
        case 3:
            print("Thoat thanh cong.")
            break
