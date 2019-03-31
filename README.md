# circle-triangle-rectangle-polycon-detector
simple code for detecting circle/triangle/rectangle/polycon in an image
To run the code, please put the file "input_image.png" in the same folder with "shape_detector.py".
Or just open "shape_detector.py" and edit the global variable "IMAGE_PATH = # your path".

Output specification:
1._1_binary_image.png: the binary image of the inputimage;
2._2_img_group.png: the grouped image of the inputimage. Each object in the image was labeled by respective group number;
3._3_sub_imagei.png: the image which has the only object i in the image. Its size is the same with the original image;
4._4_vertices_imagei_before_processing.png: the image of vertices before we process;
5._5_vertices_imagei_after_processing.png: the image of vertices after we process;
6._6_label_imagei.png: the result image which the object in image was gradually labeled.
