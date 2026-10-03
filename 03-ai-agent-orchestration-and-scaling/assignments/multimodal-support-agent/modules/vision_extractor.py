import os, re

class VisionExtractor:
    """Mock vision extractor: extracts an error-like token from the filename or path.
    Example: 'mock_err_ERR504.png' -> 'ERR504: Gateway Timeout'"""
    def extract_from_path(self, path):
        # look for patterns like ERR123 or E201
        if not path:
            return ''
        base = os.path.basename(path)
        m = re.search(r'(ERR\d+|E\d{3}|ERROR_\d+)', base, re.IGNORECASE)
        if m:
            code = m.group(1).upper()
            if '504' in code:
                return f'{code}: Gateway Timeout'
            return f'{code}: Detected from image'
        # fallback: return filename as message
        return base
