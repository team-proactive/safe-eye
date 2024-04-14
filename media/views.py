import cv2
import torch
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

import slowfast.utils.misc as misc
from slowfast.models import build_model
from slowfast.datasets.utils import pack_pathway_output
from slowfast.datasets.transform import get_transform  
import slowfast.utils.metrics as metrics
import numpy as np

from .models import MediaFile
from .serializers import MediaFileSerializer


def preprocess_frame(frame, cfg):
    # PySlowFast 전처리 변환 설정 가져오기
    transform = get_transform(cfg)
    
    # 프레임을 PyTorch 텐서로 변환
    frame = np.transpose(frame, (2, 0, 1))  # (H, W, C) -> (C, H, W)
    frame = torch.from_numpy(frame)
    
    # 전처리 변환 적용
    inputs = transform({"video": frame})
    
    return inputs

def postprocess_predictions(predictions):
    # 예측 결과 후처리
    video_pred = predictions["video_prediction"]
    k = max(video_pred, 1)
    
    # Top-k 클래스 인덱스 및 확률 가져오기
    topk_indexes = video_pred.topk(k, dim=1)[1]
    topk_values = video_pred.topk(k, dim=1)[0]
    
    # 클래스 이름 및 확률 매핑
    class_names = metrics.get_class_names(predictions["class_names"], topk_indexes)
    result = {
        "class_names": class_names,
        "probabilities": topk_values.tolist()
    }
    
    return result

class MediaFileViewSet(viewsets.ModelViewSet):
   queryset = MediaFile.objects.all()
   serializer_class = MediaFileSerializer

   @action(detail=True, methods=['post'])
   def predict(self, request, pk=None):
       media_file = self.get_object()

       # PySlowFast 모델 구성 파일 로드
       cfg = misc.get_cfg_defaults()
       cfg.merge_from_file('configs/Kinetics/C2D_8x8_R50.yaml')

       # PySlowFast 모델 로드
       model = build_model(cfg)
       model.load_state_dict(torch.load('path/to/model_weights.pth'))
       model.eval()

       # 비디오 스트림 처리
       video_stream = cv2.VideoCapture(media_file.file.path)
       predictions = []
       while True:
           ret, frame = video_stream.read()
           if not ret:
               break

           # 프레임 전처리 및 PySlowFast 모델 입력
           inputs = preprocess_frame(frame, cfg)
           outputs = model(inputs)
           predictions.append(outputs)

       video_stream.release()

       # 예측 결과 후처리
       predictions = pack_pathway_output(cfg, predictions)
       result = postprocess_predictions(predictions)

       # 결과를 MediaFile에 저장
       media_file.result = result
       media_file.save()

       # API 응답 포맷 정의
       response_data = {
              "id": media_file.id,
              'file': media_file.url,
              "result": result
       }

       return Response(response_data, status=status.HTTP_200_OK)

# 프레임 전처리 및 후처리 함수는 별도로 작성해야 합니다.
'''
이 코드에서는 먼저 PySlowFast 모델 구성 파일(yaml)을 로드하고, 제공된 모델 가중치 파일(pth)을 사용하여 PySlowFast 모델을 생성합니다.

그 다음, 업로드된 비디오 파일의 경로를 가져와 비디오 스트림을 열고, 각 프레임을 PySlowFast 모델에 입력으로 전달하여 예측을 수행합니다. 이때 프레임 전처리 과정이 필요할 것입니다.

모든 프레임에 대한 예측이 완료되면, PySlowFast의 pack_pathway_output 함수를 사용하여 결과를 후처리하고, 최종 결과를 MediaFile 인스턴스의 result 필드에 저장합니다.

preprocess_frame과 postprocess_predictions 함수는 PySlowFast의 transform 모듈을 활용하여 구현해야 합니다.

이 코드를 실행하면 사용자가 업로드한 비디오 파일에 대해 PySlowFast 모델의 예측이 수행되고, 그 결과가 MediaFile 모델에 저장될 것입니다.
'''
