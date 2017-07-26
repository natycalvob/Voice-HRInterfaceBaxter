cmake_minimum_required(VERSION 2.8.3)
project(baxter_actions)

find_package(catkin REQUIRED COMPONENTS
  baxter_core_msgs
  actionlib
  actionlib_msgs
  message_generation
  roscpp
  rospy
  std_msgs
)


generate_messages(
  DEPENDENCIES actionlib_msgs std_msgs  # Or other packages containing msgs
)


catkin_package(
  CATKIN_DEPENDS actionlib_msgs
)


include_directories(
  ${catkin_INCLUDE_DIRS}
)


install(
  DIRECTORY scripts/
  DESTINATION ${CATKIN_PACKAGE_BIN_DESTINATION}
  USE_SOURCE_PERMISSIONS
)


