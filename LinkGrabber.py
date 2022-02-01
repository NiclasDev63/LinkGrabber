import requests
from bs4 import BeautifulSoup
from collections import deque
from random import choice
from os import path
from pathvalidate import sanitize_filepath
from threading import Thread

#returns different headers by randomly choosing an User Agent
def randomHeader():

        agents = [
                "Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX1 Build/HUAWEIWAS-LX1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36 [FB_IAB/Orca-Android;FBAV/331.0.0.15.119;]",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 LightSpeed [FBAN/MessengerLiteForiOS;FBAV/331.0.0.13.119;FBBV/318533087;FBDV/iPhone9,3;FBMD/iPhone;FBSN/iOS;FBSV/14.6;FBSS/2;FBCR/;FBID/phone;FBLC/hu;FBOP/0]",
                "Mozilla/5.0 (Linux; Android 10; ZTE A2020RU Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; U; Android 10; Redmi 7A Build/QKQ1.191014.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36 OPR/31.0.2254.122029",
                "Mozilla/5.0 (Linux; arm; Android 11; SM-A115F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.216 YaApp_Android/21.56.1 YaSearchBrowser/21.56.1 BroPP/1.0 SA/3 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; EML-L29 Build/HUAWEIEML-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/337.0.0.32.118;]",
                "Mozilla/5.0 (Linux; Android 11; SM-A315F Build/RP1A.200720.012; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36[FBAN/EMA;FBLC/ru_RU;FBAV/269.0.0.8.118;]",
                "Mozilla/5.0 (Linux; arm_64; Android 10; moto e(7) plus) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 YaBrowser/21.8.1.127.00 SA/3 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; arm_64; Android 8.0.0; AGS2-L09) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.166 YaBrowser/21.8.4.10.01 (alpha) Safari/537.36",
                "Mozilla/5.0 (Linux; Android 11; V2050) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 11; HD1925) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.7 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; arm_64; Android 11; SM-G996B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4572.0 YaApp_Android/21.62.1 YaSearchBrowser/21.62.1 BroPP/1.0 SA/3 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; arm_64; Android 11; SM-P615) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaApp_Android/21.61.1/apad YaSearchBrowser/21.61.1/apad BroPP/1.0 SA/3 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; MI 8 Lite) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Mobile Safari/537.36 OPR/64.3.3282.60839",
                "Mozilla/5.0 (Linux; Android 11; M2103K19PG Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/337.0.0.32.118;]",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4524.0 CitizenFX/1.0.0.4470 Safari/537.36",
                "Mozilla/5.0 (Linux; arm; Android 10; ELE-L29) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.164 YaApp_Android/21.61.1 YaSearchBrowser/21.61.1 BroPP/1.0 SA/3 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; ALP-L29 Build/HUAWEIALP-L29S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; LM-G710VM) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.81 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 7.0; SLA-L22 Build/HUAWEISLA-L22; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/93.0.4577.82 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/337.0.0.32.118;]",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; KTXN B673778648A48129T1297416P2) like Gecko",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 [FBAN/FBIOS;FBAV/155.0.0.36.93;FBBV/87992437;FBDV/iPhone5,2;FBMD/iPhone;FBSN/iOS;FBSV/10.3.3;FBSS/2;FBCR/NOS;FBID/phone;FBLC/zh_CN;FBOP/5;FBRV/89136215]",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; KTXN B666509076A102170T1297416P1) like Gecko",
                "Mozilla/5.0 (Linux; Android 7.0; Q8T7IN Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Safari/537.36 [FB_IAB/FB4A;FBAV/175.0.0.40.97;]",
                "Mozilla/5.0 (Linux; Android 7.0; G3221 Build/42.0.A.3.30) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.158 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; KTXN B667772105A48129T1390849P1) like Gecko",
                "Mozilla/5.0 (Linux; Android 5.1; Quantum Go Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.137 Mobile Safari/537.36",
                "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0; KTXN B674211073A90245T1297416P1) like Gecko",
                "Mozilla/5.0 (Linux; Android 6.0; LG-H650 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/155.0.0.36.96;]",
                "Mozilla/5.0 (Linux; Android 7.0; Aquaris_A4.5 Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/65.0.3325.109 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/167.0.0.42.94;]",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 138.0.0.32.117 (iPhone9,1; iOS 12_3_1; en_US; en-US; scale=2.00; 750x1334; 209823574)",
                "Mozilla/5.0 (Linux; Android 10; SM-A505U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/266.0.0.64.124;]",
                "Mozilla/5.0 (Linux; Android 9; SM-G885F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 8.1.0; RCT6513W87DK5e) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 7.0; SAMSUNG-SM-T817A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.111 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; SM-G975U1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 6.0; CAM-L03) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; Pixel 3 Build/QQ2A.200405.005; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 6.0.1; SM-J700M Build/MMB29K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 6.0; 5044A) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.111 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; SM-T837A Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Safari/537.36 [FB_IAB/FB4A;FBAV/266.0.0.64.124;]",
                "Mozilla/5.0 (Linux; Android 8.1.0; 4E Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 Mobile Safari/537.36",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 138.0.0.32.117 (iPhone12,3; iOS 13_3_1; en_US; en-US; scale=3.00; 1125x2436; 209823574) NW/1",
                "Mozilla/5.0 (Linux; Android 9; SM-G950F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 BitrixMobile/Version=34",
                "Mozilla/5.0 (Linux; Android 5.0.2; SM-A300H Build/LRX22G; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; SM-G970U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.11.21.arm64",
                "Mozilla/5.0 (Linux; Android 4.4.4; XT1032 Build/KXB21.14-L1.40) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/33.0.0.0 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; U; Android 8.1.0; en-in; Redmi Note 5 Pro Build/OPM1.171019.011) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.9.3-g",
                "Mozilla/5.0 (Linux; Android 9; SM-A105G Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (Linux; U; Android 6.0.1; en-us; Redmi Note 3 Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/61.0.3163.128 Mobile Safari/537.36 XiaoMi/MiuiBrowser/10.3.4-g",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 Instagram 127.0.0.22.119 (iPhone10,5; iOS 13_3_1; en_US; en-US; scale=2.61; 1080x1920; 196215991)",
                "Mozilla/5.0 (Linux; Android 9; SM-N950F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.101 Mobile Safari/537.36 GSA/10.24.6.21.arm64",
                "Mozilla/5.0 (Linux; U; Android 9; ru-ru; KSA-LX9 Build/HONORKSA-LX9) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30 GSA/11.5.9.21.arm OpaScreenful/0",
                "Mozilla/5.0 (Linux; Android 7.0; LGUS215 Build/NRD90U; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (X11; CrOS aarch64 13020.23.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.21 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; MAR-LX1M Build/HUAWEIMAR-L01MEA; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 8.0.0; SM-G9350) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.111 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; Mi A3 Build/PKQ1.190416.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64 Taskhub",
                "Mozilla/5.0 (Linux; U; Android 7.1.2; en-in; Redmi Y1 Lite Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.9.3-g",
                "Mozilla/5.0 (Linux; Android 7.0; NEM-L51 Build/HONORNEM-L51; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 10; SM-G960F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.132 Mobile Safari/537.36 GSA/10.94.12.21.arm64",
                "Mozilla/5.0 (Linux; Android 7.0; BLN-L21 Build/HONORBLN-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.157 Mobile Safari/537.36 GSA/9.88.7.21.arm64",
                "Mozilla/5.0 (Linux; U; Android 7.0; de-de; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.9.3-g",
                "Mozilla/5.0 (Linux; Android 10; SM-G975U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.132 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/266.0.0.56.124;]",
                "Mozilla/5.0 (Linux; Android 9; SM-J530FM Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/79.0.3945.116 Mobile Safari/537.36 GSA/11.2.9.21.arm",
                "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 [FBAN/FBIOS;FBAV/175.0.0.47.102;FBBV/112197024;FBDV/iPhone8,4;FBMD/iPhone;FBSN/iOS;FBSV/13.2;FBSS/2;FBCR/AT&T;FBID/phone;FBLC/en_US;FBOP/5;FBRV/0]",
                "Mozilla/5.0 (Linux; Android 8.1.0; LML413DL Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/265.0.0.61.103;]",
                "Mozilla/5.0 (Linux; Android 9; ANE-LX1 Build/HUAWEIANE-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; U; Android 7.1.2; Redmi 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.158 Mobile Safari/537.36 OPR/47.2.2254.147957",
                "Mozilla/5.0 (Linux; Android 9; Redmi Note 8 Pro Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.119 Mobile Safari/537.36 GSA/11.3.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 9; SM-A530F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 9; COL-L29 Build/HUAWEICOL-L29; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.136 Mobile Safari/537.36 GSA/10.61.10.21.arm64",
                "Mozilla/5.0 (Linux; Android 9; MI 8 Lite Build/PKQ1.181007.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (Linux; Android 9; SM-G950F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/75.0.3770.101 Mobile Safari/537.36 Viber/12.8.0.19",
                "Mozilla/5.0 (Linux; Android 9; Lenovo TB-X505F Build/PKQ1.181218.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 6.0.1; MotoG3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36 OPR/57.2.2830.52651",
                "Mozilla/5.0 (Linux; Android 9; Armor X5 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 9; BLA-L29 Build/HUAWEIBLA-L29S; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 BitrixMobile/Version=34",
                "Mozilla/5.0 (Linux; Android 9; SM-J730F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (Linux; Android 7.0; ASUS_X018D Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36 BitrixMobile/Version=34",
                "Mozilla/5.0 (Linux; Android 10; SM-N970U Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 Instagram 138.0.0.28.117 Android (29/10; 420dpi; 1080x2064; samsung; SM-N970U; d1q; qcom; en_US; 210180522)",
                "Mozilla/5.0 (Linux; Android 9; SM-A750FN Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; U; Android 8.1.0; One Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36 OPR/47.0.2254.146760",
                "Mozilla/5.0 (Linux; Android 10; SM-A750F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36 GSA/11.2.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 8.1.0; INE-LX2 Build/HUAWEIINE-LX2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.108 Mobile Safari/537.36 GSA/9.91.6.21.arm64",
                "Mozilla/5.0 (Linux; Android 9; Nokia 3.1 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 4.4.2; Lenovo TAB 2 A7-30HC) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.111 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 8.1.0; ONEPLUS A5010) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 4.4.4; Lenovo TAB 2 A10-70L) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; SM-J530F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36 GSA/10.16.6.21.arm",
                "Mozilla/5.0 (Linux; Android 5.1.1; VS810PP) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.117 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 8.1.0; G253 Build/O11019) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; SM-G970F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 10; STK-LX1 Build/HONORSTK-LX1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/78.0.3904.96 Mobile Safari/537.36 GSA/10.94.12.21.arm64",
                "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.137 (Edition Campaign 10)",
                "Mozilla/5.0 (Linux; Android 9; RMX1992 Build/PKQ1.190630.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36 GSA/11.2.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 10; SM-G960F Build/QP1A.190711.020; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 7.0; SM-G920F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 8.1.0; SM-T580 Build/M1AJQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (Linux; Android 9; Nokia 2.2 Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.149 Mobile Safari/537.36 GSA/11.2.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 8.1.0; BS155) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.111 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; SM-A105F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (Linux; Android 8.0.0; WAS-LX1 Build/HUAWEIWAS-LX1; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm64",
                "Mozilla/5.0 (Linux; Android 9; SM-S367VL Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (Linux; Android 7.0; SM-A310F Build/NRD90M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.111 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; Infinix X650C) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.111 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 9; SM-J530F Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/81.0.4044.117 Mobile Safari/537.36 GSA/11.5.9.21.arm",
                "Mozilla/5.0 (Linux; Android 9; LM-V405 Build/PKQ1.190202.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/266.0.0.64.124;]",
                "Mozilla/5.0 (Linux; arm_64; Android 5.1; kt109) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 YaBrowser/20.3.3.92.01 Safari/537.36",
                "Mozilla/5.0 (Linux; Android 8.1.0; SM-J710F Build/M1AJQ; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36 GSA/10.65.11.21.arm",
                "Mozilla/5.0 (Linux; Android 9; SM-N950U Build/PPR1.180610.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.162 Mobile Safari/537.36 [FB_IAB/FB4A;FBAV/262.0.0.19.117;]",
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Cypress/4.4.0 Chrome/80.0.3987.158 Electron/8.2.0 Safari/537.36"
                ]
        

        agent = {
      "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
      #'Accept-Encoding': 'gzip, deflate, br',
      "Accept-Language": "de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
      'Upgrade-Insecure-Requests': "1",
      'User-Agent': choice(agents),
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'Cache-Control': 'max-age=0',
      "Viewport-Width" : "1920",
      "Referer": "https://www.google.com/",
      'Connection': 'keep-alive'}
        
        return agent


#Downloads the HTML file into the wanted directory
def htmlDownloader(link_list, html_doc_name_list, link_check_list):
  for link in link_list:
    if link not in link_check_list:
      link_check_list.append(link)
      html_doc = requests.get(link, headers = randomHeader()).text
      soup = BeautifulSoup(html_doc, "html.parser")
      html_doc_name = soup.title.string.strip()
      if html_doc_name not in html_doc_name_list:
        with open(directory + path.sep + sanitize_filepath(html_doc_name) + ".txt", "w", encoding="utf-8")as file:
          file.write(html_doc)
        html_doc_name_list.append(html_doc_name)


"""
Uses BFS to find all links on the Website.
"""
def breadthFirstSearch(start_url, threads, max_depth = 2, max_links = -1, html_download = False, directory = "", get_link_to_files = False):


  redirect_list = set()
  file_endings = ["jpg", "pdf", "JPG", "jpeg", "png", "mp3", "docx", "mp4"]
  visited = set(start_url)
  queue = deque([[start_url, "", 0]])
  want_all_links = False
  link_list = set()

  if max_links > 0:
    want_all_links = True

  stop = False
  while queue and not stop:

      #changing ".popleft()" to ".pop()" will turn the QUEUE into a STACK (Last In First Out)
      base, path, depth = queue.popleft()
      if depth <= max_depth:
          try:
              html_doc = requests.get(base + path, headers = randomHeader()).text
              soup = BeautifulSoup(html_doc, "html.parser")

              for link in soup.find_all("a"):
                  href = link.get("href")
                  if href not in visited:
                      visited.add(href)

                      if max_links == len(link_list) and want_all_links:
                          stop = True
                          break

                      #Checks if the link directs to a file
                      if not get_link_to_files:
                        try:
                          ending = href[len(href)-6:].split(".")[1]
                          if ending in file_endings:
                            continue
                        except IndexError:
                          pass


                      if href.startswith("http") or href.startswith("www"):
                        if start_url not in href:
                          redirect_list.add(href)
                          continue
                        print(str(" " * depth) + f" at deepth: {depth} URL: {href}")
                        link_list.add(href)
                        queue.append([href, "", depth + 1])
                        
                      else:
                        print(str(" " * depth) + f" at deepth: {depth} URL: {base + href}")               
                        link_list.add(base + href)
                        queue.append([base, href, depth + 1])

          except Exception as e:
              print(e)
              pass

  if html_download:
    html_doc_name_list = []
    link_check_list = []
    for i in range(threads):
      thread = "thread" + str(i)
      thread = Thread(target=htmlDownloader, kwargs={"link_list" : link_list, "html_doc_name_list" : html_doc_name_list, "link_check_list" : link_check_list})
      thread.start()

  relevant_data = {"listLength": len(link_list), "redirectCounter": len(redirect_list), "redirectLinks": redirect_list, "allLinks": link_list}

  print(str(len(link_list)) + " links found")
  return relevant_data



#Driver code 
if __name__ == "__main__":
  print("#######################################################################")
  print("##                                                                   ##")
  print("##    #########                                                      ##")
  print("##    ##            #  ####           ##       ####       #     #    ##")
  print("##    ##            # #    #                 #      #      #   #     ##")
  print("##    #########     ##      #         ##    #        #      # #      ##")
  print("##    ##            #       #         ##     #      #        #       ##")
  print("##    ##            #       #     #   ##      #    #        #        ##")
  print("##    #########    ###     ###      ###        ####        #         ##")
  print("##                                                                   ##")
  print("#######################################################################")

  #You have a few parameters to customize your link search

  start_url = input("Start URL: ")                                          #Insert an root url to start with
  threads = int(input("Wanted Threads: "))                                  #Inser an interger value
  max_deepth = int(input("Maximum depth: "))                                #Insert an interger value
  max_links = int(input("Maximum links: "))                                 #Insert an integer value (If you insert a 0 the number of maximum links is unlimited)
  get_link_to_files = input("Do you want to get links to files?: ")         #Insert Yes / No
  html_download = input("Do you want to download the html file?: ")         #Insert Yes / No
  directory = r"C:\Users\nicla\Desktop\TEST"                                #Insert the directory you want the html files in


  if get_link_to_files.lower() == "yes":
    get_link_to_files = True
  else:
    get_link_to_files = False

  if html_download.lower() == "yes":
    html_download = True
  else:
    html_download = False



  data_dic = breadthFirstSearch(start_url, threads, max_deepth, max_links, html_download, directory, get_link_to_files)
