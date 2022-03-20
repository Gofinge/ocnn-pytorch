import torch
import numpy as np

from solver import Dataset
from ocnn.octree import Points
from ocnn.utils import CollateBatch

from .utils import ReadPly, Transform


class ModelNetTransform(Transform):

  def preprocess(self, sample: dict, idx: int):

    # Build Points
    xyz = torch.from_numpy(sample['points']).float()
    normal = torch.from_numpy(sample['normals']).float()
    points = Points(xyz, normal)

    # # !NOTE: Normalize the points into one unit sphere in [-0.8, 0.8]
    # bbmin, bbmax = points.bbox()
    # points.normalize(bbmin, bbmax, scale=0.8)

    return points


def read_file(filename: str):

  if filename.endswith('.ply'):
    read_ply = ReadPly(has_normal=True)
    return read_ply(filename)
  elif filename.endswith('.npz'):
    raw = np.load(filename)
    output = {'points': raw['points'], 'normals': raw['normals']}
    return output
  else:
    raise ValueError


def get_modelnet40_dataset(flags):
  transform = ModelNetTransform(flags)
  collate_batch = CollateBatch()

  dataset = Dataset(flags.location, flags.filelist, transform,
                    read_file=read_file, take=flags.take)
  return dataset, collate_batch
