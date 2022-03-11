import argparse
import os

import chainer
from chainer import cuda, serializers
from skimage import img_as_float
from skimage.io import imread, imsave

from gp_gan import gp_gan
from model import EncoderDecoder, DCGAN_G

basename = lambda path: os.path.splitext(os.path.basename(path))[0]

"""
    Note: source image, destination image and mask image have the same size.
"""


def runner(sourceIMG, destinIMG, maskIMG, blend_id, supervised=False):
    # parser = argparse.ArgumentParser(description='Gaussian-Poisson GAN for high-resolution image blending')
    # parser.add_argument('--nef', type=int, default=64, help='# of base filters in encoder')
    nef = 64
    # parser.add_argument('--ngf', type=int, default=64, help='# of base filters in decoder or G')
    ngf = 64
    # parser.add_argument('--nc', type=int, default=3, help='# of output channels in decoder or G')
    nc = 3
    # parser.add_argument('--nBottleneck', type=int, default=4000, help='# of output channels in encoder')
    nBottleneck = 4000
    # parser.add_argument('--ndf', type=int, default=64, help='# of base filters in D')
    ndf = 64
    # parser.add_argument('--image_size', type=int, default=64, help='The height / width of the input image to network')
    image_size = 64
    # parser.add_argument('--color_weight', type=float, default=1, help='Color weight')
    color_weight = 1
    # parser.add_argument('--sigma', type=float, default=0.5,
    #                     help='Sigma for gaussian smooth of Gaussian-Poisson Equation')
    sigma = 0.5
    # parser.add_argument('--gradient_kernel', type=str, default='normal', help='Kernel type for calc gradient')
    gradient_kernel = 'normal'
    # parser.add_argument('--smooth_sigma', type=float, default=1, help='Sigma for gaussian smooth of Laplacian pyramid')
    smooth_sigma = 1
    # parser.add_argument('--supervised', type=lambda x: x == 'True', default=True,
    #                     help='Use unsupervised Blending GAN if False')
    supervised = False
    # parser.add_argument('--nz', type=int, default=100, help='Size of the latent z vector')
    nz = 100
    # parser.add_argument('--n_iteration', type=int, default=1000, help='# of iterations for optimizing z')
    n_iteration = 10000
    # parser.add_argument('--gpu', type=int, default=0, help='GPU ID (negative value indicates CPU)')
    gpu = 0
    # parser.add_argument('--g_path', default='models/blending_gan.npz', help='Path for pretrained Blending GAN model')
    g_path = 'models/blending_gan.npz'
    # parser.add_argument('--unsupervised_path', default='models/unsupervised_blending_gan.npz',
    #                     help='Path for pretrained unsupervised Blending GAN model')
    unsupervised_path='models/unsupervised_blending_gan.npz'
    # parser.add_argument('--list_path', default='',
    #                     help='File for input list in csv format: obj_path;bg_path;mask_path in each line')
    list_path =''
    # parser.add_argument('--result_folder', default='blending_result', help='Name for folder storing results')
    result_folder = 'blending_result'
    # parser.add_argument('--src_image', default='', help='Path for source image')
    src_image = sourceIMG
    # parser.add_argument('--dst_image', default='', help='Path for destination image')
    dst_image = destinIMG
    # parser.add_argument('--mask_image', default='', help='Path for mask image')
    mask_image = maskIMG
    # parser.add_argument('--blended_image', default='', help='Where to save blended image')
    blended_image = blend_id
    # args = parser.parse_args()

    # print('Input arguments:')
    # for key, value in vars(args).items():
    #     print('\t{}: {}'.format(key, value))
    # print('')

    # Init CNN model
    if supervised:
        G = EncoderDecoder(nef, ngf, nc, nBottleneck, image_size=image_size)
        print('Load pretrained Blending GAN model from {} ...'.format(g_path))
        serializers.load_npz(g_path, G)
    else:
        chainer.config.use_cudnn = 'never'
        G = DCGAN_G(image_size, nc, ngf)
        print('Load pretrained unsupervised Blending GAN model from {} ...'.format(unsupervised_path))
        serializers.load_npz(unsupervised_path, G)

    if gpu >= 0:
        cuda.get_device(gpu).use()  # Make a specified GPU current
        G.to_gpu()  # Copy the model to the GPU

    # Init image list
    if list_path:
        print('Load images from {} ...'.format(list_path))
        with open(list_path) as f:
            test_list = [line.strip().split(';') for line in f]
        print('\t {} images in total ...\n'.format(len(test_list)))
    else:
        test_list = [(src_image, dst_image, mask_image)]

    if not blended_image:
        # Init result folder
        if not os.path.isdir(result_folder):
            os.makedirs(result_folder)
        print('Result will save to {} ...\n'.format(result_folder))

    total_size = len(test_list)
    for idx in range(total_size):
        print('Processing {}/{} ...'.format(idx + 1, total_size))

        # load image
        obj = img_as_float(imread(test_list[idx][0]))
        bg = img_as_float(imread(test_list[idx][1]))
        mask = imread(test_list[idx][2], as_gray=True).astype(obj.dtype)

        with chainer.using_config("train", False):
            blended_im = gp_gan(obj, bg, mask, G, image_size, gpu, color_weight=color_weight,
                                sigma=sigma,
                                gradient_kernel=gradient_kernel, smooth_sigma=smooth_sigma,
                                supervised=supervised,
                                nz=nz, n_iteration=n_iteration)

        if blended_image:
            imsave(blended_image, blended_im)
        else:
            imsave('{}/obj_{}_bg_{}_mask_{}.png'.format(result_folder, basename(test_list[idx][0]),
                                                        basename(test_list[idx][1]), basename(test_list[idx][2])),
                   blended_im)
