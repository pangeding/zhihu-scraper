import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime


def load_cookies_from_file(cookie_file='cookie.txt'):
    """Load cookies from a file"""
    cookies = {}
    if os.path.exists(cookie_file):
        with open(cookie_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            # Parse cookie string like "key1=value1; key2=value2"
            for item in content.split(';'):
                item = item.strip()
                if '=' in item:
                    key, value = item.split('=', 1)
                    cookies[key.strip()] = value.strip()
    return cookies


def scrape_zhihu(url, cookies=None):
    """
    Scrape main content from Zhihu article or question

    Args:
        url: Zhihu article URL or question URL
        cookies: Optional session cookies (e.g. {'session_id': '...'})

    Returns:
        Extracted article text or error message
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }

    try:
        response = requests.get(url, headers=headers, cookies=cookies, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check if it's a specific answer URL (/answer/)
        if '/answer/' in url:
            return scrape_single_answer(soup)
        # Check if it's a question page (multiple answers)
        elif '/question/' in url:
            return scrape_question_answers(soup)
        else:
            # It's an article page
            return scrape_article_content(soup)

    except requests.exceptions.RequestException as e:
        return f"ERROR: Request failed - {str(e)}"


def scrape_single_answer(soup):
    """Scrape a single answer from an answer URL"""
    results = []
    
    # Try to find the answer container
    answer_items = soup.find_all('div', class_='List-item')
    
    if not answer_items:
        # Fallback to RichContent
        answer_items = soup.find_all('div', class_='RichContent')
    
    if not answer_items:
        # Try to find by content directly
        content_div = soup.find('div', class_='RichContent-inner')
        if content_div:
            answer_items = [content_div]
    
    print(f"\nFound {len(answer_items)} answer on this page")
    
    for i, item in enumerate(answer_items, 1):
        # Extract answer content
        content_div = item.find('div', class_='RichContent-inner')
        if not content_div:
            content_div = item
        
        if content_div:
            paragraphs = content_div.find_all('p')
            answer_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
            
            # Extract author name
            author_elem = item.find('a', class_='UserLink-link')
            if not author_elem:
                author_elem = item.find('a', class_='zm-item-answer-author-link')
            author = author_elem.get_text(strip=True) if author_elem else "匿名用户"
            
            # Extract vote count
            vote_elem = item.find('button', class_='VoteButton')
            votes = vote_elem.get_text(strip=True) if vote_elem else "0"
            
            results.append(f"【回答】作者：{author} | 赞同：{votes}\n{answer_text}")
    
    if results:
        return "\n\n" + "="*80 + "\n".join(results) + "\n" + "="*80
    else:
        return "ERROR: No answer found on this page"


def scrape_question_answers(soup):
    """Scrape all answers from a question page"""
    results = []
    
    # Find all answer containers
    answer_items = soup.find_all('div', class_='List-item')
    
    if not answer_items:
        # Fallback to old structure
        answer_items = soup.find_all('div', class_='zm-item-answer')
    
    print(f"\nFound {len(answer_items)} answers on this page")
    
    for i, item in enumerate(answer_items, 1):
        # Extract answer content
        content_div = item.find('div', class_='RichContent-inner')
        if not content_div:
            content_div = item.find('div', class_='zm-item-rich-text')
        
        if content_div:
            paragraphs = content_div.find_all('p')
            answer_text = '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
            
            # Extract author name
            author_elem = item.find('a', class_='UserLink-link')
            if not author_elem:
                author_elem = item.find('a', class_='zm-item-answer-author-link')
            author = author_elem.get_text(strip=True) if author_elem else "匿名用户"
            
            # Extract vote count
            vote_elem = item.find('button', class_='VoteButton')
            votes = vote_elem.get_text(strip=True) if vote_elem else "0"
            
            results.append(f"【回答 {i}】作者：{author} | 赞同：{votes}\n{answer_text}")
    
    if results:
        return "\n\n" + "="*80 + "\n".join(results) + "\n" + "="*80
    else:
        return "ERROR: No answers found on this question page"


def scrape_article_content(soup):
    """Scrape content from an article page"""
    content_div = None
    
    # Try multiple selectors for Zhihu content
    content_div = soup.find('div', class_='Post-RichText')
    
    # Method 2: Look for RichContent-inner (for answers)
    if not content_div:
        content_div = soup.find('div', class_='RichContent-inner')
    
    # Method 3: Fallback to itemprop (old method)
    if not content_div:
        content_div = soup.find(itemprop='text')
    
    if content_div:
        # Extract all text while preserving paragraph structure
        paragraphs = content_div.find_all('p')
        return '\n\n'.join(p.get_text(strip=True) for p in paragraphs)
    else:
        return "ERROR: Content container not found. The page structure may have changed."


def save_to_file(content, title_prefix=""):
    """Save content to data folder with date-based filename
    
    Args:
        content: The content to save
        title_prefix: Optional prefix for the filename (Chinese characters)
    
    Returns:
        The output file path
    """
    # Create data directory if it doesn't exist
    data_dir = 'data'
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    # Generate filename with date
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    # Limit title prefix to first 30 Chinese characters
    if title_prefix:
        # Extract Chinese characters (limit to 30)
        chinese_chars = []
        for char in title_prefix[:200]:  # Check first 200 chars to get enough Chinese
            if '\u4e00' <= char <= '\u9fff':  # Unicode range for Chinese characters
                chinese_chars.append(char)
                if len(chinese_chars) >= 30:
                    break
        title_part = ''.join(chinese_chars)
        if title_part:
            filename = f"{date_str}-{title_part}.md"
        else:
            filename = f"{date_str}-zhihu.md"
    else:
        filename = f"{date_str}-zhihu.md"
    
    output_file = os.path.join(data_dir, filename)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_file


if __name__ == "__main__":
    print("Zhihu Article Scraper")
    print("=====================")
    url = input("Enter Zhihu article URL: ").strip()

    # Try to load cookies from file first
    cookies = load_cookies_from_file('cookie.txt')
    
    if cookies:
        print(f"Loaded {len(cookies)} cookies from file")
    else:
        print("No cookie file found or file is empty")
        use_cookies = input("Use cookies? (y/n): ").lower() == 'y'
        if use_cookies:
            print("Enter cookies as key=value pairs (one per line, empty line to finish):")
            while True:
                cookie = input().strip()
                if not cookie:
                    break
                if '=' in cookie:
                    key, value = cookie.split('=', 1)
                    cookies[key] = value

    result = scrape_zhihu(url, cookies)

    if result.startswith('ERROR'):
        print(f"\n{result}")
        print("\nTroubleshooting:")
        print("- Check if the URL is correct")
        print("- Try adding session cookies if the article requires login")
        print("- Update User-Agent if blocked")
    else:
        # Extract title from URL or content for filename
        title_prefix = ""
        if result and len(result) > 0:
            # Try to extract first few Chinese characters from content
            title_prefix = result
        
        output_file = save_to_file(result, title_prefix)
        print(f"\nContent saved to {output_file}")
        print("\nFirst 200 characters:\n" + result[:200] + "...")    