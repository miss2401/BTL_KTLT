import Tao_tai_khoan as CS
import Dang_nhap as LS

while True:
    answer = int(input("1.Dang nhap \n2.Tao tai khoan \n3.Thoat \nNhập lựa chọn: "))
    if answer not in [1, 2, 3]:
        print("Lua chon khong hop le! Vui long nhap 1, 2 hoac 3.")
        continue
    match answer:
        case 1:
            LS.Dang_nhap()
        case 2:
            CS.Tao_tai_khoan()
        case 3:
            print("Thoat thanh cong.")
            break