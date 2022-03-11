from skimage.io import imread, imsave
import os
tocrop = os.path.join(os.getcwd(), 'tocrop')
cropped = os.path.join(os.getcwd(), 'cropped')
sx,sy,ex,ey = 4,5,476,494

# def cropper():
#     for img in os.listdir(tocrop):
#         #(root,ext) = os.path.splitext(img)
#         mask = imread(str(os.path.join(tocrop, img)))
#         cropped_mask = mask[sx:ex, sy:ey]
#         mask_name = "crop_" + str(img)
#         imsave(os.path.join(cropped, mask_name), cropped_mask)
#     # mask=imread('/app/tocrop/src_tst.jpg')
#     # cropped_mask=mask[sx:ex, sy:ey]



def cropper():
    for img in os.listdir(tocrop):
        #(root,ext) = os.path.splitext(img)
        mask = imread(str(os.path.join(tocrop, img)))
        cropped_mask = mask[sx:ex, sy:ey]
        mask_name = "crop_" + str(img)
        imsave(os.path.join(cropped, mask_name), cropped_mask)
    # mask=imread('/app/tocrop/src_tst.jpg')
    # cropped_mask=mask[sx:ex, sy:ey]
    # mask_src=imread(source_url)
    # cropped_mask = mask_src[sx:ex, sy:ey]
    # mask_name = "crop_src.jpg" 
    # imsave(os.path.join(cropped, mask_name), cropped_mask)

    # mask_dst=imread(dest_url)
    # cropped_mask = mask_dst[sx:ex, sy:ey]
    # mask_name = "crop_dest.jpg" 
    # imsave(os.path.join(cropped, mask_name), cropped_mask)

    # mask_dst=imread(os.path.join(os.getcwd(),'tocrop', 'mask_display.png'))
    # cropped_mask = mask_dst[sx:ex, sy:ey]
    # mask_name = "crop_mask_display.png" 
    # imsave(os.path.join(cropped, mask_name), cropped_mask)