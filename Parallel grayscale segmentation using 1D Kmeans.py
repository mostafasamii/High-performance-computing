from mpi4py import MPI
import numpy as np
from scipy import misc
from  sklearn.cluster import KMeans
comm = MPI.COMM_WORLD
size = comm.Get_size() #total number of processes
rank = comm.Get_rank() #the rank of the calling process withint the communicator

if rank == 0: #means master node
    img = misc.imread('1.jpg', True) # true 3shan tb2a grayscale
    img = misc.imresize(img, [100, 100])
    #chunk image
    split = np.array_split(img, size - 1)
    k = 4
    #generate k random numbers, initialized by random weights at the begining
    centers = np.random.randint(256, size = k)

    #----------------Loop of the KNN algorithm
    for itr in range(0, 50):
        #send chunks of the array and centroids
        for i in range(0, size - 1):
            comm.send(split[i], dest = i + 1, tag = 0)
            comm.send(centers, dest = i + 1, tag = 1)

        img_map = []
        for i in range(len(centers)):
            img_map.append([])

        # recive map
        for i in range(0, size - 1):
            n = comm.recv(dest = i + 1)
            for j in range(0, len(n)):
                for k in range(0, len(n)):
                    img_map[j].append(n[j][k])

        #claclate mean for each cluster
        for i in range(0, len(centers)):
            centers[j] = np.mean(img_map[i])
    #------------------------------------------------
    #send chunck and last center to segment
    for i in range(0, size - 1):
        comm.send(split[i], dest = i + 1, tag = 0)
        comm.send(centers, dest = i + 1, tag = 1)

    #recive segmented image to show
    s_img = []
    for i in range(0, size - 1):
        segminted_img = comm.recv(source = i + 1)
        s_img.extend(segminted_img)

    #show final image
    misc.imshow(s_img)

#--------------------------
else: #slave nodes
    #----------------------------KNN algorithm
    for itr in range(0, 50):
        #recive chunks and centroids from master
        sub_img = comm.recv(source = 0)
        centrers = comm.recv(source = 0)

        #map every every center contains list of n_clusters
        map = []
        for i in range(0, len(centrers)):
            map.append([])

        #calculate closest center
        for i range(0, sub_img.shape[0]):
            for j in range(0, sub_img.shape[1]):
                Min = 1000
                for k in range(0, len(centers)):
                    X = abs(centers[k] - sub_img[i][j])
                    if X < Min:
                        Min = X
                        centeroid_index = k
                map[centeroid_index].append(sub_img[i][j])

        #send the map to the master
        comm.send(map, dest = 0)

        #recive last value of center and chunk
        # hna 3shan alwn
        # hna 5alas al algorithm 5ls
        chunks = comm.recv(source = 0)
        centers  = comm.recv(source = 0)
        #replace each value with the center
        #dlwty galy goz2 mn al sora w al fina centroid
        # 3ayz ashof kol pixel fel sora a2rb le anhy centeroid
        for i in range(0, len(chunks.shape[0])):
            for j in range(0, len(chunks.shape[1])):
                Min = 1000
                for k in range(0, len(centers)):
                    X = np.abs(centrers[k] - chunks[i][j])
                    if X < Min:
                        Min  = X
                        closest_center = k
                #hna by7ot al mean al nha2y fel goz2 dh mn al sora 3shan yrg3o efl line aly t7t
                chunk[i][j] = closest_center
    #---------------------------------------
    #send segmented image
    comm.send(chunck, dest = 0)
