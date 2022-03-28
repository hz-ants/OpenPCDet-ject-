import glob
import numpy as np
from pathlib import Path
from ..dataset import DatasetTemplate

class LidarDataset(DatasetTemplate):
    def __init__(self, dataset_cfg, class_names, training=True, root_path=None, logger=None):
        '''
        Args:
        root_path:
        dataset_cfg:
        class_names:
        training:
        logger:

        '''
        super().__init__(
        dataset_cfg=dataset_cfg, class_names=class_names, training=training, root_path=root_path, logger=logger
        )
        points_file_list = glob.glob(str(self.root_path / 'train/points' / '*.txt'))
        labels_file_list = glob.glob(str(self.root_path / 'train/labels' / '*.txt'))
        points_file_list.sort()
        labels_file_list.sort()
        self.sample_file_list = points_file_list
        self.samplelabel_file_list = labels_file_list

    def __len__(self):
        return len(self.sample_file_list)

    def __getitem__(self, index):
        sample_idx = Path(self.sample_file_list[index]).stem  # 0000.txt -> 0000 样本id(文件编号) n：点的个数 m：标注的个数
        #print("sample_idx:",sample_idx)
        points = np.loadtxt(self.sample_file_list[index], dtype=np.float32).reshape(-1, 4)[:,0:3]  # 每个点云文件里的所有点 n*3
        points_label = np.loadtxt(self.samplelabel_file_list[index], dtype=np.float32).reshape(-1, 8) # 每个点云标注文件里的所有点 m*8
        #gt_names = np.array(['Coil']*points_label.shape[0])
        ##idx 2 char
        gt_name_lists = points_label[:,7:8].astype(np.int32).flatten().tolist()
        label_dicts= ['Car', 'Pedestrian', 'Cyclist','Van', 'Truck','Tram','Misc','Person_sitting','DontCare']
        #gt_names=np.array( label_dicts[n]  for n in gt_name_lists)
        gt_names =[]
        for i in gt_name_lists:
          gt_names.append(label_dicts[i])
        gt_names= np.array(gt_names)
        points_label = points_label[:,0:7]

        input_dict = {
            'points': points,
            'frame_id': sample_idx,
            'gt_names': gt_names,
            'gt_boxes': points_label
        }

        data_dict = self.prepare_data(data_dict=input_dict)
        return data_dict