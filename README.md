CI/CD Security Checker  
Automated Security Analysis for GitHub Actions & GitLab CI Pipelines

## Giới thiệu:
"CI/CD Security Checker" là một công cụ Python giúp phân tích "mức độ an toàn bảo mật" của các pipeline CI/CD phổ biến như "GitHub Actions" và "GitLab CI".

## Công cụ tự động:
- Phát hiện "lộ Secret/Token" trong script và môi trường  
- Nhận diện "các hành vi nguy hiểm" trong pipeline  
- Kiểm tra pipeline có tuân thủ "best practices"  
- Tính toán "điểm bảo mật (0–100)"  
- Xuất báo cáo đẹp bằng Rich + tùy chọn xuất ra JSON  

## Tính năng chính:
Secret Scanner  
- AWS Key  
- GitHub Token  
- Password  
- JWT  
- Private Key  

Risky Pattern Detector  
- curl | bash  
- wget | bash  
- sudo  
- docker --privileged  

Best Practice Checker  
- Dependency scan  
- Security scan  

Security Score  
Điểm dựa trên secret, risky steps và best practices.

## Cách chạy:
python main.py -f examples/github_insecure.yml
python main.py -f examples/github_secure.yml
python main.py -f examples/gitlab_insecure.yml
python main.py -f examples/gitlab_secure.yml


## Cài đặt:
pip install pyyaml rich


## Cấu trúc dự án:
cicd-security-checker/
│
├── main.py  
├── pipeline_parser.py  
├── secret_scanner.py  
├── risky_step_checker.py  
├── best_practice_checker.py  
├── score_calculator.py  
├── report.py  
│  
└── examples/  
    ├── github_insecure.yml  
    ├── github_secure.yml  
    ├── gitlab_insecure.yml  
    └── gitlab_secure.yml  

