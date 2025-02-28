
import os
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from PIL import Image
from paddleocr import PaddleOCR
import hdbscan
from sklearn.metrics import silhouette_score
# import matplotlib.cm as cm
import os
import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# from PIL import Image
from paddleocr import PaddleOCR
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
# import matplotlib.cm as cm


# ---------------------------
# 2. Subdivide Each Detected Rectangle into Squares
# ---------------------------
def subdivide_box_to_rectangles(box):
    """
    Given a detected rectangle (4 corner points), compute its axis-aligned
    bounding box and subdivide it along the longer side using the length of the smaller side.
    For a horizontal rectangle, this splits it vertically into segments of height equal to the rectangle's height;
    for a vertical rectangle, it splits it horizontally into segments of width equal to the rectangle's width.
    Returns a list of sub-boxes (each as 4 corner points).
    """
    # Compute axis-aligned bounding box coordinates.
    x_coords = [pt[0] for pt in box]
    y_coords = [pt[1] for pt in box]
    x_min, x_max = min(x_coords), max(x_coords)
    y_min, y_max = min(y_coords), max(y_coords)
    W = x_max - x_min
    H = y_max - y_min
    
    sub_boxes = []
    if W >= H:
        # Horizontal rectangle: subdivide along the width using H as segment length.
        segment_length = H
        num_segments = int(np.ceil(W / segment_length))
        # print( num_segments)
        for i in range(num_segments):
            x1 = x_min + i * segment_length
            x2 = min(x_min + (i+1) * segment_length, x_max)
            # Create sub-box as an axis-aligned rectangle.
            sub_box = [[x1, y_min], [x2, y_min], [x2, y_max], [x1, y_max]]
            sub_boxes.append(sub_box)
    else:
        # Vertical rectangle: subdivide along the height using W as segment length.
        segment_length = W
        num_segments = int(np.ceil(H / segment_length))
        for i in range(num_segments):
            y1 = y_min + i * segment_length
            y2 = min(y_min + (i+1) * segment_length, y_max)
            sub_box = [[x_min, y1], [x_max, y1], [x_max, y2], [x_min, y2]]
            sub_boxes.append(sub_box)
    return sub_boxes
def do_ocr(file_path):
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    
    # Set the image path and run OCR (result[0] contains detected text lines)
    img_path = file_path#r'C:\Users\Amansour\Downloads\cv2.PNG'
    result = ocr.ocr(img_path, cls=True)[0]
    
    # Open the image using PIL and convert to RGB
    # image = Image.open(img_path).convert('RGB')
    
    # Prepare lists for detected boxes, texts, and scores
    boxes = []
    texts = []
    scores = []
    
    for line in result:
        box = line[0]  # a list of four (x, y) coordinates
        boxes.append(box)
        text, score = line[1]  # detected text and confidence score
        texts.append(text)
        scores.append(score)
    return  boxes, texts ,scores 
def do_cluster(square_centers):
    if len(square_centers) >= 2:
        best_score = -1
        best_param = None
        # Try a range of min_cluster_size values (from 2 up to a small max or number of boxes)
        for min_cluster_size in range(2, min(5, len(square_centers)) + 1):
            clusterer_candidate = hdbscan.HDBSCAN(min_cluster_size=min_cluster_size)
            labels_candidate = clusterer_candidate.fit_predict(square_centers)
            # Consider only non-noise points for silhouette evaluation
            valid_idx = labels_candidate != -1
            unique_labels = set(labels_candidate[valid_idx])
            if len(unique_labels) < 2:
                continue  # Cannot compute silhouette with fewer than 2 clusters
            score = silhouette_score(square_centers[valid_idx], labels_candidate[valid_idx])
            if score > best_score:
                best_score = score
                best_param = min_cluster_size
    
        # If no valid clustering found, fallback to a default value
        if best_param is None:
            best_param = 2
    
        # Cluster the centers using the best min_cluster_size parameter
        clusterer = hdbscan.HDBSCAN(min_cluster_size=best_param)
        labels = clusterer.fit_predict(square_centers)
    else:
        labels = np.zeros(len(square_centers), dtype=int)
    return labels
def cluster_detected_boxes( boxes = None,texts = None,scores = None):
    # For each OCR box, subdivide into squares.
    all_squares = []       # list to hold all square boxes (each as list of 4 points)
    square_centers = []    # list to hold the center (x, y) of each square
    square_to_box = []     # mapping: index of square -> original box index
    
    for i, box in enumerate(boxes):
        squares = subdivide_box_to_rectangles(box)  # 2x2 grid; change grid_size if needed
        for sq in squares:
            sq_arr = np.array(sq)
            center = np.mean(sq_arr, axis=0)
            square_centers.append(center)
            square_to_box.append(i)
            all_squares.append(sq)
    square_centers = np.array(square_centers)  # shape: (total_squares, 2)

    labels = do_cluster(square_centers)
    
    box_cluster_labels = []  # will hold the cluster label for each original OCR box
    
    for i in range(len(boxes)):
        # Find indices of squares that belong to this original box.
        indices = [idx for idx, b_idx in enumerate(square_to_box) if b_idx == i]
        # Retrieve cluster labels for these squares.
        labels_for_box =  labels[indices]
        # Determine majority label (if tie, the first one is used)
        if len(labels_for_box) > 0:
            unique, counts = np.unique(labels_for_box, return_counts=True)
            majority_label = unique[np.argmax(counts)]
        else:
            majority_label = -1  # fallback label
        box_cluster_labels.append(majority_label)
    
    # ---------------------------
    
    clusters_texts = {}
    for i, box in enumerate(boxes):
        cluster_label = box_cluster_labels[i]
        if cluster_label in clusters_texts:
            clusters_texts[cluster_label].append((boxes[i][0],texts[i]))
        else:
             clusters_texts[cluster_label] = [(boxes[i][0],texts[i])]
    
    return  clusters_texts
def process_cv(file_path):
    boxes, texts ,scores =  do_ocr(file_path)
    clusters_texts = cluster_detected_boxes(boxes, texts ,scores)
    fullcv = {}
    for k,val in clusters_texts.items():
        points = clusters_texts[k]
        points = sorted(points, key=lambda p: (p[0][1], p[0][0]))
        fullcv[k] = ""
        for p in points:
            fullcv[k] +=  " "+p[1]
    return fullcv