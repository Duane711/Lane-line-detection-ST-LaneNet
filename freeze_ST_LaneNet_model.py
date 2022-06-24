# -*- coding: utf-8 -*-
# @Time    : 2021/4/5 下午4:53
# @File    : freeze_ST_LaneNet_model.py.py
# @IDE: PyCharm
"""
Freeze ST_LaneNet model into frozen pb file
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse

import tensorflow as tf

from ST_LaneNet_model import ST_LaneNet

MODEL_WEIGHTS_FILE_PATH = './test.ckpt'
OUTPUT_PB_FILE_PATH = './ST_LaneNet.pb'


def init_args():
    """

    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-w', '--weights_path', default=MODEL_WEIGHTS_FILE_PATH)
    parser.add_argument('-s', '--save_path', default=OUTPUT_PB_FILE_PATH)

    return parser.parse_args()


def convert_ckpt_into_pb_file(ckpt_file_path, pb_file_path):
    """

    :param ckpt_file_path:
    :param pb_file_path:
    :return:
    """
    # construct compute graph
    with tf.variable_scope('ST_LaneNet'):
        input_tensor = tf.placeholder(dtype=tf.float32, shape=[1, 256, 512, 3], name='input_tensor')

    net = lanenet.LaneNet(phase='test', net_flag='vgg')
    binary_seg_ret, instance_seg_ret = net.inference(input_tensor=input_tensor, name='ST_LaneNet_model')

    with tf.variable_scope('ST_LaneNet/'):
        binary_seg_ret = tf.cast(binary_seg_ret, dtype=tf.float32)
        binary_seg_ret = tf.squeeze(binary_seg_ret, axis=0, name='final_binary_output')
        instance_seg_ret = tf.squeeze(instance_seg_ret, axis=0, name='final_pixel_embedding_output')

    # create a session
    saver = tf.train.Saver()

    sess_config = tf.ConfigProto()
    sess_config.gpu_options.per_process_gpu_memory_fraction = 0.85
    sess_config.gpu_options.allow_growth = False
    sess_config.gpu_options.allocator_type = 'BFC'

    sess = tf.Session(config=sess_config)

    with sess.as_default():
        saver.restore(sess, ckpt_file_path)

        converted_graph_def = tf.graph_util.convert_variables_to_constants(
            sess,
            input_graph_def=sess.graph.as_graph_def(),
            output_node_names=[
                'ST_LaneNet/input_tensor',
                'ST_LaneNet/final_binary_output',
                'ST_LaneNet/final_pixel_embedding_output'
            ]
        )

        with tf.gfile.GFile(pb_file_path, "wb") as f:
            f.write(converted_graph_def.SerializeToString())


if __name__ == '__main__':
    """
    test code
    """
    args = init_args()

    convert_ckpt_into_pb_file(
        ckpt_file_path=args.weights_path,
        pb_file_path=args.save_path
    )
