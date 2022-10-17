# rob501_hackathon

[link to hackton files](https://q.utoronto.ca/courses/282024/pages/hackathon-materials-for-october-17)

[link to autolab](https://courses.medula.ca/courses/ROB501-F22/assessments/hackathon)


ROB501 Hackathon - Panoramas
Team: Yannis He, Kelvin Cui, Leo Li, Maxwell Zheng.

1. Code Structure
Code Structure is as follow:
.
├── mosaic_images.py
├── panorama.py
└── undo_vignetting.py
where panorama.py calls mosaic_images.py and undo_vignetting.py

2. Workflow
Panorama
  -> rectangular_image = mosaic_images(list of images)
  -> output = undo_vignetting(rectangular_image)
3. Algorithm
a) mosaic_images:
  1. find the anchor_image (image1)
  2. for rest of the image in the list:
       - feature_mapping between anchor and next_image using FLANN
       - new_anchor_image = world_perspective(anchor,next_image, RANSAC flag)
       - anchor = new_anchor
b) world_perspective: 
  1. an opencv function that takes in 2 images, feature_matches using RANSAC
  
c) undo_vignetting: 
  1. get Gaussian map from the center of the image 
  2. invert gaussian map
  4. multiply image by map
  4. normalize the output
  5. output image
  input: 
    img: str
        image path
    sigma: float
        standard deviation for gaussian kernel as a funtion of dimension
        both dimensions use the same sigma
        default is 0.5 which is half the the dimension
    brightness: float
        increased brightness after vignette correction
        (brightness * 100)% image brightness
        default is 1.3
  output: 
    a numpy array with undo_vignetting
  

   
    


The file 
A short but organized document that outlines your solution approach and enables the teaching team to
successfully run your code offline for evaluation.
