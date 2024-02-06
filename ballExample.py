import cv2
import time
import mediapipe as mp
import numpy as np
import pygame

pygame.init()

# Set up the window dimensions
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Draw Circle in Pygame")

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands()

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open webcam")
    exit()

window_name = 'Video Capture'
cv2.namedWindow(window_name)

GRIPPING_THRESH = .07
position = np.array([0., 0.])


class Ball:
    def __init__(self, r=25, gravity=3., screen_dims=(window_width, window_height), bounciness=.9):

        self.r = r
        self.gravity = gravity
        self.bounciness = bounciness
        self.screen_dims = screen_dims

        self.pos = np.array([screen_dims[0]*.5, screen_dims[1]*.5])
        self.vel = np.array([0., 0.])
        self.acc = np.array([0., gravity])

        self.friction = .1
        self.holding_pos_initial = np.array([])
        self.prev_pos = np.array([])

    def update(self, holding_pos=np.array([])):
        if len(holding_pos) != 0:
            if len(self.holding_pos_initial) == 0:
                self.holding_pos_initial = holding_pos
            if len(self.prev_pos) == 0:
                self.prev_pos = self.pos

            self.vel = np.array([0., 0.])
            self.pos = self.prev_pos + (holding_pos-self.holding_pos_initial)

        else:
            self.prev_holding_pos = np.array([])
            self.prev_pos = np.array([])
            tmp = self.vel + self.acc
            self.vel = tmp - tmp*self.friction

            self.pos += self.vel

            if self.pos[0]+self.r >= self.screen_dims[0]:
                self.pos[0] = self.screen_dims[0]-self.r
                self.vel[0] *= -self.bounciness

            if self.pos[0]-self.r < 0:
                self.pos[0] = self.r
                self.vel[0] *= -self.bounciness

            if self.pos[1]+self.r >= self.screen_dims[1]:
                self.pos[1] = self.screen_dims[1]-self.r
                self.vel[1] *= -self.bounciness

            if self.pos[1]-self.r < 0:
                self.pos[1] = self.r
                self.vel[1] *= -self.bounciness

    def draw(self):
        pygame.draw.circle(window, (255, 0, 0), self.pos, self.r)

ball = Ball()

running = True
while running:
    window.fill((0, 0, 0))
    time.sleep(.01)

    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(frame)

    gripping = False

    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(
                frame, hand_landmarks, connections=mp_hands.HAND_CONNECTIONS)

            index_tip = np.array([hand_landmarks.landmark[8].x,
                                  hand_landmarks.landmark[8].y,
                                  hand_landmarks.landmark[8].z])

            thumb_tip = np.array([hand_landmarks.landmark[4].x,
                                  hand_landmarks.landmark[4].y,
                                  hand_landmarks.landmark[4].z])

            gripping = np.linalg.norm(index_tip - thumb_tip) <= GRIPPING_THRESH
            position = np.array([hand_landmarks.landmark[8].x,
                                 hand_landmarks.landmark[8].y])

    print("Gripping state: ", gripping)
    print("Position: ", position)

    if gripping: ball.update(np.array([window_width-position[0]*500, position[1]*500]))
    else: ball.update()
    ball.draw()

    cv2.imshow(window_name, frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

hands.close()
cap.release()
cv2.destroyAllWindows()
