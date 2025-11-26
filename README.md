# CI/CD Security Checker

Phiên bản tiếng Việt — Công cụ phân tích mức độ an toàn bảo mật cho pipeline CI/CD.

> Lưu ý: Đây là bài tập lớn môn **An toàn bảo mật hệ thống thông tin**.

## Giới thiệu

`CI/CD Security Checker` là một công cụ viết bằng Python dùng để phân tích và đánh giá mức độ an toàn của các pipeline CI/CD phổ biến như GitHub Actions và GitLab CI. Công cụ tập trung vào ba trụ cột chính:

- Phát hiện secret/credentials rò rỉ trong cấu hình hoặc scripts.
- Nhận diện các bước/risky pattern có khả năng gây tổn hại (ví dụ: chạy script từ internet, quyền nâng cao).
- Kiểm tra các best practices cơ bản và tổng hợp điểm bảo mật (0–100).

Mục tiêu là cung cấp đánh giá nhanh, dễ đọc và có thể dùng để tích hợp vào quy trình kiểm tra code hoặc CI nội bộ.

## Tính năng chính

- **Quét Secret**: nhận diện các dạng secret phổ biến (AWS keys, GitHub tokens, password, JWT, private key, ...).
- **Phát hiện hành vi nguy hiểm (Risky Patterns)**: tìm kiếm các pattern rủi ro như `curl | bash`, `wget | bash`, `sudo` trong bước pipeline, `docker --privileged`, v.v.
- **Kiểm tra Best Practices**: phát hiện các bước quét dependency/security missing hoặc không có bước quét bảo mật.
- **Tính điểm bảo mật**: tổng hợp điểm từ số lượng secret, mức độ nguy hiểm của các bước, và tuân thủ best practices.
- **Báo cáo**: xuất báo cáo dạng console (đẹp với `rich`) và có thể mở rộng để xuất JSON.

## Kiến trúc hệ thống

Luồng xử lý chính của công cụ như sau:

1. `main.py` — điểm vào của chương trình: nhận tham số đầu vào (file pipeline), gọi các thành phần.
2. `pipeline_parser.py` — phân tích cấu trúc file pipeline (GitHub/GitLab) thành representation trung gian.
3. `secret_scanner.py` — quét representation để tìm secret theo regex/pattern.
4. `risky_step_checker.py` — kiểm tra từng bước (step) để phát hiện các pattern nguy hiểm.
5. `best_practice_checker.py` — đánh giá các best practices (dependency scan, security scan step có tồn tại không).
6. `score_calculator.py` — tổng hợp các kết quả thành một điểm số bảo mật (0–100).
7. `report.py` — trình bày kết quả: console friendly (sử dụng `rich`) và có thể xuất JSON (nếu cần mở rộng).

Thư mục `examples/` chứa các file pipeline mẫu để thử nghiệm:

- `examples/github_insecure.yml`
- `examples/github_secure.yml`
- `examples/gitlab_insecure.yml`
- `examples/gitlab_secure.yml`

## Cài đặt

1. Tạo môi trường ảo (khuyến khích):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Cài dependencies cơ bản:

```bash
pip install pyyaml rich
```

Ghi chú: nếu muốn quản lý dependencies tập trung, bạn có thể tạo `requirements.txt` sau này chứa `pyyaml` và `rich`.

## Cách chạy

Chạy công cụ bằng cách chỉ tới file pipeline cần phân tích với tham số `-f`:

```bash
python main.py -f examples/github_insecure.yml
python main.py -f examples/github_secure.yml
python main.py -f examples/gitlab_insecure.yml
python main.py -f examples/gitlab_secure.yml
```

Tham số thông dụng (có thể được `main.py` hỗ trợ):

- `-f, --file`: đường dẫn tới file pipeline YAML.
- Có thể thêm flag xuất `--json` nếu muốn report ở dạng JSON (tùy implement).

Kết quả: chương trình sẽ in báo cáo tóm tắt lên console và hiển thị các secret/risky-step tìm được cùng điểm số đánh giá.

## Ví dụ

Ví dụ nhanh (dùng file mẫu trong `examples/`):

```bash
# Kiểm tra pipeline GitHub insecure
python main.py -f examples/github_insecure.yml

# Kiểm tra pipeline GitHub secure
python main.py -f examples/github_secure.yml
```

Sau khi chạy, kiểm tra output console để xem chi tiết: danh sách secret/phát hiện, các bước nguy hiểm, và điểm bảo mật tổng hợp.

## Hạn chế

- Đây là một công cụ phân tích tĩnh, dựa vào pattern/regex; do đó có thể có **false positives** hoặc **false negatives**.
- Khả năng nhận diện secret phụ thuộc vào các biểu thức chính quy hiện có trong `secret_scanner.py`.
- Hiện tại chưa hỗ trợ phân tích sâu runtime (ví dụ: secrets được set qua secrets manager runtime, hoặc secrets nằm trong file mã hóa).
- Không thực hiện scanning phụ thuộc (dependency scanning) thực tế — chỉ phát hiện bước/thói quen gọi công cụ quét.
- Chưa có cơ chế CI integration/suggested-fixes tự động (ví dụ: tự động tạo PR để xóa secret).

## Hướng phát triển

- Mở rộng mẫu nhận diện secret (giảm false positives/negatives).
- Thêm tùy chọn xuất báo cáo chi tiết ở dạng JSON/HTML để dễ tích hợp với dashboard.
- Tích hợp với các dịch vụ quét dependency (Snyk, Dependabot) để thực hiện kiểm tra phụ thuộc thực tế.
- Thêm rule engine cấu hình (cho phép người dùng thêm/điều chỉnh rules mà không sửa code).
- Thêm pipeline CI job mẫu để tự động chạy công cụ này khi pipeline thay đổi.

## Cách đóng góp

- Mở issue hoặc PR trên repository, miêu tả test case và mục tiêu cải tiến.
- Khi thêm rule/quét mới, bổ sung test/example trong thư mục `examples/` để minh hoạ.

---

Nếu bạn cần, tôi có thể tiếp tục: tạo `requirements.txt`, thêm flag `--json` cho `main.py`, hoặc viết hướng dẫn tích hợp vào GitHub Actions.


