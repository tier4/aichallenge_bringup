FROM autoware/autoware:1.13.0-melodic-cuda
ENV USERNAME autoware

# Copy user files by docker `COPY` command
RUN su -c "mkdir -p /home/autoware/aichallenge_ws" $USERNAME
COPY --chown=autoware:autoware src /home/$USERNAME/aichallenge_ws/src

# Build Autoware
RUN su -c "bash -c 'cd /home/$USERNAME/; \
  source /home/$USERNAME/Autoware/install/setup.bash; \
  cd aichallenge_ws/; \
  rosdep update; \
  rosdep install -y -r -i --from-paths src --ignore-src --rosdistro $ROS_DISTRO; \
  AUTOWARE_COMPILE_WITH_CUDA=1 colcon build --parallel-workers 16 --cmake-args -DCMAKE_BUILD_TYPE=Release'" $USERNAME

CMD ["bash"]
