import datetime
import os
import subprocess
import uuid
import webbrowser
import requests

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    pass

# Cấu hình Supabase của cậu
SUPABASE_URL = "https://ssisxkimxgqkizomskar.supabase.co/rest/v1"
PUBLISHABLE_KEY = "sb_publishable_Y-gjOOHyzaGi3VepudvfmA_qzdDJsh4"

HEADERS = {
    "apikey": PUBLISHABLE_KEY,
    "Authorization": f"Bearer {PUBLISHABLE_KEY}",
    "Content-Type": "application/json",
    "Prefer": "return=representation",
}

def get_hwid():
  try:
    cmd = "wmic csproduct get uuid"
    hwid = (
        subprocess.check_output(cmd, shell=True)
        .decode(encoding="utf-8", errors="ignore")
        .split("\n")[1]
        .strip()
    )
    return hwid
  except Exception:
    return str(uuid.getnode())

def verify_license(user_key):
  hwid = get_hwid()
  try:
    # BƯỚC 1: Kiểm tra xem có phải Key của Admin không (Bảng admin_keys - Không khóa máy, không check status)
    res_admin = requests.get(
        f"{SUPABASE_URL}/admin_keys?license_key=eq.{user_key}", headers=HEADERS
    )
    admin_data = res_admin.json()
    
    if admin_data and len(admin_data) > 0:
      return True, "Đăng nhập thành công với quyền Admin (Key VIP vĩnh viễn)!"

    # BƯỚC 2: Nếu không phải key admin, kiểm tra trong bảng keys thông thường của khách
    response = requests.get(
        f"{SUPABASE_URL}/keys?license_key=eq.{user_key}", headers=HEADERS
    )
    data = response.json()

    if not data:
      return False, "Key không tồn tại trên hệ thống!"

    row = data[0]
    row_id = row["id"]
    db_hwid = row["hwid"]
    status = row["status"]

    if status == 1:
      if db_hwid == hwid:
        return True, "Hợp lệ! Chào mừng trở lại."
      else:
        return False, "Key này đã được kích hoạt trên một thiết bị khác!"
    else:
      update_headers = HEADERS.copy()
      update_payload = {"hwid": hwid, "status": 1}
      update_res = requests.patch(
          f"{SUPABASE_URL}/keys?id=eq.{row_id}",
          headers=update_headers,
          json=update_payload,
      )

      if update_res.status_code in [200, 204]:
        return True, "Kích hoạt thiết bị thành công!"
      else:
        return False, "Lỗi hệ thống khi trói buộc HWID!"
  except Exception as e:
    return False, f"Lỗi kết nối database: {e}"

def clear_screen():
  os.system("cls" if os.name == "nt" else "clear")

def check_license():
  while True:
    clear_screen()
    print(f"\n{Fore.CYAN}  ╔═══════════════════════════════════════════╗")
    print(f"  ║            🔐 HỆ THỐNG XÁC THỰC KEY       ║")
    print(f"  ╚═══════════════════════════════════════════╝{Style.RESET_ALL}")
    print(f"  {Fore.GREEN}[1] Nhập Key bản quyền (Khóa HWID / Key Admin)")
    print(f"  {Fore.YELLOW}[2] Lấy Key (Truy cập Web Get Key){Style.RESET_ALL}")
    print(f"  {Fore.RED}[0] Thoát chương trình{Style.RESET_ALL}")

    choice = input(f"\n  {Fore.YELLOW}👉 Lựa chọn của cậu: {Style.RESET_ALL}").strip()

    if choice == "1":
      user_key = input(
          f"\n  {Fore.YELLOW}🔑 Nhập Key của cậu: {Style.RESET_ALL}"
      ).strip()
      success, message = verify_license(user_key)

      if success:
        print(f"\n  {Fore.GREEN}✔ {message}{Style.RESET_ALL}")
        input("\n  Bấm Enter để vào tool...")
        return True
      else:
        print(f"\n  {Fore.RED}❌ {message}{Style.RESET_ALL}")
        input("\n  Bấm Enter để thử lại...")

    elif choice == "2":
      print(f"\n  {Fore.CYAN}🌐 Đang chuyển hướng đến trang lấy Key...{Style.RESET_ALL}")
      webbrowser.open("https://shopnamson.netlify.app/")
      input(
          f"\n  {Fore.YELLOW}💡 Lấy xong key thì bấm Enter để quay lại nhập..."
          f"{Style.RESET_ALL}"
      )

    elif choice == "0":
      return False

def show_menu():
  clear_screen()
  banner = f"""{Fore.CYAN}
███╗   ██╗ █████╗ ███╗   ███╗      ███████╗ ██████╗  █████╗ ███╗   ██║
████╗  ██║██╔══██╗████╗ ████║      ██╔════╝██╔═══██╗██╔══██╗████╗  ██║
██╔██╗ ██║███████║██╔████╔██║      ███████╗██║   ██║██║  ██║██╔██╗ ██║
██║╚██╗██║██╔══██║██║╚██╔╝██║      ╚════██║██║   ██║██║  ██║██║╚██╗██║
██║ ╚████║██║  ██║██║ ╚═╝ ██║      ███████║╚██████╔╝╚█████╔╝██║ ╚████║
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝     ╚═╝      ╚══════╝ ╚══════╝  ╚══════╝╚═╝  ╚═══╝
{Style.RESET_ALL}"""

  print(banner)
  print(
      f"  {Fore.MAGENTA}═══════════════════════════{Fore.CYAN} NAM SƠN TOOL"
      f" {Fore.MAGENTA}═══════════════════════════{Fore.CYAN}"
  )
  print(f"  {Fore.CYAN}🌐 STATUS    : {Fore.GREEN}SAFE & SECURE")
  print(
      f"  {Fore.MAGENTA}════════════════════════════════════════════════════════════════{Style.RESET_ALL}"
  )

  print(f"\n  {Fore.CYAN}MENU OPTIONS:")

  options = [
      "KIỂM TRA THÔNG TIN LIÊN KẾT",
      "LIÊN KẾT EMAIL",
      "HỦY LIÊN KẾT EMAIL",
      "THAY ĐỔI EMAIL LIÊN KẾT",
      "HỦY YÊU CẦU LIÊN KẾT",
      "LẤY ACCESS TOKEN",
      "THU HỒI ACCESS TOKEN",
      "XEM LỊCH SỬ ĐĂNG NHẬP",
      "KIỂM TRA CÁC TÀI KHOẢN ĐÃ LIÊN KẾT",
      "THÔNG TIN CHỦ SỞ HỮU",
      "EXIT",
  ]

  for i, opt in enumerate(options):
    idx = "0" if i == len(options) - 1 else str(i + 1)
    print(f"  {Fore.MAGENTA}✿ {Fore.CYAN}[{idx}] {Fore.WHITE}{opt}")

if check_license():
  while True:
    show_menu()
    choice = input(
        f"\n  {Fore.YELLOW}👉 Nhập lựa chọn của cậu: {Style.RESET_ALL}"
    ).strip()

    if choice == "1":
      print(
          f"\n  {Fore.GREEN}➔ Đang kiểm tra thông tin liên kết...{Style.RESET_ALL}"
      )
      input("\n  Bấm Enter để tiếp tục...")
    elif choice == "0" or choice.lower() == "exit":
      print(f"\n  {Fore.RED}👋 Thoát công cụ thành công!{Style.RESET_ALL}")
      break
    else:
      print(f"\n  {Fore.RED}❌ Lựa chọn không hợp lệ!{Style.RESET_ALL}")
      input("\n  Bấm Enter để thử lại...")
