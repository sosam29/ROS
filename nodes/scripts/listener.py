import rospy
from std_msgs.msg import String


def callback(message):
    rospy.loginfo(rospy.get_caller_id() + " Received message %s", message.data)

class listner():
    rospy.init_node("listner", anonymous=True)
    rospy.Subscriber("chatter", String, callback)

    rospy.spin()




if __name__ == "__main__":
    listner()