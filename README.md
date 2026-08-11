# License Key API

Hệ thống tạo & xác thực license key cho phần mềm, viết bằng FastAPI + SQLite.

## 1. Cài đặt

```bash
pip install -r requirements.txt
```

## 2. Đặt admin secret

Đây là "mật khẩu" để gọi các API quản trị (tạo key, xem danh sách...).
**Đổi giá trị này, đừng dùng mặc định:**

```bash
export ADMIN_SECRET="chuoi-bi-mat-cua-ban"
```

Trên Windows (PowerShell): `$env:ADMIN_SECRET="chuoi-bi-mat-cua-ban"`

## 3. Chạy server

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Mở trình duyệt tới `http://localhost:8000` → trang quản trị để tạo/xem key.
Nhập đúng `ADMIN_SECRET` vào ô "Admin Key" trên trang.

Tài liệu API tự động (Swagger): `http://localhost:8000/docs`

## 4. Các API chính

### Tạo key (admin) — `POST /admin/generate-keys`
Header: `X-Admin-Key: <ADMIN_SECRET>`
```json
{
  "quantity": 10,
  "product_name": "MyApp Pro",
  "max_activations": 1,
  "expires_in_days": 365,
  "prefix": "PRO"
}
```

### Xem danh sách key (admin) — `GET /admin/keys`
Header: `X-Admin-Key: <ADMIN_SECRET>`

### Thu hồi key (admin) — `POST /admin/revoke`
```json
{ "license_key": "PRO-AB3CD-..." }
```

### Kích hoạt key (client — phần mềm của bạn gọi) — `POST /api/v1/activate`
Không cần admin key. Gọi khi người dùng nhập key lần đầu.
```json
{ "license_key": "PRO-AB3CD-...", "device_id": "may-tinh-cua-khach-001" }
```
`device_id` là bạn tự sinh ra để định danh máy khách (vd hash từ thông tin phần cứng).

### Kiểm tra key còn hợp lệ không — `POST /api/v1/validate`
Gọi định kỳ (vd mỗi lần mở app) để chắc key chưa bị thu hồi/hết hạn.
```json
{ "license_key": "PRO-AB3CD-...", "device_id": "may-tinh-cua-khach-001" }
```
Trả về `{"valid": true/false, "reason": "..."}`.

## 5. Ví dụ gọi từ phần mềm của bạn (Python)

```python
import requests

resp = requests.post("https://api-cua-ban.com/api/v1/activate", json={
    "license_key": "PRO-AB3CD-EFGHJ-KMNPQ-RSTUV",
    "device_id": "hwid-cua-may-nay"
})
print(resp.json())
```

## 6. Khi triển khai thật (production)

- Đặt `ADMIN_SECRET` mạnh, không commit vào git.
- Chạy sau reverse proxy có HTTPS (Nginx/Caddy) — đừng để lộ API ở HTTP trần.
- Cân nhắc giới hạn tốc độ gọi (rate limit) cho `/api/v1/activate` để tránh bị dò key.
- File `licenses.db` (SQLite) nên được backup định kỳ; nếu tải cao, có thể chuyển sang PostgreSQL sau.
- Có thể thêm chữ ký/mã hoá vào chính license key nếu muốn xác thực offline (không cần gọi API mỗi lần) — nói mình biết nếu bạn cần hướng đó.
