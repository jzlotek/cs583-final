#
# train_Sony.py
#

from __future__ import division
import os, time
import tensorflow as tf
import tensorflow.contrib.slim as slim
import numpy as np
import imageio
import rawpy
import glob
import sys
import scipy.misc

# Constant
input_dir = './dataset/Sony/short/'
gt_dir = './dataset/Sony/long/'
checkpoint_dir = './result_Sony/'
result_dir = './result_Sony/'

# get train IDs
#
# Gets all the filenames that match the pattern
# Chops off the first 5 characters to get the file's "ID"
train_fns = glob.glob(gt_dir + '0*.ARW')
train_ids = [int(os.path.basename(train_fn)[0:5]) for train_fn in train_fns]

ps = 512  # patch size for training
save_freq = 500

DEBUG = 0
if DEBUG == 1:
    save_freq = 2
    train_ids = train_ids[0:5]

# Activation function
def lrelu(x):
    return tf.maximum(x * 0.2, x)


def upsample_and_concat(x1, x2, output_channels, in_channels):
    pool_size = 2
    deconv_filter = tf.Variable(tf.truncated_normal([pool_size, pool_size, output_channels, in_channels], stddev=0.02))
    deconv = tf.nn.conv2d_transpose(x1, deconv_filter, tf.shape(x2), strides=[1, pool_size, pool_size, 1])

    deconv_output = tf.concat([deconv, x2], 3)
    deconv_output.set_shape([None, None, None, output_channels * 2])

    return deconv_output

# Defines the structure of the model and handles running and input through it
def network(input):
    with tf.device('/gpu:0'):
        conv1 = slim.conv2d(input, 32, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv1_1')
        conv1 = slim.conv2d(conv1, 32, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv1_2')
        pool1 = slim.max_pool2d(conv1, [2, 2], padding='SAME')

        conv2 = slim.conv2d(pool1, 64, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv2_1')
        conv2 = slim.conv2d(conv2, 64, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv2_2')
        pool2 = slim.max_pool2d(conv2, [2, 2], padding='SAME')

        conv3 = slim.conv2d(pool2, 128, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv3_1')
        conv3 = slim.conv2d(conv3, 128, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv3_2')
        pool3 = slim.max_pool2d(conv3, [2, 2], padding='SAME')

        conv4 = slim.conv2d(pool3, 256, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv4_1')
        conv4 = slim.conv2d(conv4, 256, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv4_2')
        pool4 = slim.max_pool2d(conv4, [2, 2], padding='SAME')

        conv5 = slim.conv2d(pool4, 512, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv5_1')
        conv5 = slim.conv2d(conv5, 512, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv5_2')

        up6 = upsample_and_concat(conv5, conv4, 256, 512)
        conv6 = slim.conv2d(up6, 256, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv6_1')
        conv6 = slim.conv2d(conv6, 256, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv6_2')

        up7 = upsample_and_concat(conv6, conv3, 128, 256)
        conv7 = slim.conv2d(up7, 128, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv7_1')
        conv7 = slim.conv2d(conv7, 128, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv7_2')

        up8 = upsample_and_concat(conv7, conv2, 64, 128)
        conv8 = slim.conv2d(up8, 64, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv8_1')
        conv8 = slim.conv2d(conv8, 64, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv8_2')

        up9 = upsample_and_concat(conv8, conv1, 32, 64)
        conv9 = slim.conv2d(up9, 32, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv9_1')
        conv9 = slim.conv2d(conv9, 32, [3, 3], rate=1, activation_fn=lrelu, scope='g_conv9_2')

        conv10 = slim.conv2d(conv9, 12, [1, 1], rate=1, activation_fn=None, scope='g_conv10')
        out = tf.depth_to_space(conv10, 2)
    return out


def pack_raw(raw):
    # pack Bayer image to 4 channels
    im = raw.raw_image_visible.astype(np.float32)
    im = np.maximum(im - 512, 0) / (16383 - 512)  # subtract the black level

    im = np.expand_dims(im, axis=2)
    img_shape = im.shape
    H = img_shape[0]
    W = img_shape[1]

    out = np.concatenate((im[0:H:2, 0:W:2, :],
                          im[0:H:2, 1:W:2, :],
                          im[1:H:2, 1:W:2, :],
                          im[1:H:2, 0:W:2, :]), axis=2)
    return out

# Reset current tf globals
tf.reset_default_graph()

config = tf.ConfigProto()
config.gpu_options.allow_growth = True

sess = tf.Session(config=config)

in_image = tf.placeholder(tf.float32, [None, None, None, 4])
gt_image = tf.placeholder(tf.float32, [None, None, None, 3])
out_image = network(in_image)

G_loss = tf.reduce_mean(tf.abs(out_image - gt_image))

t_vars = tf.trainable_variables()
lr = tf.placeholder(tf.float32)
G_opt = tf.train.AdamOptimizer(learning_rate=lr).minimize(G_loss)

saver = tf.train.Saver()
sess.run(tf.global_variables_initializer())
ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
if ckpt:
    print('loaded ' + ckpt.model_checkpoint_path)
    saver.restore(sess, ckpt.model_checkpoint_path)

g_loss = np.zeros((5000, 1))

allfolders = glob.glob('./result/*0')
lastepoch = 0
for folder in allfolders:
    lastepoch = np.maximum(lastepoch, int(folder[-4:]))

# Batching
total_epochs = 1001 # 4001 was used in the paper, but takes a while
current_batch = 0
batch_size = 25 # Uses < 8gb of RAM
shuffled_ids = np.random.permutation(len(train_ids))

while (current_batch+1) * batch_size - 1 < len(shuffled_ids) :
    batch_ids = shuffled_ids[current_batch*batch_size:(current_batch+1)*batch_size-1]
    current_batch += 1
    learning_rate = 1e-4

    # Hold batch in memory
    gt_images = [None] * 6000
    input_images = {}
    input_images['300'] = [None] * len(train_ids)
    input_images['250'] = [None] * len(train_ids)
    input_images['100'] = [None] * len(train_ids)

    for epoch in range(lastepoch, total_epochs):
        if os.path.isdir("result/%04d" % epoch):
            continue
        cnt = 0
        if epoch > (total_epochs // 2): # Decrease learning rate halfway through
            learning_rate = 1e-5

        for ind in np.random.permutation(batch_ids):
            # get the path from image id
            train_id = train_ids[ind]
            in_files = glob.glob(input_dir + '%05d_00*.ARW' % train_id)
            in_path = None
            if len(in_files) <= 1:
                in_path = in_files[0]
            else :
                in_path = in_files[np.random.randint(0, len(in_files) - 1)]
            in_fn = os.path.basename(in_path)

            gt_files = glob.glob(gt_dir + '%05d_00*.ARW' % train_id)
            gt_path = gt_files[0]
            gt_fn = os.path.basename(gt_path)
            in_exposure = float(in_fn[9:-5])
            gt_exposure = float(gt_fn[9:-5])
            ratio = min(gt_exposure / in_exposure, 300)

            st = time.time()
            cnt += 1

            if input_images[str(ratio)[0:3]][ind] is None:
                raw = rawpy.imread(in_path)
                input_images[str(ratio)[0:3]][ind] = \
                  np.expand_dims(pack_raw(raw), axis=0) * ratio

                gt_raw = rawpy.imread(gt_path)
                im = gt_raw.postprocess(use_camera_wb=True, half_size=False, no_auto_bright=True, output_bps=16)
                gt_images[ind] = np.expand_dims(np.float32(im / 65535.0), axis=0)

            # crop
            H = input_images[str(ratio)[0:3]][ind].shape[1]
            W = input_images[str(ratio)[0:3]][ind].shape[2]

            xx = np.random.randint(0, W - ps)
            yy = np.random.randint(0, H - ps)
            input_patch = input_images[str(ratio)[0:3]][ind][:, yy:yy + ps, xx:xx + ps, :]
            gt_patch = gt_images[ind][:, yy * 2:yy * 2 + ps * 2, xx * 2:xx * 2 + ps * 2, :]

            if np.random.randint(2, size=1)[0] == 1:  # random flip
                input_patch = np.flip(input_patch, axis=1)
                gt_patch = np.flip(gt_patch, axis=1)
            if np.random.randint(2, size=1)[0] == 1:
                input_patch = np.flip(input_patch, axis=2)
                gt_patch = np.flip(gt_patch, axis=2)
            if np.random.randint(2, size=1)[0] == 1:  # random transpose
                input_patch = np.transpose(input_patch, (0, 2, 1, 3))
                gt_patch = np.transpose(gt_patch, (0, 2, 1, 3))

            input_patch = np.minimum(input_patch, 1.0)

            # get the shape before passed into net
            #print('Input shape:',input_patch.shape)

            with tf.device('/gpu:0'):
                _, G_current, output = sess.run([G_opt, G_loss, out_image],
                                        feed_dict={in_image: input_patch, gt_image: gt_patch, lr: learning_rate})
            output = np.minimum(np.maximum(output, 0), 1)
            g_loss[ind] = G_current

            if epoch % 200 == 0:
                sys.stdout.write("Batch=%-4d Epoch=%-4d Count=%-4d Loss=%-6.3f Time=%-6.3f" % (current_batch-1, epoch, cnt, np.mean(g_loss[np.where(g_loss)]), time.time() - st))

            if epoch % save_freq == 0:
                if not os.path.isdir(result_dir + '%04d' % epoch):
                    os.makedirs(result_dir + '%04d' % epoch)

                temp = np.concatenate((gt_patch[0, :, :, :], output[0, :, :, :]), axis=1)
                temp *= 255

                imageio.imwrite(result_dir + '%04d/%05d_00_train_%d.jpg' % (epoch, train_id, ratio), np.array(temp, dtype=np.uint8))

    saver.save(sess, checkpoint_dir + 'model.ckpt')
