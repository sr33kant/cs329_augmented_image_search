# FROM pytorch/pytorch:latest
# WORKDIR /app
FROM pytorch/pytorch:1.9.1-cuda11.1-cudnn8-runtime
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN mkdir tocrop cropped models
COPY mask_display.png tocrop/
COPY mask_coffee.png tocrop/
COPY scaledbigliving.png tocrop/
COPY unsupervised_blending_gan.npz models/ 
COPY *.py .
EXPOSE 8080
CMD [ "python3", "main.py" ]
