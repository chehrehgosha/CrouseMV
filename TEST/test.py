#sample of region inspector:


# if self.Module is "AngleMeasurement":
#     self.drawing = False  # True if mouse is pressed
#     self.mode = True  # if True, draw rectangle. Press 'm' to toggle to curve
#     self.ix, self.iy = -1, -1
#
#     # mouse callback function
#
#     self.img = cv2.imread(InspectionSource, 1)
#     self.img2 = self.img.copy()
#
#     # make cv2 windows, set mouse callback
#     cv2.namedWindow('image')
#     cv2.setMouseCallback('image', self.draw_circle)
#
#     self.inspectionDialog = QWidget()
#     self.inspectionLayout = QVBoxLayout()
#     self.inspectionDialog.setLayout(self.inspectionLayout)
#     self.HueLabel = QLabel()
#     self.inspectionLayout.addWidget(self.HueLabel)
#     self.HueLabel.setText('Press R for reset\n')
#     self.inspectionDialog.show()
#     while (1):
#         cv2.imshow('image', self.img2)
#
#         # This is where we get the keyboard input
#         # Then check if it's "m" (if so, toggle the drawing mode)
#         k = cv2.waitKey(1) & 0xFF
#         if k == ord('m'):
#             self.mode = not self.mode
#         elif k == ord('r'):
#             cv2.destroyWindow('image')
#             cv2.namedWindow('image', 0)
#             self.img = cv2.imread(InspectionSource)
#             self.img2 = self.img.copy()
#             cv2.setMouseCallback('image', self.draw_circle)
#             self.originArray = []
#             # self.rectRadio.setChecked(True)
#             # self.RectNow = True
#             # self.CircNow = False
#         elif k == 27:
#             cv2.destroyWindow('image')
#             break


# if self.Module is 'AngleMeasurement':
#     # global ix, iy, drawing, mode, overlay, output, alpha
#     overlay = self.img.copy()
#     output = self.img.copy()
#     alpha = 0.5
#
#     if event == cv2.EVENT_LBUTTONDOWN:
#         self.drawing = True
#         self.ix, self.iy = x, y
#
#     elif event == cv2.EVENT_MOUSEMOVE:
#         if self.drawing == True:
#             if self.mode == True:
#                 cv2.circle(overlay, (int((x + self.ix) / 2), int((y + self.iy) / 2)),
#                            int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2) / 2.8), (0, 0, 255), 4)
#                 cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
#                 cv2.imshow('image', self.img2)
#             else:
#                 cv2.rectangle(overlay, (self.ix, self.iy), (x, y), (0, 255, 0), 4)
#                 cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img2)
#                 cv2.imshow('image', self.img2)
#
#     elif event == cv2.EVENT_LBUTTONUP:
#         self.drawing = False
#         if self.mode == True:
#             cv2.circle(overlay, (int((x + self.ix) / 2), int((y + self.iy) / 2)),
#                        int(math.sqrt((self.ix - x) ** 2 + (self.iy - y) ** 2) / 2.8), (0, 0, 255), 4)
#             cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)
#
#         else:
#             cv2.rectangle(overlay, (self.ix, self.iy), (x, y), (0, 255, 0), 4)
#             cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, self.img)




