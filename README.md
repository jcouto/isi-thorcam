# isi-thorlabs
A repo to record intrinsic signal imaging with thorcams.. because we can't always get the camera we want.

This uses the [thorcam](https://github.com/matham/thorcam) package, thank you @matham.

## Installation

- Install anaconda and ``pip install thorcam``

- Clone the repo ``git clone http://github.com/jcouto/isi-thorcam``

- Install in developer mode ``python setup.py develop`` from the isi-thorcam folder


## Usage

Basic usage is to run using the command ``isi-thorcam``, then set the sample and click the ``Run acquisition button``. That will open a file selection menu. Select the path and name of a new file and the recording will start.

**Note** the recording starts in ``HW Trigger`` mode, so you need to send pulses to the camera.


*File save format* - saves to HDF5 files. Can be read in matlab and python. The data are in the ``frames`` dataset; frame id and timestamps in the ``frame_id`` dataset.

Joao Couto - Feb 2023
