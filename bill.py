from PIL import Image, ImageDraw, ImageFont
import os
from datetime import datetime

# Tạo thư mục nếu chưa tồn tại
output_dir = "picture_bill"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Cài đặt kích thước và màu sắc
width, height = 900, 700
background_color = (245, 245, 245)  # Xám nhạt làm nền
primary_color = (0, 0, 0)           # Đen
accent_color = (0, 51, 102)         # Xanh đậm
momo_color = (160, 0, 160)          # Tím Momo
bank_color = (0, 102, 0)            # Xanh lá ngân hàng
highlight_color = (230, 240, 255)   # Màu nền nhẹ cho tiêu đề

# Tạo ảnh mới
image = Image.new("RGB", (width, height), background_color)
draw = ImageDraw.Draw(image)

# Tải font chữ
try:
    font_title = ImageFont.truetype("arialbd.ttf", 30)  # Font tiêu đề lớn
    font_subtitle = ImageFont.truetype("arialbd.ttf", 20)  # Font phụ đề
    font_body = ImageFont.truetype("arial.ttf", 16)      # Font nội dung
except:
    font_title = ImageFont.load_default()
    font_subtitle = font_title
    font_body = font_title

# Lấy ngày giờ hiện tại
current_date = datetime.now().strftime("%d/%m/%Y")
current_time = datetime.now().strftime("%H:%M:%S")  # Thêm giờ phút giây cho file text
current_time_for_filename = datetime.now().strftime("%H%M%d%m%Y")
current_day = datetime.now().strftime("%d%m%Y")
current_month = datetime.now().strftime("%m%Y")
current_year = datetime.now().strftime("%Y")

# Nhập dữ liệu từ bàn phím
product_name = input("Nhập tên sản phẩm: ")
quantity = input("Nhập số lượng: ")
unit_price = input("Nhập đơn giá (VD: 15000000): ")

# Định dạng đơn giá và tổng cộng với dấu phẩy và thêm "VND"
unit_price_formatted = f"{int(unit_price):,d} VND"
total_price = int(unit_price) * int(quantity)
total_price_formatted = f"{total_price:,d} VND"

# Nội dung hóa đơn với dữ liệu từ input
invoice_content = [
    ("HÓA ĐƠN BÁN HÀNG", font_title, accent_color),
    (f"Ngày: {current_date}", font_body, primary_color),
    (f"Sản phẩm: {product_name}", font_body, primary_color),
    (f"Số lượng: {quantity}", font_body, primary_color),
    (f"Đơn giá: {unit_price_formatted}", font_body, primary_color),
    (f"TỔNG CỘNG: {total_price_formatted}", font_subtitle, (200, 0, 0)),
]

# Vẽ nền nhẹ cho tiêu đề
draw.rectangle([(20, 20), (width-20, 120)], fill=highlight_color, outline=accent_color, width=2)

# Vẽ nội dung hóa đơn (căn giữa) với padding
y_position = 30
padding = 30
for text, font, color in invoice_content:
    text_width = draw.textlength(text, font=font)
    x_position = (width - text_width) // 2
    draw.text((x_position, y_position), text, font=font, fill=color)
    y_position += font.getbbox(text)[3] + padding

# Thông tin thanh toán
bank_info = [
    ("THANH TOÁN QUA NGÂN HÀNG", font_subtitle, bank_color),
    ("Ngân hàng: Vietcombank", font_body, primary_color),
    ("Số TK: 0311000742731", font_body, primary_color),
    ("Chủ TK: Dinh Thi Hiep", font_body, primary_color),
]

momo_info = [
    ("THANH TOÁN QUA MOMO", font_subtitle, momo_color),
    ("Số điện thoại: 0866005531", font_body, primary_color),
    ("Chủ TK: Nguyen Ngoc Truong", font_body, primary_color),
]

# Vẽ hai cột thông tin thanh toán nằm ngang hàng
y_payment_start = y_position + 40
column_width = width // 2 - 60
column_height = 200

# Cột ngân hàng
x_bank = 40
draw.rectangle([(x_bank-10, y_payment_start-10), (x_bank + column_width, y_payment_start + column_height)], 
               fill=(235, 245, 235), outline=bank_color, width=1)
y_position = y_payment_start
for text, font, color in bank_info:
    draw.text((x_bank, y_position), text, font=font, fill=color)
    y_position += font.getbbox(text)[3] + padding

# Cột Momo
x_momo = width // 2 + 20
draw.rectangle([(x_momo-10, y_payment_start-10), (x_momo + column_width, y_payment_start + column_height)], 
               fill=(245, 235, 245), outline=momo_color, width=1)
y_position = y_payment_start
for text, font, color in momo_info:
    draw.text((x_momo, y_position), text, font=font, fill=color)
    y_position += font.getbbox(text)[3] + padding

# Vẽ khung viền trang trí với bóng
draw.rectangle([(15, 15), (width-15, height-15)], outline=accent_color, width=3)
draw.rectangle([(20, 20), (width-20, height-20)], outline=(150, 150, 150), width=1)

# Thêm dòng chữ "CẢM ƠN QUÝ KHÁCH!" phía dưới, căn giữa
thank_you_text = "CẢM ƠN QUÝ KHÁCH!"
thank_you_font = font_subtitle
thank_you_color = accent_color
text_width = draw.textlength(thank_you_text, font=thank_you_font)
x_position = (width - text_width) // 2
y_thank_you = y_payment_start + column_height + 40
draw.text((x_position, y_thank_you), thank_you_text, font=thank_you_font, fill=thank_you_color)

# Lưu ảnh với tên file theo giờ phút ngày tháng năm
output_filename = f"invoice_{current_time_for_filename}.png"
output_path = os.path.join(output_dir, output_filename)
image.show()
image.save(output_path)

# Ghi hóa đơn vào file text duy nhất (cùng thư mục với .py)
invoice_text_file = "invoices.txt"
with open(invoice_text_file, "a", encoding="utf-8") as f:  # "a" để ghi thêm
    f.write(f"\n========== HÓA ĐƠN BÁN HÀNG - {current_time_for_filename} ==========\n")
    f.write(f"Thời gian: {current_date} {current_time}\n")
    f.write(f"Sản phẩm: {product_name}\n")
    f.write(f"Số lượng: {quantity}\n")
    f.write(f"Đơn giá: {unit_price_formatted}\n")
    f.write(f"Tổng cộng: {total_price_formatted}\n")
    f.write("--------------------------------------\n")
    f.write("THANH TOÁN QUA NGÂN HÀNG\n")
    f.write("Ngân hàng: Vietcombank\n")
    f.write("Số TK: 0311000742731\n")
    f.write("Chủ TK: Dinh Thi Hiep\n")
    f.write("--------------------------------------\n")
    f.write("THANH TOÁN QUA MOMO\n")
    f.write("Số điện thoại: 0866005531\n")
    f.write("Chủ TK: Nguyen Ngoc Truong\n")
    f.write("--------------------------------------\n")
    f.write("CẢM ƠN QUÝ KHÁCH!\n")
    f.write("======================================\n")

# Theo dõi tổng doanh thu (cùng thư mục với .py)
revenue_file = "revenue.txt"
revenue_data = {"day": {}, "month": {}, "year": {}}

# Đọc dữ liệu doanh thu hiện có (nếu tồn tại)
if os.path.exists(revenue_file):
    with open(revenue_file, "r", encoding="utf-8") as f:
        lines = f.readlines()
        current_section = None
        for line in lines:
            line = line.strip()
            # Sửa phần kiểm tra header để khớp với định dạng ghi trong file
            if line.startswith("=== Doanh thu ngày"):
                current_section = "day"
            elif line.startswith("=== Doanh thu tháng"):
                current_section = "month"
            elif line.startswith("=== Doanh thu năm"):
                current_section = "year"
            elif line and "=" in line and current_section:
                date, amount = line.split(" = ")
                revenue_data[current_section][date] = int(amount.replace(",", ""))

# Cập nhật doanh thu
revenue_data["day"][current_day] = revenue_data["day"].get(current_day, 0) + total_price
revenue_data["month"][current_month] = revenue_data["month"].get(current_month, 0) + total_price
revenue_data["year"][current_year] = revenue_data["year"].get(current_year, 0) + total_price

# Ghi lại doanh thu vào file
with open(revenue_file, "w", encoding="utf-8") as f:
    f.write("=== Doanh thu ngày ===\n")
    for date, amount in revenue_data["day"].items():
        f.write(f"{date} = {amount:,d}\n")
    f.write("\n=== Doanh thu tháng ===\n")
    for month, amount in revenue_data["month"].items():
        f.write(f"{month} = {amount:,d}\n")
    f.write("\n=== Doanh thu năm ===\n")
    for year, amount in revenue_data["year"].items():
        f.write(f"{year} = {amount:,d}\n")

print(f"Hóa đơn đã được lưu tại: {output_path}")
print(f"Thông tin hóa đơn đã được ghi thêm vào: {invoice_text_file}")
print(f"Doanh thu đã được cập nhật trong: {revenue_file}")
