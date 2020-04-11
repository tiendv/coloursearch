# Content-Based Image Retrieval System based on Color

## Các phần mềm cần thiết

- Python 3
- Virtualenv
- Django
- NGINX

<p align="center">
  <img src="https://github.com/tiendv/coloursearch/blob/master/resources/1.png?raw=true" alt="Sơ đồ minh hoạ kiến trúc các công nghệ được sử dụng trong ứng dụng"/>
</p>
<p align="center">
<i>Sơ đồ minh hoạ kiến trúc các công nghệ được sử dụng trong ứng dụng.</i></p>

## Các bước cài đặt

### Đối với Windows

Đối với hệ điều hành Windows, việc cài đặt và thiết lập uWSGI phức tạp và phát sinh nhiều vấn đề chưa được hỗ trợ đầy đủ bởi nhà phát hành nên bài viết giới hạn tới phần chạy ứng dụng Django.

1. Tải về và cài đặt phiên bản Python 3 mới nhất tại địa chỉ. https://www.python.org/downloads/

2. Tải về và cài đặt Git phiên bản mới nhất tại địa chỉ. https://git-scm.com/downloads

3. Clone project bằng cách nhập vào câu lệnh sau:

    ~~~bash
    git clone https://github.com/tiendv/coloursearch.git
    ~~~

4. Mở Command Prompt (hoặc Windows Powershell hoặc Mingw-w64, Cygwin), cài đặt Virtual Environment (Virtualenv) bằng PyPI (pip) (đã được cài đặt cùng với Python 3):

    ~~~bash
    pip install virtualenv
    ~~~

5. Tạo một môi trường ảo cho project (để cài đặt các package của Python vào môi trường này) bằng Virtualenv:

    ~~~bash
    virtualenv <tên môi trường ảo>
    ~~~

    ~~~bash
    # Thí dụ:
    virtualenv cbir
    ~~~

6. Kích hoạt môi trường ảo:

    ~~~bash
    .\cbir\Scripts\activate
    ~~~

7. Cài đặt các package của Python thông qua PyPI (pip) được mô tả trong file `requirements.txt` (bao gồm Django, mysqlclient, numpy, scipy, opencv, faiss và một số thư viện khác):

    ~~~bash
    pip install -r requirements.txt
    ~~~

    __Lưu ý:__ Tới thời điểm hiện tại, faiss chưa hỗ trợ Windows, khi build trên Windows sẽ bị lỗi. Một giải pháp thay thế cho việc indexing bằng faiss là dùng multiprocessing. Để deploy project trên Windows, người dùng comment các dòng số `212-232`, `326-346`, `444-464` và bỏ comment các dòng số `235-249`, `349-365`, `467-483`.

8. Tải về và cài đặt hệ quản trị cơ sở dữ liệu MySQL tại địa chỉ. https://dev.mysql.com/downloads/installer/

    __Lưu ý:__ Đối với Windows, yêu cầu cài đặt Microsoft .NET Framework từ 3.5.2 trở lên và Microsoft Visual C++ Redistributable Package để có thể cài đặt MySQL.

9. Sau khi cài đặt thành công MySQL và đã khởi động các service cần thiết. Đăng nhập vào MySQL Shell, tạo cơ sở dữ liệu có tên là cbir (khớp với tên cơ sở dữ liệu trong file `content-based-image-retrieval\src\settings.py`, dòng 83):

    ~~~SQL
    CREATE DATABASE cbir;
    ~~~

    Tạo tài khoản người dùng mới trong MySQL (khớp với `username` và `password` trong file `content-based-image-retrieval\src\cbir\settings.py`, dòng 84, 85)

    ~~~SQL
    CREATE USER 'django_user'@'localhost' IDENTIFIED BY '123456';
    ~~~

    Thêm quyền cho tài khoản người dùng vừa tạo trên cơ sở dữ liệu `cbir`:

    ~~~SQL
    GRANT ALL PRIVILEGES ON cbir.* TO 'django_user'@'localhost';
    ~~~

10. Migrate cấu trúc model trong project Django qua database schema:

    Kích hoạt môi trường ảo `cbir`:

    ~~~bash
    .\cbir\Scripts\activate
    ~~~

    Migrate từ thư mục chứa file `manage.py`:

    ~~~bash
    python manage.py migrate
    ~~~

    Nếu thông báo migrate tất cả các file thành công, trong MySQL sẽ hiện ra các table.

    <p align="center">
    <img src="https://github.com/tiendv/coloursearch/blob/master/resources/2.png?raw=true" alt="Migrate cấu trúc model trong project Django qua database schema thành công"/>
    </p>
    <p align="center">
    <i>Migrate cấu trúc model trong project Django qua database schema.</i></p>

    <p align="center">
    <img src="https://github.com/tiendv/coloursearch/blob/master/resources/3.png?raw=true" alt="Các table được tạo ra trong MySQL"/>
    </p>
    <p align="center">
    <i>Các table được tạo ra trong MySQL.</i></p>

11. Để chạy ứng dụng Django, chạy lệnh sau:

    ~~~bash
    python manage.py runserver
    ~~~

    Mở trình duyệt web, truy cập vào địa chỉ http://127.0.0.1:8000 màn hình ứng dụng sẽ hiện ra.

### Đối với Ubuntu

1. Cài đặt Python 3:

    ~~~bash
    sudo apt update
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.7
    sudo apt install build-essential libssl-dev libffi-dev python3-dev
    ~~~

    Vào file `.bashrc` của Ubuntu, thêm dòng sau để alias python3 thành python:

    ~~~bash
    alias python='python3'
    alias pip='pip3
    ~~~

    Khởi động lại Terminal để sử dụng.

2. Cài đặt Git:

    ~~~bash
    sudo apt install git
    ~~~

3. Clone project bằng cách nhập vào câu lệnh sau:

    ~~~bash
    git clone https://github.com/tiendv/coloursearch.git
    ~~~

4. Cài đặc PyPI (pip):

    ~~~bash
    sudo apt install -y python3-pip
    ~~~

5. Cài đặt Virtual Environment (Virtualenv):

    ~~~bash
    sudo apt install -y python3-venv
    ~~~

6. Tạo một môi trường ảo cho project (để cài đặt các package của Python vào môi trường này) bằng Virtualenv:

    ~~~bash
    python -m venv cbir
    ~~~

7. Kích hoạt môi trường:

      ~~~bash
      source cbir/bin/activate
      ~~~

8. Cài đặt MySQL:

    ~~~bash
    sudo apt install -y mysql-server
    sudo apt install -y libmysqlclient-dev
    ~~~

9. Cài đặt các package của Python thông qua PyPI (pip) được mô tả trong file requirements.txt (bao gồm Django, mysqlclient, numpy, scipy, opencv, faiss và một số thư viện khác):

    ~~~bash
    pip install -r requirements.txt
    ~~~

10. Sau khi cài đặt thành công MySQL và đã khởi động các service cần thiết. Đăng nhập vào MySQL Shell, tạo cơ sở dữ liệu có tên là cbir (khớp với tên cơ sở dữ liệu trong file `content-based-image-retrieval/src/settings.py`, dòng 83):

    Đăng nhập MySQL Shell:

    ~~~bash
    mysql -u root -p
    ~~~

    Tạo cơ sở dữ liệu cbir:

    ~~~SQL
    CREATE DATABASE cbir;
    ~~~

    Tạo tài khoản người dùng mới trong MySQL (khớp với username và password trong file `content-based-image-retrieval/src/cbir/settings.py`, dòng 84, 85)

    ~~~SQL
    CREATE USER 'django_user'@'localhost' IDENTIFIED BY '123456';
    ~~~

    Thêm quyền cho tài khoản người dùng vừa tạo trên cơ sở dữ liệu `cbir`:

    ~~~SQL
    GRANT ALL PRIVILEGES ON cbir.TO 'django_user'@'localhost';
    ~~~

11. Migrate cấu trúc model trong project Django qua database schema:

    Kích hoạt môi trường ảo:

    ~~~SQL
    source cbir/venv/activate
    ~~~

    Migrate từ thư mục `content-based-image-retrieval/src/`:

    ~~~bash
    python manage.py migrate
    ~~~

    Nếu thông báo migrate tất cả các file thành công, trong MySQL sẽ hiện ra các table.

12. Cài đặt nginx server:

    ~~~bash
    sudo apt install -y nginx
    ~~~

    __Điều chỉnh cấu hình Ubuntu firewall:__

    Kiểm tra danh sách cấu hình ứng dụng mà Ubuntu firewall nhận diện được có tồn tại Nginx hay không:

    ~~~bash
    sudo ufw app list
    ~~~

    Output:

    ~~~bash
    Available applications:
      Nginx Full
      Nginx HTTP
      Nginx HTTPS
      OpenSSH
    ~~~

    Cho phép Nginx HTTP

    ~~~bash
    sudo ufw allow 'Nginx HTTP'
    ~~~

    Kiểm tra trạng thái hoạt động của Nginx bằng câu lệnh sau:

    ~~~bash
    systemctl status nginx
    ~~~

13. Tạo một file `.ini` để mô tả các thiết lập cấu hình uWSGI cho project.

    ~~~ini
    # cbir_uwsgi.ini file
    [uwsgi]

    # Django-related settings
    # the base directory (full path)
    chdir           = /home/username/content-based-image-retrieval/src
    # Django's wsgi file
    module          = cbir.wsgi
    # the virtualenv (full path)
    home            = /home/username/content-based-image-retrieval/cbir

    # process-related settings
    # master
    master          = true
    # maximum number of worker processes
    processes       = 10
    # the socket (use the full path to be safe
    socket          = /home/username/content-based-image-retrieval/cbir.sock
    # ... with appropriate permissions - may be needed
    chmod-socket    = 666
    # clear environment on exit
    vacuum          = true
    ~~~

    Trong đó:

    - `chdir` là đường dẫn của thư mục chứa file `manage.py` của project.
    - `module` là tên module WSGI của project được mô tả trong file `content-based-image-retrieval/src/cbir/apps.py`.
    - `home` là đường dẫn của thư mục virtualenv của project.
    - `socket` là đường dẫn của file socket muốn tạo.

14. Cài đặt uwsgi:

    ~~~bash
    pip install uwsgi
    ~~~

    Tạo file `uwsgi.serivce` tại đường dẫn `/etc/systemd/system/` có nội dung như sau:

    ~~~bash
    [Unit]
    Description=uWSGI Emperor service
    After=syslog.target

    [Service]
    ExecStart=/usr/local/bin/uwsgi --emperor /home/username/content-based-image-retrieval/cbir_uwsgi.ini
    Restart=always
    KillSignal=SIGQUIT
    Type=notify
    StandardError=syslog
    NotifyAccess=all

    [Install]
    WantedBy=multi-user.target
    ~~~

    Trong đó:

    - `ExecStart=/usr/local/bin/uwsgi` mô tả đường dẫn của uWSGI được cài đặt trong máy, để có thể lấy đường dẫn này, chạy lệnh `which uwsgi` hoặc `whereis uwsgi`.

    - `--emperor /home/username/content-based-image-retrieval/cbir_uwsgi.ini` là địa chỉ đường dẫn tới file `.ini` ở trên.

    Làm mới trạng thái của `systemd` với uWSGI service:

    ~~~bash
    sudo systemctl daemon-reload
    ~~~

    Khởi động uWSGI

    ~~~bash
    sudo systemctl start uwsgi
    ~~~

15. Tạo file cấu hình của NGINX tên `cbir.conf` tại đường dẫn `/etc/nginx/conf.d` có nội dung như sau:

    ~~~ini
    # cbir.conf
    upstream django {
        server unix:///home/username/content-based-image-retrieval/cbir.sock;
    }

    # configuration of the server
    server {
        listen      80;
        server_name cbir.net;
        charset     utf-8;

        client_max_body_size 75M;

        location /static {
            alias /home/username/content-based-image-retrieval/src/static;
        }

        location / {
            uwsgi_pass  django;
            include     /etc/nginx/uwsgi_params;
        }
    }
    ~~~

    Trong đó:

    - `/home/username/content-based-image-retrieval/cbir.sock` là đường dẫn chứa file socket của project.
    - `/home/username/content-based-image-retrieval/src/static` là đường dẫn chứa các file tĩnh (static) của project.
    - `/etc/nginx/uwsgi_params` là đường dẫn file chứa các tham số uWSGI để NGINX có thể phục vụ.

    Khởi động lại NGINX:

    ~~~bash
    sudo systemctl restart nginx
    ~~~

    Mở trình duyệt web, truy cập vào địa chỉ http://127.0.0.1:8000 sẽ ra được màn hình ứng dụng.

    <p align="center">
    <img src="https://github.com/tiendv/coloursearch/blob/master/resources/5.png?raw=true" alt="Màn hình ứng dụng"/>
    </p>
    <p align="center">
    <i>Màn hình ứng dụng</i></p>

## Thực thi ứng dụng

1. Câu lệnh sau thực hiện việc trích xuất đặc trưng từ dữ liệu hình ảnh:

    ~~~bash
    python manage.py extract -p1 <tham số 1> -p2 <tham số 2> -p3 <tham số 3> '<đường dẫn thư mục hình ảnh trong dấu nháy đơn>' '<loại đặc trưng cần trích xuất>'
    ~~~

    ~~~bash
    # Thí dụ
    python manage.py extract -p1 4096 -p2 64 -p3 1.9 '/home/username/images' 'fuzzy_color_histogram'
    ~~~

    Trong đó, loại đặc trưng cần trích xuất kèm theo tham số thường được sử dụng có trong bảng sau:

    | Tên đặc trưng              | Mã đặc trưng               | Tham số 1                                          | Tham số 2                                               | Tham số 3                        |
    |----------------------------|----------------------------|----------------------------------------------------|---------------------------------------------------------|----------------------------------|
    | Fuzzy Color Histogram      | fuzzy_color_histogram      | Số lượng màu sắc thô - n (Number of coarse colors) | Số lượng màu sắc sau xử lý - n' (Number of fine colors) | Số mũ đóng vai trò  trọng số - m |
    | Color Correlogram          | color_correlogram          | Số lượng màu sắc - n (Number of colors)            | Khoảng cách tối đa - d (Distance)                       | Gia số - i (Increment)           |
    | Color Coherence Vector     | color_coherence_vector     | Số lượng màu sắc - n (Number of colors)            | Đại lượng xác định  tính coherence - т (tau)            |                                  |
    | Cumulative Color Histogram | cumulative_color_histogram | Số lượng màu sắc - n (Number of colors)            |                                                         |                                  |

    <p align="center">
    <img src="https://github.com/tiendv/coloursearch/blob/master/resources/4.png?raw=true" alt="Trích xuất đặc trưng thành công"/>
    </p>
    <p align="center">
    <i>Trích xuất đặc trưng thành công.</i></p>

2. Đối với đặc trưng Fuzzy Color Histogram, để tăng tốc độ truy xuất hình ảnh, thực hiện câu lệnh sau để annotate các màu về một số màu cơ bản:

    ~~~bash
    python manage.py annotate '<đường dẫn thư mục hình ảnh>'
    ~~~

    ~~~bash
    # Thí dụ:
    python manage.py annotate '/home/username/images'
    ~~~

    Câu lệnh này sẽ gán nhãn các hình ảnh trong thư mục với một số màu sắc phổ biến được quy định sẵn và lưu lại trong file `.csv` trong đường dẫn `content-based-image-retrieval/src/annotation`.

3. Câu lệnh sau thực hiện việc đánh giá phương pháp trích xuất:

    ~~~bash
    python manage.py evaluate '<tên tập dữ liệu hình ảnh>' '<đường dẫn thư mục hình ảnh truy vấn>' '<extraction_id>' '<k>' '<loại truy vấn>'
    ~~~

    ~~~bash
    # Thí dụ:
    python manage.py evaluate 'ukbench' '/home/username/query/ukbench_query_images' 1 10 'color_layout'
    ~~~

    Trong đó:
    - `<tên tập dữ liệu hình ảnh>`: hiện tại project hỗ trợ đánh giá hai tập dữ liệu hình ảnh là `holidays` ([INRIA Holidays](http://lear.inrialpes.fr/people/jegou/data.php)) và `ukbench` ([University of Kentucky Benchmark](https://archive.org/details/ukbench)). Người dùng có thể tuỳ chỉnh trong file `content-based-image-retrieval/src/cbir/views/evaluate.py`
    - `<k>` là số hình ảnh đầu tiên trong kết quả tìm kiếm lấy ra để đánh giá.
    - `<loại truy vấn>` là cách thức truy vấn hình ảnh, bao gồm: `image` và `color_layout`.
