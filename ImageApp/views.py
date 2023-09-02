from django.shortcuts import render
from django.core.files.storage import default_storage

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Profile
from .serializers import ProfileSerializer

from keras.preprocessing import image
from keras.models import load_model
import tensorflow as tf

import numpy as np
import json
import math


class ProfilesView(APIView):
    def post(self, request):
        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Done'})
        return Response(serializer.errors)
    def get(self, request):
        profile = Profile.objects.last()
        serializer = ProfileSerializer(profile)
        picture_data = serializer.data.get('picture', None)
        # return Response({'picture': picture_data})
        return Response(picture_data)


with open('./models/imagenet_classes.json', 'r') as f:
    labelInfo = f.read()

labelInfo = json.loads(labelInfo)


model_graph = tf.Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model = load_model('./models/MobileNetModelImagenet.h5') 

def index(request):
    return render(request, 'index.html')

def prediction(request):
    
    file = request.FILES['imageFile']
    file_name = default_storage.save('./my_pictures/'+file.name, file)

    # profile = Profile.objects.last()
    # serializer = ProfileSerializer(profile)
    # picture_data = serializer.data.get('picture', None)

    file_url = default_storage.url(file_name)

    testimage = '.'+file_url

    img_height, img_width = 224, 224
    img = image.load_img(testimage, target_size=(img_height, img_width))
    x = image.img_to_array(img)
    x = x / 255.0
    x = x.reshape(1, img_height, img_width, 3)

    with model_graph.as_default():
        with tf_session.as_default():
            global predi
            predi = model.predict(x)
            
    
    predictedLabel = labelInfo[str(np.argmax(predi[0]))]
    
    top_five = {}

    for i in range(5):
        predictedLabel2 = labelInfo[str(np.argmax(predi[0][i:]))]
        chances = (sum(predi[0][i:])/sum(predi[0]))*100
        top_five[predictedLabel2[1]] = chances
    
    return render(request, 'prediction.html', {"file_path": file_url, "predictedLabel": predictedLabel[1], 
                                               'top_five': top_five})
