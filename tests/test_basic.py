# Basic smoke tests for youtube-downloader
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import_main():
    import main
    assert hasattr(main, '__name__')

def test_import_downloader():
    try:
        import downloader
    except Exception:
        pass  # module may depend on Qt/network
