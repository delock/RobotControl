#!/usr/bin/python3
import cv2
import numpy as np
import time
import _thread as thread
from mvnc import mvncapi as mvnc
import settings

def init(network):
    global dim
    global ilsvrc_mean
    global graph
    global device

    # get labels
    labels_file = 'words.txt'
    settings.labels = np.loadtxt(labels_file,str,delimiter='\t')
    # configuration NCS
    mvnc.SetGlobalOption(mvnc.GlobalOption.LOGLEVEL, 2)
    devices = mvnc.EnumerateDevices()
    if len(devices) == 0:
        print('No devices found')
        quit()
    device = mvnc.Device(devices[0])
    device.OpenDevice()
    opt = device.GetDeviceOption(mvnc.DeviceOption.OPTIMISATIONLIST)

    if network == "squeezenet":
        print ("using squeezenet")
        network_blob='networks/SqueezeNet/graph'
        dim=(227,227)
    elif network=="googlenet":
        print ("using goolenet")
        network_blob='networks/GoogLeNet/graph'
        dim=(224,224)
    elif network=='alexnet':
        print ("using alexnet")
        network_blob='networks/AlexNet/graph'
        dim=(227,227)
    #Load blob
    with open(network_blob, mode='rb') as f:
        blob = f.read()
    graph = device.AllocateGraph(blob)
    graph.SetGraphOption(mvnc.GraphOption.ITERATIONS, 1)
    iterations = graph.GetGraphOption(mvnc.GraphOption.ITERATIONS)
    ilsvrc_mean = np.load('ilsvrc_2012_mean.npy').mean(1).mean(1)

    thread.start_new_thread(inference_frame, ("Inference thread", (0)))


def inference_frame(threadName, arg):
    global dim
    global ilsvrc_mean
    global graph
    global labels

    while True:
        #begin = time.time()
        local_frame = settings.frame
        img = local_frame[360:720, 360:720]
        img = cv2.resize(img, dim)
        img = img.astype(np.float32)
        img[:,:,0] = (img[:,:,0] - ilsvrc_mean[0])
        img[:,:,1] = (img[:,:,1] - ilsvrc_mean[1])
        img[:,:,2] = (img[:,:,2] - ilsvrc_mean[2])
        graph.LoadTensor(img.astype(np.float16), 'user object')
        output, userobj = graph.GetResult()
        settings.order = output.argsort()[::-1][:6]
        #end = time.time()
        #print ("inference in " + str(end-begin) + " s")

def close():
    global graph
    global device
    graph.DeallocateGraph()
    device.CloseDevice()
