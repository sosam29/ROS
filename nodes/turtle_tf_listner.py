#!/usr/bin/env python
import rospy
import roslib
roslib.load_manifest('learning_tf')

import tf
import geometry_msgs.msg
import math
import turtlesim.srv

if __name__ == "__main__":
    rospy.init_node("turtle_tf_listner")
    listner = tf.TransformListener()

    rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4,2,0,'turtle2')

    turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist, queue_size=1)
    rate = rospy.Rate(10.0)
    listner.waitForTransform('/turtle2','/carrot1', rospy.Time(), rospy.Duration(4.0))

    while not rospy.is_shutdown():
        try:
            # (trans, rot)=listner.lookupTransform('/turtle2','/carrot1', rospy.Time(0))
            now = rospy.Time.now()
            past = now - rospy.Duration(5.0)
            listner.waitForTransformFull("/turtle2", now, "/turtle1", past, '/world',rospy.Duration(1.0))
            (trans, rot) = listner.lookupTransformFull('/turtle2',now, '/turtle1', past,  '/world')
        except (tf.LookupException,tf.ConnectivityException, tf.Exception):
            continue
        angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0]**2 + trans[1]**2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular
        turtle_vel.publish(cmd)
        rate.sleep()

