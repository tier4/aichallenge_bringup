#!/bin/bash
cd `dirname $0`
tar zcvf src.tar.gz \
  --exclude src/aichallenge_bringup/image \
  --exclude src/aichallenge_bringup/data/simulator.pcd \
  --exclude src/aichallenge_bringup/.git \
  src
