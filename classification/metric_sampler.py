from __future__ import absolute_import
from collections import defaultdict

import numpy as np
import torch
from torch.utils.data.sampler import (Sampler)


class RandomIdentitySampler(Sampler):
    def __init__(self, data_source, num_instances=1):
        self.data_source = data_source
        self.num_instances = num_instances
        self.index_dic = data_source.index_dic
        self.pids = list(self.index_dic.keys())
        self.num_samples = len(self.pids)
        if(num_instances>1.):
            self.num_instances = int(num_instances)

    def __len__(self):
        if(self.num_instances<1.0):
            return self.num_samples
        else:
            return self.num_samples * self.num_instances

    def __iter__(self):
        indices = torch.randperm(self.num_samples)
        ret = []
        for i in indices:
            pid = self.pids[i]
            t = self.index_dic[pid]
            if(self.num_instances<1.0):
                if(torch.rand(1)[0]<self.num_instances):
                    t = np.random.choice(t, size=2, replace=False)
                else: 
                    t = np.random.choice(t, size=1, replace=False)
            else:
                if len(t) >= self.num_instances:
                    t = np.random.choice(t, size=self.num_instances, replace=False)
                else:
                    t = np.random.choice(t, size=self.num_instances, replace=True)
            ret.extend(t)
        
        if(self.num_instances<1.0):
            ret = ret[:self.num_samples]
        return iter(ret)

