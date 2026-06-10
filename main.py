import create_user as CS
import login_user as LS

while True:
    try:
        answer = int(input("1.Dang nhap \n2.Tao tai khoan \n3.Thoat \nNhập lựa chọn: "))
        if answer not in [1, 2, 3]:
            print("Lua chon khong hop le! Vui long nhap 1, 2 hoac 3.")
            continue
        match answer:
            case 1:
                LS.dang_nhap()
            case 2:
                CS.Create_user()
            case 3:
                print("Thoat thanh cong.")
                break
    except ValueError:
        print("Vui long nhap mot so nguyen!")