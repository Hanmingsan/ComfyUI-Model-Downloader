import os
import folder_paths
import requests
import re
import tqdm

class HFDownloader:
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        models_folders = [d for d in os.listdir(folder_paths.models_dir) if os.path.isdir(os.path.join(folder_paths.models_dir, d))]
        return {
            "required": {
                # Format: "name": ("TYPE", {"default": value, "min": min, "max": max})
                "model_url": ("STRING", {"multiline": False, "default": "",}),
                "save_dir": (models_folders,),
            },
            "optional": {
                "api_key" : ("STRING", {"multiline": False, "default": "",}),
                "file_name":("STRING", {"multiline": False, "default": "",}), # this is depricated as there is a model name given by cvt. maybe one kindly as you would like to realize this function?
            },
            "hidden":   {
                
            }
        }
        
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("download_path",)
    FUNCTION = "download_model_HF"
    CATEGORY = "Comfy_Model_Downloader"
    
    def download_model_HF(self, model_url, save_dir, api_key="", file_name="",):
        
        try:
            if not re.match(r"^https://huggingface\.co/(?P<user>[\w\.-]+)/(?P<repo>[\w\.-]+)/resolve/(?P<revision>[\w\.-]+)/(?P<file_path>.+)$", model_url):
                raise ValueError("The given model_url is probably invalid...")
            # This case is for full params
            if api_key:
                headers={}
                headers["Authorization"] = f"Bearer {api_key}"
            else:
                headers={}
            
            r = requests.get(model_url, headers = headers, stream = True)

            if not r.status_code == 200:
                raise ValueError(f"Download failed with http code {r.status_code}")
                
            # Get file name here!
            if not file_name:
                if "Content-Disposition" in r.headers and re.findall(r'filename="?([^"]+)"?', r.headers["Content-Disposition"]):
                        file_name = re.findall(r'filename="?([^"]+)"?', r.headers["Content-Disposition"])[0]
                else:
                    raise ValueError("You did not name your file, nor did HF...")
                    
            # Get content-length for calc
            file_size = int(r.headers['content-length'] if 'content-length' in r.headers else 0)

            chunk_size = 1024*1024

            progress_bar = tqdm.tqdm(total=file_size, unit='iB', unit_scale=True)

            with open(os.path.join(folder_paths.models_dir, save_dir, file_name), 'xb') as f:
                for chunk in r.iter_content(chunk_size=1024*1024):
                    progress_bar.update(len(chunk))
                    f.write(chunk)

            if file_size != 0 and progress_bar.n != file_size:
                raise RuntimeError("Uknown Issue Occured")
        
            return (f"Model successfully downloaded into {os.path.join(folder_paths.models_dir, save_dir, file_name)}",)
        
        except FileNotFoundError:
            return ("file not found",)
        
        except ValueError as e:
            return (f"download failed due to {e}",)
            
        except RuntimeError as e:
            return ("idk...",)
            
        except Exception as e:
            return (f"Unexcepted Error: {e}",)


