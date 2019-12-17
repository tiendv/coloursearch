# Server

Cài đặt Docker, java 1.8, nodejs.

Chạy lệnh sau để cài đặt ADAMPro 2.0 (phần mềm quản lý cơ sở dữ liệu trích xuất), ADAMPro UI chạy trên port 443, Spark chạy trên port 80.
~~~
docker run --name adampro -p 80:4040 -p 5890:5890 -p 443:9099 -d vitrivr/adampro:2.0-selfcontained
~~~

Tải source code Cineast (retrival) tại:

https://github.com/vitrivr/cineast/archive/2.0.0.zip

Trang chủ GitHub: https://github.com/vitrivr/cineast/releases

Giải nén ra thư mục `cineast-2.0.0`

Chỉnh sửa file `cineast.json` có nội dung như sau:

~~~
{
	"database": {
		"host" : "127.0.0.1",
		"port": 5890,
		"plaintext": true
	},
	"benchmark": {
		"mode":"OFF",
		"path":"benchmarks"
	},
	"retriever": {
		"threadPoolSize": 2,
		"maxResults": 200,
		"resultsPerModule": 250,
		"features" : {
			"globalcolor": [
				{"feature": "AverageColor",							"weight": 2.3},
				{"feature": "MedianColor",							"weight": 1.2},
				{"feature": "AverageFuzzyHist",						"weight": 0.7},
				{"feature": "AverageFuzzyHistNormalized",			"weight": 0.7},
				{"feature": "MedianFuzzyHist",						"weight": 1.3},
				{"feature": "QueryImageExporter",					"weight": 0.00001}
			],
			"localcolor": [
				{"feature": "AverageColorRaster",					"weight": 1.0}
			],
			"edge": [
				{"feature": "EdgeARP88",							"weight": 0.85},
				{"feature": "EdgeGrid16",							"weight": 1.15},
				{"feature": "EHD",									"weight": 0.7},
				{"feature": "DominantEdgeGrid16",					"weight": 1.4},
				{"feature": "DominantEdgeGrid8",					"weight": 1.4}
			],
			"motion": [
				{"feature": "SubDivMotionHistogram3",				"weight": 0.5},
				{"feature": "SubDivMotionHistogram5",				"weight": 0.5},
				{"feature": "SubDivMotionHistogramBackground3",		"weight": 0.5},
				{"feature": "SubDivMotionHistogramBackground5",		"weight": 0.5}
			],
			"quantized": [
				{"feature": "AverageColorGrid8Reduced11",			"weight": 1.0},
				{"feature": "AverageColorGrid8Reduced15",			"weight": 1.0},
				{"feature": "AverageColorRasterReduced11",			"weight": 1.0},
				{"feature": "AverageColorRasterReduced15",			"weight": 1.0},
				{"feature": "CLDReduced11",							"weight": 1.0},
				{"feature": "CLDReduced15",							"weight": 1.0}
			],
			"asr": [
				{"feature": "SubtitleFulltextSearch",				"weight": 1.0}
			],
			"ocr": [
				{"feature": "OCRSearch",							"weight": 1.0}
			],
			"description": [
				{"feature": "DescriptionTextSearch",				"weight": 1.0}
			],
			"localfeatures" : [
				{"feature": "SURFMirflickr25K512",					"weight": 1.75},
				{"feature": "HOGMirflickr25K512",					"weight": 1.0}
			],
			"localfeatures_fast" : [
				{"feature": "SURFMirflickr25K256",					"weight": 1.75},
				{"feature": "HOGMirflickr25K256",					"weight": 1.0}
			],
			"meta": [
				{"feature": "VideoMetadata",					"weight": 1.0}
			],
			"audiofingerprint": [
				{"feature": "AudioFingerprint",					"weight": 1.0}
			],
			"hpcpaverage" : [
				{"feature": "AverageHPCP20F36B",				"weight": 1.5},
				{"feature": "AverageHPCP30F36B",				"weight": 0.75}
			],
			"audiomatching" : [
				{"feature": "CENS12Shingle",						"weight": 2.0},
				{"feature": "HPCP12Shingle",						"weight": 1.0},
				{"feature": "MFCCShingle",							"weight": 0.5}
			],
			"lightfield" : [
				{"feature": "LightfieldFourier",				"weight": 1.0},
				{"feature": "LightfieldZernike",				"weight": 2.5}
			],
			"sphericalharmonicslow" : [
				{"feature": "SphericalHarmonicsLow",			"weight": 1.0}
			],
			"sphericalharmonicsdefault" : [
				{"feature": "SphericalHarmonicsDefault",		"weight": 1.0}
			],
			"sphericalharmonicshigh" : [
				{"feature": "SphericalHarmonicsHigh",			"weight": 1.0}
			],
			"pitchsequence" : [
				{"feature": "MelodyEstimate",			 		"weight": 1.0}
			]
		}
	},
	
	"decoders": {
		"VIDEO":{
			"decoder": "FFMPEG",
			"properties": {
				"maxFrameWidth": 640,
				"maxFrameHeight": 480
			}
		},
		"IMAGE":{
			"decoder": "DefaultImageDecoder",
			"properties": {
				"bounds":1024
			}
		},
		"AUDIO":{
			"decoder": "FFMpegAudioDecoder",
			"properties": {
				"samplerate":44100,
				"channels":2
			}
		}
	},
	
	"extractor": {
		"threadPoolSize": 4,
		"outputLocation": "out"
	},
	
	"imagecache": {
		"softMemoryLimit": 2048,
		"hardMemoryLimit": 1024
	},
	
	"api": {
		"enableCLI": true,
		"enableWebsocket": true,
		"enableWebsocketSecure": false,
		"enableRest": true,
		"enableRestSecure": false,
		"enableLegacy":false,
		"maxMessageSize":40960000,
		"httpPort": 8080,
		"httpsPort": 4568,
		"legacyPort": 12345,
		"threadPoolSize" : 16
	},
	
	"visualization": {
		"cacheEnabled": false,
		"cachePath": "cache/art/"
	}

}
~~~

Trong database là cấu hình của ADAMPro và API là cấu hình của Cineast (để ý địa chỉ IP và số port). Ở đây, Cineast chạy port 8080 trên server.

Sau đó, chạy lệnh sau:

~~~
cd cineast
./gradlew deploy
~~~

Để deploy Cineast ra thư mục `build`. Sau đó, thêm các thuộc tính trích của của Cineast vào ADAMPro bằng lệnh sau:

~~~
cd build/libs/
java -jar cineast.jar --setup
~~~

Tải job file của Cineast tại địa chỉ sau:

https://github.com/vitrivr/cineast-config-examples/tree/master/jobs

Địa chỉ job trích xuất ảnh, mặc định: 

https://raw.githubusercontent.com/vitrivr/cineast-config-examples/master/jobs/extract%20default/extraction_images.json

Chỉnh sửa job file như sau:

~~~
{
	"type":"IMAGE",
	"input":{
		"path": "/path/to/data/images/",
		"depth": 2,
		"skip": 0,
		"id": {
			"name": "UniqueObjectIdGenerator",
			"properties": {}
		}
	},
	"extractors":[
		{"name": "AverageColor"},
		{"name": "AverageColorRaster"},
		{"name": "AverageFuzzyHist"},
		{"name": "EdgeARP88"},
		{"name": "EdgeGrid16"},
		{"name": "EHD"},
		{"name": "MedianColor"},
		{"name": "HOGMirflickr25K512"},
		{"name": "SURFMirflickr25K512"}
	],
	"exporters":[
		{
			"name": "ShotThumbNails",
			"properties": {
				"destination":"/path/to/thumbnails/"
			}
		}
	]
}
~~~

Trong đó `"path": "/path/to/data/images/"` là đường dẫn thư mục chứa hình ảnh cần rút trích đặc trưng đầu vào.

`"destination":"/path/to/thumbnails/` là đường dẫn thư mục chứa hình ảnh thumbnails đầu ra.

Sau đó, chạy lệnh sau để chạy job rút trích đặc trưng từ hình ảnh:

~~~
java -Xmx8g -Xms8g -jar cineast.jar --job /path/to/job.json
~~~

Trong đó, `/path/to/job.json` là đường dẫn tới file job.

Để dừng ADAMPro trên server, chạy lệnh (chạy dưới quyền administrator):

~~~
docker stop adampro
~~~

# Client
Địa chỉ GitHub của `vitrivr-ng`:
https://github.com/vitrivr/vitrivr-ng/

Tải bản phát hành phiên bản 1.0.2 tại địa chỉ:

https://github.com/vitrivr/vitrivr-ng/archive/v1.0.2.zip

Giải nén ra thư mục `vitrivr-ng-1.0.2` bằng lệnh:

~~~
unzip vitrivr-ng-1.0.2.zip
~~~

Sửa file cấu hình tại địa chỉ `\vitrivr-ng-1.0.2\src\config.json`

~~~
{
  "api": {
    "host" : "192.168.28.75",
    "port" : 8080,
    "protocol_http": "http",
    "protocol_ws": "ws",
    "ping_interval": 10000
  },
  "resources": {
    "host_thumbnails" : "http://192.168.28.75/vitrivr/thumbnails/",
    "host_object": "http://192.168.28.75/vitrivr/thumbnails",
    "suffix_default":".jpg",
    "suffix": {
      "IMAGE": "png",
      "VIDEO": "png"
    }
  },
  "evaluation": {
    "active":false,
    "templates":[
      {"name":"Testset A", "url":"http://192.168.28.75/vitrivr/testset/evaluation_a.json"},
      {"name":"Testset B", "url":"http://192.168.28.75/vitrivr/testset/evaluation_b.json"}
    ]
  },
  "queryContainerTypes":{
    "image": true,
    "text" : true,
    "audio": false,
    "model3d": false,
    "motion": false
  }
}
~~~

Sửa file cấu hình tại địa chỉ `\vitrivr-ng-1.0.2\src\app\core\basics\config.model.ts`

~~~
export class Config {
    ...
    private api = {
        host : "192.168.28.75",
        port : 8080,
        protocol_http: "http",
        protocol_ws: "ws",

        /* Default ping interval in milliseconds. */
        ping_interval: 10000
    };

    /**
     * Contains information concerning access to resources like multimedia objects
     * and thumbnails for preview.
     *
     * @type {{}}
     */
    private resources = {
        /** Path / URL to location where media object thumbnails will be stored. */
        host_thumbnails: "http://192.168.28.75/vitrivr",

        /** Path / URL to location where media object's will be stored. */
        host_object: "http://192.168.28.75/vitrivr",

        /** Default suffix for thumbnails. */
        suffix_default: ".jpg",

        /** Per-mediatype suffix definition for thumbnails. */
        suffix: {}
    };
    ...
}
~~~

**Chú ý sửa địa chỉ IP đúng với địa chỉ IP trên server.**

Chạy lần lượt các lệnh sau cài đặt Angular để build project ra thư mục `dist`:

~~~
cd vitrivr-ng
npm install
npm install -g @angular/cli
ng build --prod
~~~

Cài đặt `Nginx`, tạo file `vitrivr.conf` trong thư mục `conf.d` (nếu chưa có thì tạo thư mục `conf.d` trong thư mục `Nginx`) có nội dung như sau:

~~~
server {
    listen      80;
    server_name localhost;
    root        C:/vitrivr-ng-1.0.2/dist;
    index       index.html;

    location / {
        try_files   $uri $uri/ /index.html;
    }
}
~~~

Trong đó, `C:/vitrivr-ng-1.0.2/dist;` là đường dẫn thư mục vừa build ở trên. Nếu port 80 đã được sử dụng thì thay bằng port khác.

Mở `Command Prompt` hoặc `PowerShell`, mở thư mục Nginx rồi chạy lệnh sau:

~~~
start nginx
~~~

Truy cập địa chỉ `127.0.0.1` để bắt đầu sử dụng Vitrivr trên trình duyệt web.

Để dừng nginx, chạy lệnh:

~~~
.\nginx.exe -s quit
~~~
