from math import cos, sin, pi
import numpy as np
import os, time

# screen_width, screen_height = os.get_terminal_size()
screen_width, screen_height = 50, 25

theta_spacing: float = 0.07
phi_spacing: float = 0.02

R1, R2, K2 = 1, 2, 5

# Calculate K1 based on screen size: the maximum x-distance occurs
# roughly at the edge of the torus, which is at x=R1+R2, z=0.  we
# want that to be displaced 3/8ths of the width of the screen, which
# is 3/4th of the way from the center to the side of the screen.
# screen_width*3/8 = K1*(R1+R2)/(K2+0)
# screen_width*K2*3/(8*(R1+R2)) = K1
K1: float = screen_width * K2 * 3 / (8 * (R1 + R2))

def render_frame(A: float, B: float) -> None:
    # precompute sines and cosines of A and B
    cosA: float = cos(A)
    sinA: float = sin(A)
    cosB: float = cos(B)
    sinB: float = sin(B)

    output:  list = [[' ' for _ in range(screen_width)] for _ in range(screen_height)]
    zbuffer: list = [[0.0 for _ in range(screen_width)] for _ in range(screen_height)]

    # theta goes around the cross-sectional circle of a torus
    for theta in np.arange(0, 2*pi, theta_spacing):

        # precompute sines and cosines of theta
        costheta: float = cos(theta)
        sintheta: float = sin(theta)

        # phi goes around the center of revolution of a torus
        for phi in np.arange(0, 2*pi, phi_spacing):

            # precompute sines and cosines of phi
            cosphi: float = cos(phi)
            sinphi: float = sin(phi)

            # the x,y coordinate of the circle, before revolving (factored
            # out of the above equations)
            circlex: float = R2 + R1 * costheta
            circley: float = R1 * sintheta

            # final 3D (x,y,z) coordinate after rotations, directly from
            # our math above
            x: float = circlex * (cosB * cosphi + sinA * sinB * sinphi) - circley * cosA * sinB
            y: float = circlex * (sinB * cosphi - sinA * cosB * sinphi) + circley * cosA * cosB
            z: float = K2 + cosA * circlex * sinphi + circley * sinA

            ooz: float = 1/z # 'one over' z

            # x and y projection. note that y is negated here, because y
            # goes up in 3D space but down on 2D displays.
            xprojection: int = int(screen_width / 2 + K1 * ooz * x)
            yprojection: int = int(screen_height / 2 - K1 * ooz * y)

            # calculate luminance.  ugly, but correct.
            luminance: float = cosphi * costheta * sinB - cosA * costheta * sinphi - \
                sinA * sintheta + cosB * (cosA * sintheta - costheta * sinA * sinphi)

            # L ranges from -sqrt(2) to +sqrt(2). If it's < 0, the surface
            # is pointing away from us, so we won't bother trying to plot it.
            if not (luminance > 0):
                continue

            if not (0 <= xprojection < screen_width and 0 <= yprojection < screen_height):
                continue

            # test against the z-buffer. larger 1/z means the pixel is
            # closer to the viewer than what's already plotted.
            if not (ooz > zbuffer[yprojection][xprojection]):
                continue

            zbuffer[yprojection][xprojection] = ooz
            luminance_index: int = int(luminance * 8)

            # luminance_index is now in the range 0..11 (8*sqrt(2) = 11.3)
            # now we lookup the character corresponding to the
            # luminance and plot it in our output:
            output[yprojection][xprojection] = '.,-~:;=!*#$@'[luminance_index]

    # now, dump output[] to the screen.
    # bring cursor to "home" location, in just about any currently-used
    # terminal emulation mode
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\n'.join(''.join(row) for row in output))

A, B = 0, 0
while True:
    render_frame(A, B)
    A += 0.04
    B += 0.08

    time.sleep(0.03)