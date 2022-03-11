from perform_search import Searcher
import os
from PIL import Image
import google.cloud.logging
client = google.cloud.logging.Client()
client.setup_logging()
from gs_utils import fetch_images

searcher = Searcher()
def get_images_and_search(search_tags,query_phrase):
    images_list=fetch_images(search_tags)
    top_images,top_scores=searcher.get_similar_images(images_list,query_phrase,top_k=3)
    print(top_scores)
    return top_images

def get_cached_image():
    blended_image=Image.open('blended_image/'+'blended_image.jpeg').convert("RGB")
    return blended_image