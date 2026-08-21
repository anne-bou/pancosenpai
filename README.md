# pancosenpai
A small graphical tool for network analysis with Panco

PancoSenpai can be viewed as a pedagogic tool for helping with the use of the [Panco](https://github.com/anne-bou/panco) toolbox. Basically, it enables to 

1. draw a small network
2. analysing the network (end-to-end delays)
3. generating a python file with the panco analysis of the small network.

For now, there are only a few possibilities, that should be enough for a start with Panco.

## Requirements
The installation of **Panco** is required, which requires itself the installation of **lp_solve** and**Cplex**. Only lp_solve is required here. 

## Installation

- download the repository, and install it (pip install .)
- launch  `pancoSenpai`

### For Debian/ Ubuntu
The packages can only be installed in a virtual environment (venv). In the repository where the package is downloaded:
```
python3 -m venv mon_env
source mon_venv/bin/activate
pip install . 
```
If you want to be able to run the script outside this virtual environment, the easiest way (though not cleanest) is to export the path in the .bashrc: add the line `export PATH="$PATH:path/to/pancoSenpaiRepo"`, you can find the repo with the command `which pancoSenpai/`

## Documentation
First, launch pancoSenpai in a terminal


### Default parameters
You can choose the defaults parameters for the service / arrival curves (we only use token-bucket / rate-latency curves), as well as the shaping rate (for the servers) and the maximum packet length (for flows). 

**Only integers are accepted**

If you modify, do not forget to save the parameters (they will be the default parameters until you modify them again)

### Toy FIFO Network
In this frame, you can draw and analyze a small FIFO network
- click on the white  canvas to create servers
- their default service curve is the one you chose at the previous step
- you can click again on the server to modify its parameters (column 1), or delete the server.
- you can create flows (column 1): click on *new flow*. You can again modify the parameters and you need to select the path, by clicking on the servers (in order). Then click *Apply* and the flow is created
- you can see the construction of the network in column 4
- In column 3, you can select /modify or delete a flow. When you click on *Modify flow*, the path should be shown in red (it you do not click on any server, the path will be unmodified, otherwise enter the new path).
- When you have finished drawing the network, you can select the methods for the analysis (computation of the end-to0end delays). Select the methods and click *Compute bounds*. The results will show in  a new window
- You can also generate  a python file `toy.py` that will  compute  the bounds. You can execute it where `panco` can be used (that means in a virtual environment for Debian/Ubuntu users).

### Toy network with priorities
- This is basically the same as the previous point.
- You can now choose the number of classes
- When defining a flow, you need to enter the class of the flow. Be aware that **when modifying a flow, you need to enter its class**
- The results are
  1. computing the network for each priority class
  2. computing the end-to-end delays (slight renumbering of the flows per class)
- This is also what the python file `toyprio.py` will print .

  


