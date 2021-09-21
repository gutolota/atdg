import numpy
#import pandas
import matplotlib.pyplot as plt
import time
import math
from numpy.core.fromnumeric import reshape

class Trajectory:

    def __init__(self, name='t', xd=50, yd=50, smooth_m=10) -> None:
        self.smooth_m = smooth_m
        self.name = name
        self.m_time = 0.001
        self.size = 100000
        self.xd = xd
        self.yd = yd
        self.time = numpy.zeros((self.size), dtype=numpy.float64)
        self.draw_position = numpy.zeros((self.size, 2), dtype=numpy.float64)
        self.direction = numpy.zeros((self.size, 2), dtype=numpy.float64)
        self.last_index = 0

    def add_timestamp(self, x:int, y:int, t:numpy.float64) -> None:
        if(self.last_index >= self.size):
            self.size *= 1.5
            self.draw_position.reshape((self.size, 2))
            self.time.reshape((self.size))
            self.position.reshape((self.size, 2))
        self.draw_position[self.last_index][0] = x
        self.draw_position[self.last_index][1] = y
        self.time[self.last_index] = t*1e-3
        self.last_index += 1
 
    def notgauss1d(self, array, times):
        for t in range(times):
            for i in range(1, len(array)):
                soma = 0.0
                cont = 0
                for j in range(0, self.smooth_m):
                    if(i+j < len(array)):
                        cont += 1
                        soma += array[i+j]
                soma /= cont
                array[i] = soma

    def notgauss2d(self, array, times):
        for t in range(times):
            for i in range(0, len(array)):
                somax = 0.0
                somay = 0.0
                cont = 0
                for j in range(0, self.smooth_m):
                    if(i+j < len(array)):
                        cont += 1
                        somax += array[i+j][0]
                        somay += array[i+j][1]
                somax /= cont
                somay /= cont
                array[i][0] = somax
                array[i][1] = somay

    def smooth(self, smooth_times):
        self.position = numpy.zeros((self.last_index, 2), dtype=numpy.float64)
        self.velocity = numpy.zeros((self.last_index), dtype=numpy.float64)
        self.acceleration = numpy.zeros((self.last_index), dtype=numpy.float64)
        for i in range(0, self.last_index):
            self.position[i][0] = (((self.draw_position[i][0]+1)/2)*self.xd)
            self.position[i][1] = (((self.draw_position[i][1]+1)/2)*self.yd)
        self.notgauss2d(self.position, smooth_times)
        plt.plot(self.position[:, 0], self.position[:, 1])
        for i in range(1, self.last_index):
            self.direction[i] = self.getDirection(self.position[i], self.position[i])
            self.velocity[i] = self.instVelocity(self.time[i], self.time[i-1], self.position[i], self.position[i-1])
            self.acceleration[i] = self.instAccel(self.time[i], self.time[i-1], self.velocity[i], self.velocity[i-1])



    def instVelocity(self, tf, ti, si, sf):
        if(tf-ti != 0):
            vx = (sf[0]-si[0])/(tf-ti)
            vy = (sf[1]-si[1])/(tf-ti)
        else:
            vx = 0
            vy = 0
        return numpy.sqrt(vx**2 + vy**2)
    
    def instAccel(self, tf, ti, vf, vi):
        if(tf-ti != 0):
            return (vf-vi)/(tf-ti)
        else:
            return 0

    def getDirection(self, sf, si):
        vr = [sf[0]-si[0], sf[1]-si[1]]
        module = numpy.sqrt(vr[0]**2 + vr[1]**2)
        if(module != 0):
            vr[0] /= module
            vr[1] /= module
        else:
            vr = [0, 0]
        return vr

    def plotAcceleration(self):
        plt.close()
        plt.title(f'Acceleration of {self.name}')
        plt.xlabel('Instant of time')
        plt.ylabel('Simulated acceleration (m/s²)')
        plt.plot(self.time[0:self.last_index], self.acceleration[0:self.last_index])
        plt.show()

    def plotVelocity(self):
        plt.close()
        plt.title(f'Velocity of {self.name}')
        plt.xlabel('Instant of time')
        plt.ylabel('Simulated velocity (m/s)')
        plt.plot(self.time[0:self.last_index], self.velocity[0:self.last_index])
        plt.show()
    
    def plotPosition(self):
        plt.close()
        plt.title(f'Position of {self.name}')
        plt.xlabel('Instant of time')
        plt.ylabel('Simulated position (m)')
        plt.plot(self.position[:self.last_index, 0], self.position[:self.last_index, 1])
        plt.show()

    def getDrawCoords(self, i):
        return [(((self.position[i][0]/self.xd)*2)-1), (((self.position[i][1]/self.yd)*2)-1)]

    def save(self):
        file = open(f'{self.name}.dat', 'w')
        lines = '#Time,X,Y,DirectionX,DirectionY,Velocity,Acceleration\n'
        for i in range(0, self.last_index):
            lines += f'{self.time[i]},{self.position[i][0]},{self.position[i][1]},{self.direction[i][0]},{self.direction[i][1]},{self.velocity[i]},{self.acceleration[i]}\n'
        file.writelines(lines)


    def __sizeof__(self) -> int:
        return self.last_index
