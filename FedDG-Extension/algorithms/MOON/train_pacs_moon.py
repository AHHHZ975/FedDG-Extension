import os
import argparse
import sys

sys.path.append('/home/am_zam/feddg/FedDG-Extension')

from network.get_network import GetNetwork
from torch.utils.tensorboard.writer import SummaryWriter
from data.pacs_dataset import PACS_FedDG
from utils.classification_metric import Classification
from utils.log_utils import *
from utils.fed_merge import Cal_Weight_Dict, FedAvg, FedUpdate
from utils.trainval_func import site_evaluation, site_train_moon, GetFedModel, SaveCheckPoint
import torch.nn.functional as F
from tqdm import tqdm
import copy

def get_argparse():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset", type=str, default='pacs', choices=['pacs'], help='Name of dataset')
    parser.add_argument("--model", type=str, default='resnet18',
                        choices=['resnet18', 'resnet50'], help='model name')
    parser.add_argument("--test_domain", type=str, default='p',
                        choices=['p', 'a', 'c', 's'], help='the domain name for testing')
    parser.add_argument('--num_classes', help='number of classes default 7', type=int, default=7)
    parser.add_argument('--batch_size', help='batch_size', type=int, default=16)
    parser.add_argument('--local_epochs', help='epochs number', type=int, default=5)
    parser.add_argument('--comm', help='epochs number', type=int, default=100)
    parser.add_argument('--lr', help='learning rate', type=float, default=0.001)
    parser.add_argument("--lr_policy", type=str, default='step', choices=['step'],
                        help="learning rate scheduler policy")
    parser.add_argument('--note', help='note of experimental settings', type=str, default='fedavg')
    parser.add_argument('--display', help='display in controller', action='store_true')
    return parser.parse_args()

def main():
    '''log part'''
    file_name = 'moon_'+ os.path.split(__file__)[1].replace('.py', '')
    args = get_argparse()
    log_dir, tensorboard_dir = Gen_Log_Dir(args, file_name=file_name)
    log_ten = SummaryWriter(log_dir=tensorboard_dir)
    log_file = Get_Logger(file_name=log_dir + 'train.log', display=args.display)
    Save_Hyperparameter(log_dir, args)

    '''dataset and dataloader'''
    dataobj = PACS_FedDG(test_domain=args.test_domain, batch_size=args.batch_size)
    dataloader_dict, dataset_dict = dataobj.GetData()

    '''model'''
    metric = Classification()
    global_model, model_dict, optimizer_dict, scheduler_dict = GetFedModel(args, args.num_classes)    
    previous_model_dict = copy.deepcopy(model_dict)
    weight_dict = Cal_Weight_Dict(dataset_dict, site_list=dataobj.train_domain_list)
    FedUpdate(model_dict, global_model)
    best_val = 0.


    # Repeat the federated algorithm with the number of communication rounds
    for i in range(args.comm+1):
        FedUpdate(model_dict, global_model)
        for domain_name in dataobj.train_domain_list:
            
            # Put the previous local model on the evaluation mode
            previous_model_dict[domain_name].eval()
            for param in previous_model_dict[domain_name].parameters():
                param.requires_grad = False

            # Put the global model on the evaluation mode
            global_model.eval()
            for param in global_model.parameters():
                param.requires_grad = False

            site_train_moon(i, domain_name, args, model_dict[domain_name], previous_model_dict[domain_name], global_model, optimizer_dict[domain_name],
                       scheduler_dict[domain_name],dataloader_dict[domain_name]['train'], log_ten, metric)

            site_evaluation(i, domain_name, args, model_dict[domain_name], dataloader_dict[domain_name]['val'], log_file, log_ten, metric, note='before_fed')
        FedAvg(model_dict, weight_dict, global_model)


        # Initialize the previous local models with the updated local models        
        previous_model_dict = copy.deepcopy(model_dict)
        # Put the previous local model on the evaluation mode
        previous_model_dict[domain_name].eval()
        for param in previous_model_dict[domain_name].parameters():
            param.requires_grad = False
        

        fed_val = 0.
        for domain_name in dataobj.train_domain_list:
            results_dict = site_evaluation(i, domain_name, args, global_model, dataloader_dict[domain_name]['val'], log_file, log_ten, metric)
            fed_val+= results_dict['acc']*weight_dict[domain_name]
        # val 结果
        if fed_val >= best_val:
            best_val = fed_val
            SaveCheckPoint(args, global_model, args.comm, os.path.join(log_dir, 'checkpoints'), note='best_val_model')
            for domain_name in dataobj.train_domain_list:
                SaveCheckPoint(args, model_dict[domain_name], args.comm, os.path.join(log_dir, 'checkpoints'), note=f'best_val_{domain_name}_model')

            log_file.info(f'Model saved! Best Val Acc: {best_val*100:.2f}%')
        site_evaluation(i, args.test_domain, args, global_model, dataloader_dict[args.test_domain]['test'], log_file, log_ten, metric, note='test_domain')

    SaveCheckPoint(args, global_model, args.comm, os.path.join(log_dir, 'checkpoints'), note='last_model')
    for domain_name in dataobj.train_domain_list:
        SaveCheckPoint(args, model_dict[domain_name], args.comm, os.path.join(log_dir, 'checkpoints'), note=f'last_{domain_name}_model')

if __name__ == '__main__':
    main()

