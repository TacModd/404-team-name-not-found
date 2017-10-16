﻿;; unsolvable domain with no capsule and 1 of 2 ghosts on food

(define (problem pacman)
    (:domain pacman)
    (:objects  node-x1-y1 node-x1-y2 node-x1-y3 node-x1-y4 node-x1-y5 node-x2-y1 node-x2-y3 node-x2-y5 node-x3-y1 node-x3-y3 node-x3-y5 node-x4-y1 node-x4-y3 node-x4-y4 node-x4-y5 node-x5-y1 node-x5-y3 node-x5-y5 node-x6-y1 node-x6-y3 node-x6-y4 node-x6-y5 node-x7-y1 node-x7-y3 node-x7-y5 node-x8-y1 node-x8-y3 node-x8-y5 node-x9-y1 node-x9-y3 node-x9-y5 node-x10-y3 node-x10-y5 node-x11-y3 node-x11-y5 node-x12-y1 node-x12-y3 node-x12-y5 node-x13-y1 node-x13-y3 node-x13-y4 node-x13-y5 node-x14-y1 node-x14-y3 node-x14-y5 node-x15-y1 node-x15-y3 node-x15-y4 node-x15-y5 node-x16-y1 node-x16-y3 node-x16-y5 node-x17-y1 node-x17-y3 node-x17-y5 node-x18-y1 node-x18-y2 node-x18-y3 node-x18-y4 node-x18-y5 - node)
(:init (at node-x8-y1)
(foodAt node-x13-y3)
(foodAt node-x13-y4)
(foodAt node-x13-y5)
(foodAt node-x14-y3)
(foodAt node-x15-y3)
(foodAt node-x15-y4)
(foodAt node-x16-y3)
(foodAt node-x17-y3)
(foodAt node-x18-y3)
(foodAt node-x18-y4)
(foodAt node-x18-y5)
(ghostAt node-x9-y5)
(ghostAt node-x18-y5)
(connected node-x1-y1 node-x1-y2)
(connected node-x1-y1 node-x2-y1)
(connected node-x1-y2 node-x1-y1)
(connected node-x1-y2 node-x1-y3)
(connected node-x1-y3 node-x1-y2)
(connected node-x1-y3 node-x1-y4)
(connected node-x1-y3 node-x2-y3)
(connected node-x1-y4 node-x1-y3)
(connected node-x1-y4 node-x1-y5)
(connected node-x1-y5 node-x1-y4)
(connected node-x1-y5 node-x2-y5)
(connected node-x2-y1 node-x1-y1)
(connected node-x2-y1 node-x3-y1)
(connected node-x2-y3 node-x1-y3)
(connected node-x2-y3 node-x3-y3)
(connected node-x2-y5 node-x1-y5)
(connected node-x2-y5 node-x3-y5)
(connected node-x3-y1 node-x2-y1)
(connected node-x3-y1 node-x4-y1)
(connected node-x3-y3 node-x2-y3)
(connected node-x3-y3 node-x4-y3)
(connected node-x3-y5 node-x2-y5)
(connected node-x3-y5 node-x4-y5)
(connected node-x4-y1 node-x3-y1)
(connected node-x4-y1 node-x5-y1)
(connected node-x4-y3 node-x3-y3)
(connected node-x4-y3 node-x4-y4)
(connected node-x4-y3 node-x5-y3)
(connected node-x4-y4 node-x4-y3)
(connected node-x4-y4 node-x4-y5)
(connected node-x4-y5 node-x3-y5)
(connected node-x4-y5 node-x4-y4)
(connected node-x4-y5 node-x5-y5)
(connected node-x5-y1 node-x4-y1)
(connected node-x5-y1 node-x6-y1)
(connected node-x5-y3 node-x4-y3)
(connected node-x5-y3 node-x6-y3)
(connected node-x5-y5 node-x4-y5)
(connected node-x5-y5 node-x6-y5)
(connected node-x6-y1 node-x5-y1)
(connected node-x6-y1 node-x7-y1)
(connected node-x6-y3 node-x5-y3)
(connected node-x6-y3 node-x6-y4)
(connected node-x6-y3 node-x7-y3)
(connected node-x6-y4 node-x6-y3)
(connected node-x6-y4 node-x6-y5)
(connected node-x6-y5 node-x5-y5)
(connected node-x6-y5 node-x6-y4)
(connected node-x6-y5 node-x7-y5)
(connected node-x7-y1 node-x6-y1)
(connected node-x7-y1 node-x8-y1)
(connected node-x7-y3 node-x6-y3)
(connected node-x7-y3 node-x8-y3)
(connected node-x7-y5 node-x6-y5)
(connected node-x7-y5 node-x8-y5)
(connected node-x8-y1 node-x7-y1)
(connected node-x8-y1 node-x9-y1)
(connected node-x8-y3 node-x7-y3)
(connected node-x8-y3 node-x9-y3)
(connected node-x8-y5 node-x7-y5)
(connected node-x8-y5 node-x9-y5)
(connected node-x9-y1 node-x8-y1)
(connected node-x9-y3 node-x8-y3)
(connected node-x9-y3 node-x10-y3)
(connected node-x9-y5 node-x8-y5)
(connected node-x9-y5 node-x10-y5)
(connected node-x10-y3 node-x9-y3)
(connected node-x10-y3 node-x11-y3)
(connected node-x10-y5 node-x9-y5)
(connected node-x10-y5 node-x11-y5)
(connected node-x11-y3 node-x10-y3)
(connected node-x11-y3 node-x12-y3)
(connected node-x11-y5 node-x10-y5)
(connected node-x11-y5 node-x12-y5)
(connected node-x12-y1 node-x13-y1)
(connected node-x12-y3 node-x11-y3)
(connected node-x12-y3 node-x13-y3)
(connected node-x12-y5 node-x11-y5)
(connected node-x12-y5 node-x13-y5)
(connected node-x13-y1 node-x12-y1)
(connected node-x13-y1 node-x14-y1)
(connected node-x13-y3 node-x12-y3)
(connected node-x13-y3 node-x13-y4)
(connected node-x13-y3 node-x14-y3)
(connected node-x13-y4 node-x13-y3)
(connected node-x13-y4 node-x13-y5)
(connected node-x13-y5 node-x12-y5)
(connected node-x13-y5 node-x13-y4)
(connected node-x13-y5 node-x14-y5)
(connected node-x14-y1 node-x13-y1)
(connected node-x14-y1 node-x15-y1)
(connected node-x14-y3 node-x13-y3)
(connected node-x14-y3 node-x15-y3)
(connected node-x14-y5 node-x13-y5)
(connected node-x14-y5 node-x15-y5)
(connected node-x15-y1 node-x14-y1)
(connected node-x15-y1 node-x16-y1)
(connected node-x15-y3 node-x14-y3)
(connected node-x15-y3 node-x15-y4)
(connected node-x15-y3 node-x16-y3)
(connected node-x15-y4 node-x15-y3)
(connected node-x15-y4 node-x15-y5)
(connected node-x15-y5 node-x14-y5)
(connected node-x15-y5 node-x15-y4)
(connected node-x15-y5 node-x16-y5)
(connected node-x16-y1 node-x15-y1)
(connected node-x16-y1 node-x17-y1)
(connected node-x16-y3 node-x15-y3)
(connected node-x16-y3 node-x17-y3)
(connected node-x16-y5 node-x15-y5)
(connected node-x16-y5 node-x17-y5)
(connected node-x17-y1 node-x16-y1)
(connected node-x17-y1 node-x18-y1)
(connected node-x17-y3 node-x16-y3)
(connected node-x17-y3 node-x18-y3)
(connected node-x17-y5 node-x16-y5)
(connected node-x17-y5 node-x18-y5)
(connected node-x18-y1 node-x17-y1)
(connected node-x18-y1 node-x18-y2)
(connected node-x18-y2 node-x18-y1)
(connected node-x18-y2 node-x18-y3)
(connected node-x18-y3 node-x17-y3)
(connected node-x18-y3 node-x18-y2)
(connected node-x18-y3 node-x18-y4)
(connected node-x18-y4 node-x18-y3)
(connected node-x18-y4 node-x18-y5)
(connected node-x18-y5 node-x17-y5)
(connected node-x18-y5 node-x18-y4))
(:goal (and (not (foodAt node-x13-y3))
(not (foodAt node-x13-y4))
(not (foodAt node-x13-y5))
(not (foodAt node-x14-y3))
(not (foodAt node-x15-y3))
(not (foodAt node-x15-y4))
(not (foodAt node-x16-y3))
(not (foodAt node-x17-y3))
(not (foodAt node-x18-y3))
(not (foodAt node-x18-y4))
(not (foodAt node-x18-y5))
(or (at node-x9-y1)
    (at node-x9-y3)
    (at node-x9-y5)))))