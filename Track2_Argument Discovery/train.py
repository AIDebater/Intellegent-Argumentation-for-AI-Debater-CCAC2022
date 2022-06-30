from simpletransformers.classification import ClassificationModel
import pandas as pd
from sklearn.metrics import classification_report
import logging
import csv

logging.basicConfig(level=logging.INFO)
transformers_logger = logging.getLogger("transformers")
transformers_logger.setLevel(logging.WARNING)

# Load training data
train_df = pd.read_csv('train.txt', sep='\t', header=None, quoting=csv.QUOTE_NONE)
train_df.columns = ['text_a', 'text_b', 'labels']

dev_df = pd.read_csv('dev.txt', sep='\t', header=None, quoting=csv.QUOTE_NONE)
dev_df.columns = ['text_a', 'text_b', 'labels']


# Set training arguments
train_args = {
    'evaluate_during_training': True,
    'evaluate_during_training_verbose': True,
    'max_seq_length': 128,
    'num_train_epochs': 10,
    'train_batch_size': 16,
    'labels_list': ['0', '1'],
    'use_multiprocessing': False,
    'use_multiprocessing_for_evaluation': False,
    'overwrite_output_dir': True,
    'evaluate_during_training_steps': 100000
}

# Create model
model = ClassificationModel('roberta', 'roberta-base', num_labels=2, args=train_args, use_cuda=False)

# Define metric
def clf_report(labels, preds):
    return classification_report(labels, preds, output_dict=True)


# Train model 
# Checkpoint after each epoch will be saved to outputs/
# The best model on dev set will be saved to outputs/best_model/
model.train_model(train_df, eval_df=dev_df, clf_report=clf_report)





