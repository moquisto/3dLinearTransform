import pygame as pg
from matrices import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position, 1.0])
        self.forward = np.array([0,0,1,1])
        self.right = np.array([1,0,0,1])
        self.up = np.array([0,1,0,1])
        self.h_fov = math.pi / 2 #original was 3
        self.v_fov = self.h_fov * (render.HEIGHT / render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.movement_speed = 0.1
        self.rotation_speed = 0.05
    
    def controls(self):
        key = pg.key.get_pressed()
        if key[pg.K_a]:
            self.position -= self.right * self.movement_speed
        if key[pg.K_d]:
            self.position += self.right * self.movement_speed
        if key[pg.K_w]:
            self.position += self.forward * self.movement_speed
        if key[pg.K_s]:
            self.position -= self.forward * self.movement_speed
        if key[pg.K_SPACE]:
            self.position += self.up * self.movement_speed
        if key[pg.K_LCTRL]:
            self.position -= self.up * self.movement_speed
        if key[pg.K_LEFT]:
            self.camera_yaw(-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_yaw(self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_pitch(-self.rotation_speed)
        if key[pg.K_DOWN]:
            self.camera_pitch(self.rotation_speed)
    
    def camera_yaw(self, angle):
        rotate = rotate_y(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate
    
    def camera_pitch(self, angle):
        rotate = rotate_x(angle)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate
    
    def translation_matrix(self):
        x, y, z, w = self.position
        return np.array([
            [1,0,0,0],
            [0,1,0,1],
            [0,0,1,0],
            [-x,-y,-z,1]
        ]) #This is also odd. I don't fully understand this yet. w isn't used for any of these. Why do we take the negative? Why is there a one on the second row last column?
    
    def rotation_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0], 
            [0, 0, 0, 1]
        ])
    
    def camera_matrix(self):
        return self.translation_matrix() @ self.rotation_matrix() #This is matrix multiplication. First we apply the rotation, then translation.