import google.cloud.logging
import logging
import time
import os
from PIL import Image
from google.cloud import storage
client = google.cloud.logging.Client()
client.setup_logging()
storage_client = storage.Client()
def search_by_keyword_download_all(bucket_name,prefix,delimiter=None):
    """Lists all the blobs in the bucket."""
  

    blobs = storage_client.list_blobs(bucket_name,prefix=prefix)
    if blobs:
      for idx,val in enumerate(blobs):
            if idx >0:
              val.download_to_filename(os.path.join('infer_dir',str(val.name).split('/')[1]))
          
    return 100   

def fetch_images(search_tags):
    images_list=[]
    for tag in search_tags.split(','):
      assert search_by_keyword_download_all("imagesearch-cs329s",tag.lstrip())==100
    gcs_list=os.listdir('infer_dir')
    for gcs_file in gcs_list:
      image=Image.open('infer_dir/'+gcs_file).convert("RGB")
      images_list.append(image)
    return images_list

   