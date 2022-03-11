FROM pytorch/pytorch
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir infer_dir model blended_image
RUN chmod 755 infer_dir
COPY blended_image.jpeg blended_image/
COPY main.py .
COPY app.py .
COPY gs_utils.py .
COPY perform_search.py .
COPY similarity_utils.py .
ENV REDIS_IN_USE="true"
ENV REDISHOST="10.247.231.219"
EXPOSE 8085
CMD conda run streamlit run app.py --server.port=8085  --browser.serverAddress="0.0.0.0"