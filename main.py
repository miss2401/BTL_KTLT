import create_user as CS
answer = int(input("1.Dang nhap \n2.Tao tai khoan \n3.Thoat \nNhập lựa chọn: "))
match answer:
    case 1:
        pass
    case 2:
        sdt = input("So dien thoai: ")
        while(len(sdt) != 10 or CS.check_number(sdt)):
            sdt = input("Nhap lai so dien thoai: ")
        password = input("Mat khau: ")
        while(len(password) < 8 or CS.check_password(password)):
            print("Mat khau phai co it nhat 8 ki tu, co ket hop giua chu cai in hoa, chu so va ki tu dac biet")
            password = input("Nhap lai mat khau: ")
        print("Tao tai khoan thanh cong")
    case _:
        pass