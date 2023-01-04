"""
To test the trained model and to visualise the result.
@fleming
Jan 4th, 2023
"""
import paddlex as pdx
import cv2
import random


def detection(image, model_structure='yolov3_darknet53', model_param='best_model', show_result=True):
	model_path = './output' + '/' + model_structure + '/' + model_param
	model = pdx.load_model(model_path)
	result = model.predict(image)
	pdx.det.visualize(image, result,threshold=0.3, save_dir='./visualize/')
	if show_result:
		img_name = image.split('/')[-1]
		img = cv2.imread('./visualize/visualize_'+img_name)
		cv2.imshow('cone detection result', img)
		cv2.waitKey(1)


def get_test_iamge(list_img):
	rand_idx = random.randint(0, len(list_img))
	img_name = list_img[rand_idx].split(' ')[0]
		# for i in range(1 + rand_idx):
		# 	img_name = f.readline().split(' ')[0]
	return './cone_det' + '/' + img_name

# model = pdx.load_model('xiaoduxiong_epoch_12')
# result = model.predict('./xiaoduxiong_epoch_12/xiaoduxiong.jpeg')
# pdx.det.visualize('./xiaoduxiong_epoch_12/xiaoduxiong.jpeg', result, save_dir='./')
# # 预测结果保存在./visualize_xiaoduxiong.jpeg


if __name__ == "__main__":
	with open('./cone_det/test_list.txt') as f:
		list_img = f.readlines()
		for i in range(30):
			test_image = get_test_iamge(list_img)
			detection(test_image)
		f.close()

