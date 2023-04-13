#! /usr/bin/env python

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

from time import perf_counter
import serial,time

class teleop(Node):# e
    """Crea objetos de tipo nodo."""
    
    def __init__(self):
        """Constructor de la clase teleop."""

        super().__init__("robot_hearer")

        #Creamos el publisher al tópico '/turtlebot_cmdVel':
        self.subscriptionTwist = self.create_subscription(Twist,'/turtlebot_cmdVel',self.receive_parameters,10)
        self.get_logger().info("Robot Hearer has been started correctly.")

        # Conexión con Arduino
        self.arduino = serial.Serial("/dev/tyACM0",9600,timeout=1)
        self.arduino.reset_input_buffer()
        time.sleep(0.1)
        if self.arduino.isOpen():
            print("{} conneced!".format(self.arduino.port))

    def receive_parameters(self,msg):
        """Pide los parámetros de velocidad lineal y angular al usuario y los publica en el tópico '/turtlebot_route'"""
        
        self.linear_vel = msg.linear.x
        self.angular_vel = msg.angular.z

        if self.arduino.isOpen():
            try:
                while True:
                    if self.arduino.inWaiting()>0:
                        print("-----------")
                        self.arduino.write(b"{}".format(self.linear_vel))
                        print("Imprimo: {}".format(self.linear_vel))
                        answer = self.arduino.readline().decode('utf-8').rstrip()
                        print(answer)
                        self.arduino.flushInput()
            except KeyboardInterrupt:
                print("KeyboardInterrupt has been caugh.")
        


def main(args=None):
    rclpy.init(args=args)
    teleop_node = teleop()
    
    teleop_node.receive_parameters()
    teleop_node.listen_keyboard()
    
    rclpy.spin(teleop_node)
    
    teleop.destroy_node()
    rclpy.shutdown()
    
if __name__== "__main__":
    main()