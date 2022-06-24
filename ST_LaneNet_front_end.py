# -*- coding: utf-8 -*-
# @Time    : 19-4-24 下午3:53
# @File    : ST_LaneNet_front_end.py
# @IDE: PyCharm
"""
ST_LaneNet frontend branch which is mainly used for feature extraction
"""
from semantic_segmentation_zoo import cnn_basenet
from semantic_segmentation_zoo import vgg16_based_fcn


class ST_LaneNetFrondEnd(cnn_basenet.CNNBaseModel):
    """
    ST_LaneNet frontend which is used to extract image features for following process
    """
    def __init__(self, phase, net_flag):
        """

        """
        super(ST_LaneNetFrondEnd, self).__init__()

        self._frontend_net_map = {
            'vgg': vgg16_based_fcn.VGG16FCN(phase=phase)
        }

        self._net = self._frontend_net_map[net_flag]

    def build_model(self, input_tensor, name, reuse):
        """

        :param input_tensor:
        :param name:
        :param reuse:
        :return:
        """

        return self._net.build_model(
            input_tensor=input_tensor,
            name=name,
            reuse=reuse
        )
