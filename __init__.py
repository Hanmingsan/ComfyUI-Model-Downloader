from .civitai_downloader import CivitaiDownloader
from .hf_downloader import HFDownloader

NODE_CLASS_MAPPINGS = \
        {
    "CivitaiDownloader": CivitaiDownloader,
    "HFDownloader":      HFDownloader,
}

NODE_DISPLAY_NAME_MAPPINGS = \
        {
    "CivitaiDownloader": "Civitai Model Downloader",
    "HFDownloader":      "Hugging Face Model Downloader",

}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
