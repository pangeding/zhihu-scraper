# Zhihu Article Scraper

A Python script to extract main content from Zhihu (知乎) articles.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![Dependencies](https://img.shields.io/badge/Dependencies-requests%20%7C%20beautifulsoup4-orange)

## Features

- Extracts clean text content from Zhihu articles
- Preserves paragraph structure
- Supports cookie authentication for login-required content
- Error handling and troubleshooting guidance
- Saves output to UTF-8 encoded text file

## Installation


在浏览器的console里搜索document.cookie,然后就可以找到cookie 复制到cookie.txt里

```bash
uv pip install requests beautifulsoup4
```

## Usage

```bash
source .venv/bin/activate
python zhihu_scraper.py
echo "https://www.zhihu.com/question/1920630198509995936/answer/2021915304188543089" | python zhihu_scraper.py

```

1. Enter the Zhihu article URL when prompted
2. Choose whether to use cookies (required for some content)
3. If using cookies, enter them as `key=value` pairs (one per line)
4. The extracted content will be saved to `zhihu_content.txt`

## Cookie Configuration

To access protected content:

1. Get cookies from your browser:
   - Open Zhihu in browser
   - Open DevTools (F12)
   - Go to Application > Cookies
   - Copy relevant cookies (usually `sessionid`, `z_c0`)

2. When prompted:
   ```
   Enter cookies as key=value pairs (one per line, empty line to finish):
   sessionid=your_session_id
   z_c0=your_z_c0_value
   \n
   ```

## Output

- Content saved to `zhihu_content.txt`
- First 200 characters displayed for verification
- Example output:
  ```
  Content saved to zhihu_content.txt

  First 200 characters:
  本文超过8500字，阅读量超过9.9w，快要破10万阅读，记录的是Stag1：2022年暑假到2023年底的故事。 Stag2：2024上半年的故事，点击(华为是一家怎样的公司？ - 知乎 (zhihu.com) Stag3:  2025年6月已离职，点击为什么...
  ```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Content container not found | Zhihu may have updated their page structure - check `itemprop="text"` element |
| 403 Forbidden | Update User-Agent header or add more cookies |
| Login required content | Ensure you're providing valid session cookies |
| Encoding issues | Script uses UTF-8 - verify your terminal supports it |

## Notes

⚠️ **Please note**:
- Always respect [Zhihu's terms of service](https://www.zhihu.com/terms)
- Do not scrape at high frequency or for commercial purposes without permission
- Some articles may require additional headers or more complex authentication
- This tool is designed for personal educational use only