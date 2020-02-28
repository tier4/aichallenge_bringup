cmake_minimum_required(VERSION 2.8.3)
project(aichallenge_bringup)

## Compile as C++11, supported in ROS Kinetic and newer
add_compile_options(-std=c++11)

find_package(catkin REQUIRED COMPONENTS
  autoware_msgs
  map_file
  robot_state_publisher
  rosbridge_server
)

catkin_package(
)

include_directories(
  include
  ${catkin_INCLUDE_DIRS}
)

foreach(dir launch data)
  install(DIRECTORY ${dir}/
    DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}/${dir})
endforeach(dir)