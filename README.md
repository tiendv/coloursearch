# Content-Based Image Retrieval System based on Color

## Các phần mềm cần thiết

- Python
- virtualenv
- django
- nginx

<p align="center">
  <img src="https://github.com/nxh235/content-based-image-retrieval/blob/master/resources/1.png?raw=true" alt="Sơ đồ minh hoạ kiến trúc các công nghệ được sử dụng trong ứng dụng"/>
</p>
<p align="center">
<i>Sơ đồ minh hoạ kiến trúc các công nghệ được sử dụng trong ứng dụng</i></p>

## Các bước cài đặt

### Đối với Windows

1. Tải về và cài đặt phiên bản Python 3 mới nhất tại địa chỉ. https://www.python.org/downloads/

2. Tải về và cài đặt Git phiên bản mới nhất tại địa chỉ. https://git-scm.com/downloads

3. Clone project bằng cách nhập vào câu lệnh sau:

    ~~~bash
    git clone https://github.com/tiendv/coloursearch.git
    ~~~

4. Cài đặt Virtual Environment (Virtualenv) bằng pip (gõ câu lệnh vào Command Prompt trong Windows hoặc Terminal đối với Ubuntu):

    ~~~bash
    pip install virtualenv
    ~~~

5. Tạo một môi trường ảo cho project (để cài đặt các package của Python vào môi trường này) bằng Virtualenv:

    ~~~bash
    virtualenv <tên môi trường>

    virtualenv cbir
    ~~~

6. Kích hoạt môi trường ảo:

    ~~~bash
    .\cbir\Scripts\activate
    ~~~

7. Cài đặt các package của Python thông qua PyPI (pip) được mô tả trong file requirements.txt (bao gồm Django, mysqlclient, numpy, scipy, opencv, faiss và một số thư viện khác):

    ~~~bash
    pip install -r requirements.txt
    ~~~

    __Lưu ý__. Tới thời điểm hiện tại, faiss-cpu hiện tại chưa hỗ trợ Windows, khi build trên Windows sẽ bị lỗi.

8. Tải về và cài đặt hệ quản trị cơ sở dữ liệu MySQL tại địa chỉ. https://dev.mysql.com/downloads/installer/

    Đối với Windows, yêu cầu cài đặt Microsoft .NET Framework từ 3.5.2 trở lên và Microsoft Visual C++ Redistributable Package để có thể cài đặt MySQL.

9. Sau khi cài đặt thành công MySQL và đã khởi động các service cần thiết. Đăng nhập vào MySQL Shell, tạo cơ sở dữ liệu có tên là cbir (khớp với tên cơ sở dữ liệu trong file `coloursearch\src\settings.py`, dòng 83):

    ~~~SQL
    CREATE DATABASE cbir;
    ~~~

    Tạo tài khoản người dùng mới trong MySQL khớp với `username` và `password` trong file `coloursearch\src\cbir\settings.py` (dòng 84, 85)

    ~~~SQL
    CREATE USER 'django_user'@'localhost' IDENTIFIED BY '123456';
    ~~~

    Thêm quyền cho tài khoản người dùng vừa tạo trên cơ sở dữ liệu cbir:

    ~~~SQL
    GRANT ALL PRIVILEGES ON cbir.TO 'django_user'@'localhost';
    ~~~

10. Migrate cấu trúc model trong project Django qua database schema:

    Kích hoạt môi trường ảo:

    ~~~bash
    source cbir\venv\activate
    ~~~

    Migrate từ thư mục coloursearch\src\:

    ~~~bash
    python manage.py migrate
    ~~~

    Nếu thông báo migrate tất cả các file thành công, trong MySQL sẽ hiện ra các table.

### Đối với Ubuntu

1. Cài đặt Python 3:

    ~~~bash
    sudo apt update
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt install python3.7
    sudo apt install build-essential libssl-dev libffi-dev python3-dev
    ~~~

    Vào file .bashrc của Ubuntu, thêm dòng sau để alias python3 thành python:

    ~~~bash
    alias python='python3'
    alias pip='pip3
    ~~~

    Khởi động lại Terminal để sử dụng.

2. Cài đặt Git:

    ~~~bash
    sudo apt-get install git
    ~~~

3. Clone project bằng cách nhập vào câu lệnh sau:

    ~~~bash
    git clone https://github.com/tiendv/coloursearch.git
    ~~~

4. Cài đặc pip:

    ~~~bash
    sudo apt install -y python3-pip
    ~~~

5. Cài đặt Virtual Environment (Virtualenv):

    ~~~bash
    bashsudo apt install -y python3-venv
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

10. Sau khi cài đặt thành công MySQL và đã khởi động các service cần thiết. Đăng nhập vào MySQL Shell, tạo cơ sở dữ liệu có tên là cbir (khớp với tên cơ sở dữ liệu trong file coloursearch\src\settings.py, dòng 83):

    ~~~SQL
    CREATE DATABASE cbir;
    ~~~

    Tạo tài khoản người dùng mới trong MySQL khớp với username và password trong file coloursearch\src\cbir\settings.py (dòng 84, 85)

    ~~~SQL
    CREATE USER 'django_user'@'localhost' IDENTIFIED BY '123456';
    ~~~

    Thêm quyền cho tài khoản người dùng vừa tạo trên cơ sở dữ liệu cbir:

    ~~~SQL
    GRANT ALL PRIVILEGES ON cbir.TO 'django_user'@'localhost';
    ~~~

11. Migrate cấu trúc model trong project Django qua database schema:

    Kích hoạt môi trường ảo:

    ~~~SQL
    source cbir\venv\activate
    ~~~

    Migrate từ thư mục coloursearch\src\:

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

    Output

    ~~~bash
    Available applications:
      Nginx Full
      Nginx HTTP
      Nginx HTTPS
      OpenSSH
    ~~~

    Cho phép Nginx

    ~~~bash
    sudo ufw allow 'Nginx HTTP'
    ~~~

    Kiểm tra Nginx có hoạt động ổn định bằng câu lệnh sau:

    ~~~bash
    systemctl status nginx
    ~~~

13. Tạo một file `.ini` để mô tả các thiết lập cấu hình uWSGI cho project.

    ~~~ini
    # cbir_uwsgi.ini file
    [uwsgi]

    # Django-related settings
    # the base directory (full path)
    chdir           = /home/cbir/coloursearch/src
    # Django's wsgi file
    module          = cbir.wsgi
    # the virtualenv (full path)
    home            = /home/cbir/coloursearch/cbir

    # process-related settings
    # master
    master          = true
    # maximum number of worker processes
    processes       = 10
    # the socket (use the full path to be safe
    socket          = /home/cbir/coloursearch/cbir.sock
    # ... with appropriate permissions - may be needed
    chmod-socket    = 666
    # clear environment on exit
    vacuum          = true
    ~~~

    Trong đó:

    - `chdir` là đường dẫn của thư mục chứa file `manage.py` của project.
    - `module` là tên module WSGI của project được mô tả trong file `coloursearch\src\cbir\apps.py`.
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
    ExecStart=/usr/local/bin/uwsgi --emperor /etc/uwsgi/sites
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

    - `--emperor /etc/uwsgi/sites` là địa chỉ đường dẫn tới file `.ini` ở trên.

    Làm mới trạng thái của `systemd` với uWSGI service:

    ~~~bash
    sudo systemctl daemon-reload
    ~~~

    Khởi động uWSGI

    ~~~bash
    sudo systemctl start uwsgi
    ~~~
