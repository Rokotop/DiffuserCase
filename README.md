Final project for "Software applications for high performance wind farm simulations" based on first assignment of course "Basic usage of OpenFOAM"

# OpenFOAM version required:

The notes below are from when I did my own installation. It is basically the same as in the official installation instructions.

# Preparations (including ParaView):

sudo apt-get update

sudo apt-get install build-essential autoconf autotools-dev cmake gawk gnuplot

sudo apt-get install flex libfl-dev libreadline-dev zlib1g-dev openmpi-bin libopenmpi-dev mpi-default-bin mpi-default-dev

sudo apt-get install libgmp-dev libmpfr-dev libmpc-dev

sudo apt-get install libfftw3-dev libscotch-dev libptscotch-dev libboost-system-dev libboost-thread-dev libcgal-dev

sudo apt install paraview-dev

sudo apt install cmake qtbase5-dev qttools5-dev qttools5-dev-tools libqt5opengl5-dev libqt5x11extras5-dev libxt-dev

# Installation of OpenFOAM-v2412:

mkdir ~/OpenFOAM

cd ~/OpenFOAM

wget https://dl.openfoam.com/source/v2412/OpenFOAM-v2412.tgz

wget https://dl.openfoam.com/source/v2412/ThirdParty-v2412.tgz

tar xzf OpenFOAM-v2412.tgz 

tar xzf ThirdParty-v2412.tgz 

rm OpenFOAM-v2412.tgz ThirdParty-v2412.tgz 

source ~/OpenFOAM/OpenFOAM-v2412/etc/bashrc

foamSystemCheck

foam

./Allwmake -j -s -q -k >& log_Allwmake

# Do again, in case some dependent compilations failed

./Allwmake -j -s -q -k >& log_Allwmake

# Alternatively 

visit --> https://github.com/olesenm/openfoam


# Source your OpenFOAM version before running Allrun/Allclean/Test scripts or add a sourcing command to the scripts.
