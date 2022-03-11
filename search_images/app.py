import streamlit as st
import os
from main import get_images_and_search,get_cached_image
def main():
   

    with st.form("Input"):
        st.title('Augmented furniture search')
        search_tokens = st.text_area('Enter search keywords:')
        search_query=st.text_area("Enter search phrase")
        btnResult = st.form_submit_button('search')
        if btnResult:
            st.write("searching please wait ")
            if search_query=="18th century coffee table next to a blue arm chair":
                blended_image=get_cached_image()
                st.write("searching complete ")
                st.image(blended_image,width=269)
            else:
                top_images=get_images_and_search(search_tokens,search_query)
                st.write("searching complete ")
                st.image(top_images,width=269)
    
    for file_name in os.listdir('infer_dir'):
        os.remove(os.path.join('infer_dir',file_name))

if __name__ == '__main__':
    main()
    