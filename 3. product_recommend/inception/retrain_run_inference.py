"""Inception v3 architecture 모델을 retraining한 모델을 이용해서 이미지에 대한 추론(inference)을 진행하는 예제"""

import numpy as np
import tensorflow as tf
from inception.download import Down
from inception.dbConnect import Con


rootPath = '/Users/shinkangsik/django/imageT/down/'
modelFullPath = '/tmp/output_graph.pb'  # 읽어들일 graph 파일 경로
labelsFullPath = '/tmp/output_labels.txt'  # 읽어들일 labels 파일 경로


class Train:

    def create_graph(self):
        """저장된(saved) GraphDef 파일로부터 graph를 생성하고 saver를 반환한다."""
        # 저장된(saved) graph_def.pb로부터 graph를 생성한다.
        with tf.io.gfile.GFile(modelFullPath, 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

    def run_inference_on_image(self, imagePath, fileName, time):
        answer = None

        if not tf.io.gfile.exists(imagePath):
            tf.compat.v1.logging.fatal('File does not exist %s', imagePath)
            return answer

        image_data = tf.io.gfile.GFile(imagePath, 'rb').read()

        # 저장된(saved) GraphDef 파일로부터 graph를 생성한다.
        self.create_graph()

        with tf.compat.v1.Session() as sess:

            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
            predictions = np.squeeze(predictions)
            top_k = predictions.argsort()[-5:][::-1]  # 가장 높은 확률을 가진 5개(top 5)의 예측값(predictions)을 얻는다.
            f = open(labelsFullPath, 'rb')
            lines = f.readlines()
            labels = [str(w).replace("\n", "") for w in lines]
            for node_id in top_k:
                human_string = labels[node_id].replace("b'", "").replace("\\n'", "")
                score = str(predictions[node_id]*100)[0:5]
                result = ()
                result = (fileName, human_string, score, time)

                con = Con()
                con.insert(result)
                print('%s (score = %s)' % (human_string, score))

            param = (fileName, time)
            con = Con()
            con.insertResult(param)
            answer = labels[top_k[0]]
            return answer

    def main(self, fileName, time):
        down = Down()
        onPath = "http://chickang9.cafe24.com/uploads/"
        down.downloader(onPath + fileName, fileName)
        imagePath = rootPath + fileName  # 추론을 진행할 이미지 경로
        self.run_inference_on_image(imagePath, fileName, time)

'''
if __name__ == '__main__':
'''
