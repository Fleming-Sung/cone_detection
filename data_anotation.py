"""
To convert .csv annotation to Pascal VOC standard format.
Partially referenced to ChengXuYuanXiaoDu from CSDN.
@fleming
Jan.1st. 2023
"""
import csv
import os
import shutil

# specify source path
orin_dir = "/home/fleming/workspace/self_research/fsac/MIT-Driverless-CV-TrainingInfra/CVC-YOLOv3/dataset"


def write_pbj(xml_file, str_in_csv, obj='cone'):
	bbox_list = str_in_csv.strip("[").strip("]").split(',')
	x0 = int(bbox_list[0])
	y0 = int(bbox_list[1])
	x1 = int(bbox_list[0]) + int(bbox_list[3])
	y1 = int(bbox_list[1]) + int(bbox_list[2])
	xml_file.write('    <object>\n')
	xml_file.write('        <name>' + str(obj) + '</name>\n')
	xml_file.write('        <pose>Unspecified</pose>\n')
	xml_file.write('        <truncated>0</truncated>\n')
	xml_file.write('        <difficult>0</difficult>\n')
	xml_file.write('        <bndbox>\n')
	xml_file.write('            <xmin>' + str(x0) + '</xmin>\n')
	xml_file.write('            <ymin>' + str(y0) + '</ymin>\n')
	xml_file.write('            <xmax>' + str(x1) + '</xmax>\n')
	xml_file.write('            <ymax>' + str(y1) + '</ymax>\n')
	xml_file.write('        </bndbox>\n')
	xml_file.write('    </object>\n')


def get_annotation(csv_file_path):
	with open(csv_file_path) as csvfile:
		# 读取csv数据
		csv_reader = csv.reader(csvfile)
		# 去掉第2行(第0,1行是列名)
		for i in range(header_line):
			csv_header = next(csv_reader)
		# 因为csv数据中有许多行其实是同一个照片，因此需要pre_img
		# pre_img = ''  # 存储前一张图像的名称
		for row in csv_reader:
			# C:/Users/Timothy/Desktop/keras-retinanet/images/test/Subset_1_450x450_001.jpg
			# 只要文件名Subset_1_450x450_001
			img = row[0].split("/")[-1].split(".")[0]
			width = row[2]
			height = row[3]
			# 遇到的是一张新图片
			# todo: clean the pre_image related code
			# if img != pre_img:
				# 非第一张图片,在上一个xml中写下</annotation>
				# if pre_img != '':
					# todo: add a repeat .xml file checking
					xml_file1 = open((save_xml_dir + pre_img + '.xml'), 'a')
					xml_file1.write('</annotation>')
					xml_file1.close()
				# 新建xml文件
				xml_file = open((save_xml_dir + img + '.xml'), 'w')
				xml_file.write('<annotation>\n')
				xml_file.write('    <folder>JPEGImages</folder>\n')
				xml_file.write('    <filename>' + str(img) + '.jpg' + '</filename>\n')
				xml_file.write('    <source>\n')
				xml_file.write('        <database>Unknow</database>\n')
				# xml_file.write('<annotation> organoid </annotation>\n')
				xml_file.write('    </source>\n')
				xml_file.write('    <size>\n')
				xml_file.write('        <width>' + str(width) + '</width>\n')
				xml_file.write('        <height>' + str(height) + '</height>\n')
				xml_file.write('        <depth>3</depth>\n')
				xml_file.write('    </size>\n')
				xml_file.write('	<segmented>0</segmented>\n')

				for idx, column in enumerate(row):
					if idx < 5:
						continue
					elif column == '':
						break
					else:
						write_pbj(xml_file, column)
				xml_file.close()
				pre_img = img
			else:
				# 同一张图片，只需要追加写入object
				xml_file = open((save_xml_dir + pre_img + '.xml'), 'a')
				xml_file.write('    <object>\n')
				xml_file.write('<name>' + str(row[-1]) + '</name>\n')
				# '''  按需添加
				xml_file.write('        <pose>Unspecified</pose>\n')
				xml_file.write('        <truncated>0</truncated>\n')
				xml_file.write('        <difficult>0</difficult>\n')

				xml_file.write('        <bndbox>\n')
				xml_file.write('            <xmin>' + str(row[1]) + '</xmin>\n')
				xml_file.write('            <ymin>' + str(row[2]) + '</ymin>\n')
				xml_file.write('            <xmax>' + str(row[3]) + '</xmax>\n')
				xml_file.write('            <ymax>' + str(row[4]) + '</ymax>\n')
				xml_file.write('        </bndbox>\n')
				xml_file.write('    </object>\n')
				xml_file.close()
				pre_img = img

	# csv表格最后一个xml需要写入</annotation>
	xml_file1 = open((save_xml_dir + pre_img + '.xml'), 'a')
	xml_file1.write('</annotation>')
	xml_file1.close()
	print("Annotation convert finished!")


def get_img(dir_path, dest_path):
	src_files = os.listdir(dir_path)
	print('Copying .jpg images...')
	for file_name in src_files:
		source_file = dir_path + file_name
		dst_file = dest_path + file_name
		if not os.path.exists(dest_path+file_name):
			shutil.copy(source_file, dst_file)
	print('Images copy completed!')


if __name__ == "__main__":
	csv_file_path = orin_dir + '/all.csv'
	orin_jpg_dir = orin_dir + '/YOLO_Dataset/'
	save_xml_dir = "./cone_det/Annotations/"
	save_jpg_dir = "./cone_det/JPEGImages/"
	header_line = 2

	if not os.path.exists(save_xml_dir):
		os.makedirs(save_xml_dir)
	csv_file_path = orin_dir + '/all.csv'
	get_annotation(csv_file_path)

	if not os.path.exists(save_jpg_dir):
		os.makedirs(save_jpg_dir)
	get_img(orin_jpg_dir, save_jpg_dir)

	# todo: add a file check function



