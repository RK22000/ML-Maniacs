# Child Mind Sleep

## Steps to get started

1. Download the dataset from the [kaggle competetion](https://www.kaggle.com/competitions/child-mind-institute-detect-sleep-states/data)
2. Unzip the 4 files in a directory called data/
3. Run EAD.ipynb, and download any dependencies you might need.
4. 

## Steps to contribute

1. Pull the repo
2. Create a new branch from the branch you want to modify
3. Modify your branch
4. Push your branch and create a Pull request to merge your branch into main
5. 

## About this banch

In this branch I tried different way to organize and set up the dataset for easy data loading. Ultimately I've decided on loading and caching small section of the data from `train_series.parquet` as and when its needed. You can see this demonstrated in [dataloader_demo](dataloader_demo.ipynb)
