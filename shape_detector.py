# 自己编写的简单的圆、三角形、矩形和多边形检验代码
import cv2
import numpy as np

IMAGE_PATH = "input_image.png"


class ShapeDetector(object):
    def __init__(self, image_path):
        self.input_image = cv2.imread(IMAGE_PATH)
        self.subimage = []  # 将原图像切分为各个几何形状单独的图像
        self.vertices_data = []  # 储存角点信息self.vertices_data[i]代表第i个物体的角点list
        self.class_of_shape = ["circle", "triangle", "rectangle", "polygon"]  # 将图像分为四类，圆、三角形、矩形和多边形

        self.image_segmentation()
        for i in range(len(self.subimage)):
            self.vertices_data.append(self.vertices_detector(self.subimage, i))
            self.shape_classification(self.vertices_data[i], i)
            cv2.imwrite("_6_label_image"+str(i)+".png",self.input_image)

    def image_segmentation(self):
        """将图像中的像素按不同物体之间进行分组并分割，同一物体具有同一分组标号"""
        img_gray = cv2.cvtColor(self.input_image,cv2.COLOR_RGB2GRAY)
        _, img_gray = cv2.threshold(img_gray,200,255,cv2.THRESH_BINARY_INV)
        # cv2.imshow("binary",img_gray)
        cv2.imwrite("_1_binary_image.png",img_gray)
        # 开始对图像的像素进行分组，同一物体的像素应该是同一标号
        group = 1  # 图像中物体分组标号
        img_group = np.zeros((img_gray.shape[0] + 2, img_gray.shape[1] + 2))
        for i in range(1, img_gray.shape[0]):
            for j in range(1, img_gray.shape[1]):
                if img_gray[i, j] != 0:
                    temp_group = img_group[i - 1:i + 2, j - 1:j + 2].copy()
                    # print(i, j, img_group[i - 1:i + 2, j - 1:j + 2])
                    if np.sum(temp_group) == 0:
                        img_group[i, j] = group
                        group += 1
                    else:
                        temp_group[temp_group == 0] = group + 2
                        img_group[i, j] = np.min(temp_group)
                        edit_flag = False
                        for ii in range(0, 3):
                            for jj in range(0, 3):
                                if (temp_group[ii, jj] != group + 2) and (temp_group[ii, jj] != img_group[i, j]):
                                    edit_num = temp_group[ii, jj]
                                    edit_flag = True
                        if edit_flag:
                            img_group[img_group == edit_num] = img_group[i, j]
        print("group=",group)
        img_group = img_group[1:-1, 1:-1].astype(np.uint8)  # 转换为uint8类型，否则无法用imshow显示图片

        thresh_area = 100
        object_group_index = []
        for i in range(1, group):
            temp_group = img_group.copy()
            # print(temp_group[temp_group == i])
            temp_group[temp_group != i] = 0
            area = np.sum(temp_group) / i
            # print("area",i,"=",np.sum(temp_group),"/",i,"=",area)
            if area > thresh_area:
                object_group_index.append(i)
        cv2.imwrite("_2_img_group.png",img_group*10)
        for i in range(len(object_group_index)):
            subimage = img_gray.copy()
            subimage[img_group!=object_group_index[i]]=0
            self.subimage.append(subimage)
            cv2.imwrite("_3_sub_image"+str(i)+".png",subimage)

    def vertices_detector(self, subimage, index):
        if 0 == len(subimage):
            print("the list of subimage is None")
            return -1
        vertices_image = cv2.cornerHarris(subimage[index],3,5,0.04)
        print(vertices_image.max())
        _, vertices_image = cv2.threshold(vertices_image, 1, 255, cv2.THRESH_BINARY)
        vertices_image = vertices_image.astype(np.uint8)
        cv2.imwrite("_4_vertices_image"+str(index)+"_before_processing.png", vertices_image)
        vertices_data =[]
        for i in range(vertices_image.shape[0]):
            for j in range(vertices_image.shape[1]):
                if vertices_image[i,j]!=0:
                    vertices_image[i-5:i+6,j-5:j+6]=0  # 把相邻的顶点都消去，保证领域内只有一个顶点
                    vertices_image[i,j] = 255  # 把当前的角点复原
                    cv2.circle(vertices_image,(i,j),10,(0,0,255),2)  # 将当前角点画出来
                    vertices_data.append((j,i))
        cv2.imwrite("_5_vertices_image"+str(index)+"_after_processing.png", vertices_image)
        return vertices_data  # 返回当前subimage的角点信息

    def shape_classification(self, vertices_data, index):
        if 0==len(vertices_data):
            stop_flag = False
            for i in range(self.subimage[index].shape[0]):
                for j in range(self.subimage[index].shape[1]):
                    if self.subimage[index][i,j]!=0:
                        cv2.putText(self.input_image, self.class_of_shape[0], (j,i), cv2.FONT_HERSHEY_PLAIN,
                                    1.2, (0, 0, 0))
                        stop_flag = True
                        break
                if stop_flag:
                    break
        elif 3==len(vertices_data):
            cv2.putText(self.input_image, self.class_of_shape[1], vertices_data[0], cv2.FONT_HERSHEY_PLAIN, 1.2, (0,0,0))
        elif 4==len(vertices_data):
            cv2.putText(self.input_image, self.class_of_shape[2], vertices_data[0], cv2.FONT_HERSHEY_PLAIN, 1.2, (0,0,0))
        else:
            cv2.putText(self.input_image, self.class_of_shape[3], vertices_data[0], cv2.FONT_HERSHEY_PLAIN, 1.2, (0,0,0))


def main():
    shape_detector = ShapeDetector(IMAGE_PATH)
    cv2.waitKey(0)


if __name__ == '__main__':
    main()
