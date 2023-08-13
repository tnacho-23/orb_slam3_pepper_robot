# ROS wrapper for ORB-SLAM3

Adadaptation for [Pepper Robot](https://github.com/uchile-robotics/maqui_bringup) of a ROS wrapper for [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3). The main idea is to use the ORB-SLAM3 as a standalone library and interface with it instead of putting everything together.

##  Installation

ORB-SLAM3 [installation](https://devpress.csdn.net/ubuntu/62f629af7e6682346618ab89.html) and operation Operating environment: Ubuntu 18 04 Installation dependency Download ORB-SLAM3 source code git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git ORB_SLAM3 Pangolin


### Pangolin installation

```
git clone https://github.com/stevenlovegrove/Pangolin.git
```

According to the instructions on github, install the dependencies required for Pangolin

    C++11
    OpenGL (Desktop / ES / ES2)
        (lin) sudo apt install libgl1-mesa-dev
    Glew
        (deb) sudo apt install libglew-dev
    CMake (for build environment)
        (deb) sudo apt install cmake

Recommended Dependencies

    Python2 / Python3, for drop-down interactive console
        (deb) sudo apt install libpython2.7-dev
    Wayland
        pkg-config: sudo apt install pkg-config
        Wayland and EGL:sudo apt install libegl1-mesa-dev libwayland-dev libxkbcommon-dev wayland-protocols

```
sudo apt-get install cmake libeigen3-dev libsuitesparse-dev qtdeclarative5-dev qt5-qmake libqglviewer-dev 
sudo apt-get install libboost-dev 

```

Compile and install Pangolin


```
cd Pangolin
mkdir build
cd build
cmake ..
cmake --build .
```

Opencv (requirement > 3.0) installation steps are omitted


### Orbslam Installation

```
git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git  ORB_SLAM3
```

Go to the file CmakeLists.txt in the ORB_SLAM3 folder and change the lines:

```
find_package(OpenCV 4.0)
   if(NOT OpenCV_FOUND)
      message(FATAL_ERROR "OpenCV > 4.0 not found.")
   endif()
```

to:

```
find_package(OpenCV 3.2)
   if(NOT OpenCV_FOUND)
      message(FATAL_ERROR "OpenCV > 3.2 not found.")
   endif()
```

Build ORB_SLAM:

```
cd ORB_SLAM3

cd Thirdparty/DBoW2
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j2

cd ../../g2o
mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j2

cd ../../../

cd Vocabulary
tar -xf ORBvoc.txt.tar.gz
cd ..

mkdir build
cd build
cmake .. -DCMAKE_BUILD_TYPE=Release
make -j2

```

### ORB_SLAM3 Ros Wrapper installation

```
mkdir orb_ws
cd orb_ws
mkdir src
cd ..
catkin build -j2

cd src

git clone https://github.com/tnacho-23/orb_slam3_ros.git

cd ..
catkin build -j2

```


##  How to run ORBSLAM3 ROS on Pepper Robot?
 1. Launch maqui bringup in Maqui's head

    ```
    roslaunch maqui_bringup maqui.launch
    ```

2. Connect to Pepper exporting the ros master in every new terminal in your pc
    
    ```
    export ROS_MASTER_URI=http://pepper.local:11311
    ```

3. Launch orbslam3 **don't forget to source your ws**

    ```
    roslaunch orb_slam3_ros ntuviral_mono_maqui.launch
    ```

4. Map! Launch Teleop and map the enviroment (try using some routine to keep Pepper's head withoup moving)



 ## Realsense things
 (Tengo el cerebro frito y no voy a pensar en inglés, queda pendiente su traducción)

 1. Launch Realsense d435i node
```
roslaunch orb_slam3_ros realsense_d435i.launch
```
 2. Launch TUM RGB-D for Realsense d435i
```
roslaunch orb_slam3_ros tum_rgbd_rs.launch
```
 3. Enjoy! Pangolin is active by default.


##  Save and load map 

The map file will have `.osa` extension, and is located in the `ROS_HOME` folder (`~/.ros/` by default).
#### Load map:
- Set the name of the map file to be loaded with `System.LoadAtlasFromFile` param in the settings file (`.yaml`).
- If the map file is not available, `System.LoadAtlasFromFile` param should be commented out otherwise there will be error.
#### Save map:
- **Option 1**: If `System.SaveAtlasToFile` is set in the settings file, the map file will be automatically saved when you kill the ros node.
- **Option 2**: You can also call the following ros service at the end of the session
```
rosservice call /orb_slam3/save_map [file_name]
```

- Once the 3D mapping is ready, save it and restart, loading the map, using the localization mode. Launch the pointcloud to laser scan, then try saving the map with gmapping, as it follows:

```
roslaunch orb_slam3_ros pointcloud_to_laser_scan.launch
```

```
roslaunch orb_slam3_ros orb_mapping.launch
```

 Now everytime you want to load a map, you must load the orbslam 3D map and the pgm generated with gmapping using your favourite localization/navigation algorithms.
 
