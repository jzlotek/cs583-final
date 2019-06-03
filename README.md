# Learning to See in the Dark

> Joe Hines and John Zlotek
> But based entirely on the work found [here](http://cchen156.web.engr.illinois.edu/SID.html)

# Developers

## Python Notebooks

Since we did all of our training and testing on Google's Colaboratory,
we decided to provided our notebooks in the `notebooks/` directory.
This will run through the training and validation of a model, and
provide access to the outputs of the tests.

This allows you to quickly get access to and play around with the
network. However, if you're looking to get more hands on, keep reading.

## CLI

We provide all of the necessary files to train, modify, and use this
network in the `src/` directory of this project. While we do provide
our own trained model, we encourage explorations. The following are
instructions/requirements for various items.

***NOTE: WE ONLY SUPPORT THE SONY DATASET AND MODEL IN THIS VERSION***

- Datasets
	- The original paper used a Sony and Fuji dataset, as these cameras
		have different RAW formats. **IF YOU WISH TO USE .DNG FILES, WHICH
		MOST SMARTPHONES CAN TAKE, USE THE SONY MODEL. IT IS COMPATIBLE WITH
		.ARW AND .DNG FILES**
	- Downloading and unzipping the dataset will take a while
		as well as roughly ~150gb of disk space, as the dataset is
		25GB (Sony)
	- To download (inside the `src/` directory):
		- `python3 download_datasets.py`
- Our trained model
	- We trained a model with 501 epochs, although we recommend 4001 per
		the paper (but deadlines can be a tricky thing).
	- This model requires a ~100MB of disk space, and is unzipped into
		`src/trained_model/`
- Train the model
	- If you choose to train the model yourself, it is good to be aware of
		the `batch_size` variable. A high batch number _could_ provide better
		results, but will use impractical amounts of memory. Batch sizes less
		than 30 images can use less than 6GB of RAM, but some experimentation
		may be required on your system.
	- From within `src/`
		- `python3 train_Sony.py`
- Test the model
	- This requires a model to exist in `src/trained_model/`
	- From inside `src/`
		- `python3 test_Sony.py`
- CLI application is run via `python correct_img.py`
  - Usage:
    - `python correct_img.py {source} {optional: destination}`
    - Not supplying a destination will create a `.png` file in the same directory of the source image

