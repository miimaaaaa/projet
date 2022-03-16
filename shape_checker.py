# import the necessary packages
import argparse
import cv2


def detect(contour):
	# On initialise la forme inconnue pour l'instant
	shape = "*"
	# On calcule d'abord le contour de la forme avant d'appliquer
	# l'algorithme d'approximation de contour
	# La forme est divisée en "vertices"
	peri = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
	# 3 Vertices, c'est probablement un triangle
	if len(approx) == 3:
		shape = "triangle"
	# 4 Vertices, c'est probablement un carré/rectangle
	elif len(approx) == 4:
		# On calcule l'aspect/ratio de la forme
		# si c'est proche de 1, c'est un carré, sinon un rectangle
		(x, y, w, h) = cv2.boundingRect(approx)
		ar = w / float(h)
		shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
	# 5 vertices, on part sur un pentagone
	elif len(approx) == 5:
		shape = "pentagon"
	# Si on a plus de 5 vertices ou moins de 3 on part du principe que c'est un cercle
	else:
		shape = "circle"
	return shape
