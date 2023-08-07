# ROS wrapper for ORB-SLAM3: The Pepper case

Adadaptation for [Pepper Robot](https://github.com/uchile-robotics/maqui_bringup) of a ROS wrapper for [ORB-SLAM3](https://github.com/UZ-SLAMLab/ORB_SLAM3). The main idea is to use the ORB-SLAM3 as a standalone library and interface with it instead of putting everything together. 

##  How to run ORBSLAM3 ROS on Pepper Robot?
 1. Launch maqui bringup in Maqui's head

    ```
    roslaunch maqui_bringup maqui.launch
    ```

2. Connect to Pepper exporting the ros master in every new terminal in your pc
    
    ```
    export ROS_MASTER_URI=http://pepper.local:11311
    ```

3. Launch orbslam3 **don't forget to source your catkin_ws**

    ```
    roslaunch orb_slam3_ros ntuviral_mono_maqui.launch
    ```

4. Map! Launch Teleop and map the enviroment (try using some routine to keep Pepper's head withoup moving)


### Save and load map 

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

5. Once the mapping is ready, launch the pointcloud to laser scan, then try saving the map with gmapping (it subscribes to the full map, maybe we need to change it to only the points it sees at the moment).

```
roslaunch orb_slam3_ros pointcloud_to_laser_scan.launch
```

```
roslaunch orb_slam3_ros orb_mapping.launch
```

 Now everytime you want to load a map, you must load the pgm generated with gmapping and the orbslam 3D map.