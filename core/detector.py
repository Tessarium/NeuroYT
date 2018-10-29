from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import numpy as np
import tensorflow as tf

from tensorflow.models.research.object_detection.utils import ops as utils_ops
from tensorflow.models.research.object_detection.utils import label_map_util
from tensorflow.models.research.object_detection.utils import visualization_utils as vis_util
from PIL import Image
import os


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Detector(object, metaclass=Singleton):
    def __init__(self):
        self.model_file_name = 'faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28/frozen_inference_graph.pb'
        self.label_map_file_name = 'faster_rcnn_inception_resnet_v2_atrous_coco_2018_01_28/mscoco_label_map.pbtxt'
        # self.model_file_name = 'mask_rcnn_resnet101_atrous_coco_2018_01_28/frozen_inference_graph.pb'
        # self.label_map_file_name = 'mask_rcnn_resnet101_atrous_coco_2018_01_28/mscoco_label_map.pbtxt'

        self.detection_graph = None
        self.category_index = None
        self.tensor_dict = {}
        self.load_trained_model()


    def load_trained_model(self):
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.gfile.GFile(self.model_file_name, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}

                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        self.tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                            tensor_name)

        label_map = label_map_util.load_labelmap(self.label_map_file_name)
        categories = label_map_util.convert_label_map_to_categories(label_map,
                                                                    max_num_classes=90,
                                                                    use_display_name=True)
        self.category_index = label_map_util.create_category_index(categories)

    def detect(self):
        image = Image.open('frontend/static/images/pre_in.png')
        (im_width, im_height) = image.size
        image_np = np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)

        with self.detection_graph.as_default():
            with tf.Session() as sess:
                if 'detection_masks' in self.tensor_dict:
                    detection_boxes = tf.squeeze(self.tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(self.tensor_dict['detection_masks'], [0])
                    real_num_detection = tf.cast(self.tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image_np.shape[0], image_np.shape[1])

                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    self.tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                output_dict = sess.run(self.tensor_dict,
                                       feed_dict={image_tensor: np.expand_dims(image_np, 0)})

                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.uint8)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]

        sess.close()
        tf.reset_default_graph()

        vis_util.visualize_boxes_and_labels_on_image_array(
            image_np,
            output_dict['detection_boxes'],
            output_dict['detection_classes'],
            output_dict['detection_scores'],
            self.category_index,
            instance_masks=output_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=8)

        os.rename('frontend/static/images/pre_in.png', 'frontend/static/images/in.png')
        result = Image.fromarray((image_np).astype(np.uint8))
        result.save('frontend/static/images/out.png')
        result.close()

        return output_dict['num_detections']
