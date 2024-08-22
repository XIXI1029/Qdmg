import json
import os
import argparse
from tqdm import tqdm


def convert_label_json(json_dir, save_dir, classes):
    json_paths = [f for f in os.listdir(json_dir) if f.endswith('.json')]
    classes = classes.split(',')

    # 创建标签到索引的映射
    label_to_index = {label: index for index, label in enumerate(classes)}

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    for json_path in tqdm(json_paths):
        path = os.path.join(json_dir, json_path)
        with open(path, 'r') as load_f:
            json_dict = json.load(load_f)
        h, w = json_dict['imageHeight'], json_dict['imageWidth']

        txt_path = os.path.join(save_dir, json_path.replace('json', 'txt'))
        with open(txt_path, 'w') as txt_file:

            for shape_dict in json_dict['shapes']:
                label = shape_dict['label']

                # 仅处理在指定类别中的标签
                if label not in label_to_index:
                    continue

                label_index = label_to_index[label]
                points = shape_dict['points']

                points_nor_list = []
                for point in points:
                    points_nor_list.append(point[0] / w)
                    points_nor_list.append(point[1] / h)

                points_nor_list = list(map(lambda x: str(x), points_nor_list))
                points_nor_str = ' '.join(points_nor_list)

                label_str = str(label_index) + ' ' + points_nor_str + '\n'
                txt_file.write(label_str)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Convert JSON annotations to TXT.')
    parser.add_argument('--json-dir', type=str, required=True, help='Path to the directory containing JSON files.')
    parser.add_argument('--save-dir', type=str, required=True, help='Directory to save converted TXT files.')
    parser.add_argument('--classes', type=str, required=True, help='Comma-separated list of class labels to include.')
    args = parser.parse_args()

    convert_label_json(args.json_dir, args.save_dir, args.classes)
