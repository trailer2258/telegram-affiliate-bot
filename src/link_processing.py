import urllib.parse
import os
import re

def convert_affiliate_link(original_url):
    try:
        parsed = urllib.parse.urlparse(original_url)
        
        # Amazon
        if 'amazon.' in parsed.netloc and os.getenv('AMAZON_TAG'):
            query = urllib.parse.parse_qs(parsed.query)
            if 'tag' in query: 
                del query['tag']
            query['tag'] = os.getenv('AMAZON_TAG')
            new_query = urllib.parse.urlencode(query, doseq=True)
            return urllib.parse.urlunparse(parsed._replace(query=new_query))
        
        # Flipkart
        if 'flipkart.' in parsed.netloc and os.getenv('FLIPKART_AFFID'):
            sep = '&' if '?' in original_url else '?'
            return f"{original_url}{sep}affid={os.getenv('FLIPKART_AFFID')}"
        
        # Myntra
        if 'myntra.' in parsed.netloc and os.getenv('MYNTRA_PID'):
            sep = '&' if '?' in original_url else '?'
            return f"{original_url}{sep}pid={os.getenv('MYNTRA_PID')}"
        
        # EarnKaro
        earnkaro_url = os.getenv('EARNKARO_URL')
        if earnkaro_url:
            supported_domains = [
                'amazon.', 'flipkart.', 'myntra.', 'ajio.', 'nykaa.', 
                'tatacliq.', 'firstcry.', 'meesho.', 'shopclues.', 
                'zivame.', 'purplle.'
            ]
            if any(domain in parsed.netloc for domain in supported_domains):
                return f"{earnkaro_url}{urllib.parse.quote(original_url)}"
        
        return original_url
        
    except Exception as e:
        print(f"URL conversion error: {str(e)}")
        return original_url