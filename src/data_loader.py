"""
数据加载模块 - 负责加载和处理传感器数据
"""

import pandas as pd
import os


class DataLoader:
    """数据加载器"""

    def __init__(self, data_path='data/sensor_data.csv'):
        self.data_path = data_path
        self.data = None

    def load_data(self):
        """加载csv数据"""
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"数据文件不存在: {self.data_path}")

        self.data = pd.read_csv(self.data_path, encoding='utf-8')
        self.data['date'] = pd.to_datetime(self.data['date'])
        print(f"数据已成功加载: {self.data.shape[0]} 行, {self.data.shape[1]} 列")
        return self.data

    def get_data(self):
        """获取数据"""
        if self.data is None:
            self.load_data()
        return self.data

    def get_summary(self):
        """获取数据摘要"""
        if self.data is None:
            self.load_data()

        return {
            'shape': self.data.shape,
            'columns': list(self.data.columns),
            'date_range': (self.data['date'].min(), self.data['date'].max()),
            'locations': self.data['location'].unique().tolist()
        }

    def filter_by_date(self, start_date=None, end_date=None):
        """按日期过滤数据"""
        if self.data is None:
            self.load_data()

        filtered_data = self.data.copy()
        if start_date:
            filtered_data = filtered_data[filtered_data['date'] >= pd.to_datetime(start_date)]
        if end_date:
            filtered_data = filtered_data[filtered_data['date'] <= pd.to_datetime(end_date)]

        return filtered_data

    def filter_by_location(self, locations):
        """按站点过滤数据"""
        if self.data is None:
            self.load_data()

        if isinstance(locations, str):
            locations = [locations]

        return self.data[self.data['location'].isin(locations)]


# 测试代码
if __name__ == '__main__':
    loader = DataLoader()
    data = loader.load_data()
    print("\n数据前5行:")
    print(data.head())
    print("\n数据摘要:")
    summary = loader.get_summary()
    for key, value in summary.items():
        print(f"{key}: {value}")