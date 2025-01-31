# https://github.com/dmlc/dgl/blob/master/examples/pytorch/gat/utils.py

from http.client import UnimplementedFileMode
import numpy as np
import torch
import os


class EarlyStopping:
    def __init__(self, patience=100, store_path="es_checkpoint"):
        self.patience = patience
        self.counter = 0
        self.best_score = None
        self.record_val_acc = None

        self.best_epoch = -1
        self.epoch_id = -1

        self.early_stop = False
        self.store_path = os.path.join("cache", "ckpts", store_path)
        self.history = []

    def step(self, val_loss, model):
        self.epoch_id += 1
        score = val_loss.item()
        self.history.append(score)

        if self.best_score is None:
            self.best_score = score
            self.save_checkpoint(model)
            self.best_epoch = self.epoch_id

        elif score >= self.best_score:
            self.counter += 1
            if self.counter >= self.patience:
                self.early_stop = True  # stop
        else:
            self.best_score = score
            self.save_checkpoint(model)
            self.best_epoch = self.epoch_id
            self.counter = 0
        return self.early_stop

    def save_checkpoint(self, model):
        """Saves model when validation loss decrease."""
        torch.save(model.state_dict(), self.store_path)
