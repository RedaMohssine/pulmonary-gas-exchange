import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.sparse import lil_matrix, csc_matrix
from scipy.sparse.linalg import spsolve

# Constantes et paramètres du modèle
M = 100
N = 100
R = M * N
L = 0.049
l = 0.0067
P1 = 10 + 3.8e-4
P2 = 10
Dx = L / (M - 1)  # Pas de discrétisation en x
Dy = l / (N - 1)  # Pas de discrétisation en y
e = 0.0000185
debit = []

# Définition des points de bordure et des ensembles en 2D
I = {(1, 1), (1, N), (M, 1), (M, N)}  # Quatre coins
A = {(i, N) for i in range(2, M)}  # Bord supérieur excluant les coins
B = {(i, 1) for i in range(2, M)}  # Bord inférieur excluant les coins
C = {(1, j) for j in range(2, N)}  # Bord gauche excluant les coins
D = {(M, j) for j in range(2, N)}  # Bord droit excluant les coins
E = {(i, j) for i in range(2, M) for j in range(2, N)}  # Points intérieurs

# Fonction de conversion des indices 2D en 1D
def bij(i, j):
    return (j - 1) + N * (i - 1)

# Création de la matrice Z et du vecteur Y pour le système linéaire
Z = lil_matrix((3 * M * N, 3 * M * N))
Y = np.zeros(3 * M * N)

# Remplissage de la matrice Z pour les points intérieurs
for (i, j) in E:
    idx = bij(i, j)
    # Première équation : équation de continuité ou de flux en x
    Z[idx, bij(i, j) + 2 * R] = -(1) / (Dx)
    Z[idx, bij(i - 1, j) + 2 * R] = (1) / (Dx)
    Z[idx, bij(i + 1, j)] = e / (Dx ** 2)
    Z[idx, bij(i - 1, j)] = e / (Dx ** 2)
    Z[idx, bij(i, j + 1)] = e / (Dy ** 2)
    Z[idx, bij(i, j - 1)] = e / (Dy ** 2)
    Z[idx, idx] = -2 * e * ((1 / (Dx ** 2) + 1 / (Dy ** 2)))
    
    # Deuxième équation : équation de continuité ou de flux en y
    Z[idx + R, bij(i, j + 1) + 2 * R] = -(1) / (Dy * 2)
    Z[idx + R, bij(i, j - 1) + 2 * R] = (1) / (Dy * 2)
    Z[idx + R, bij(i + 1, j) + R] = e / (Dx ** 2)
    Z[idx + R, bij(i - 1, j) + R] = e / (Dx ** 2)
    Z[idx + R, bij(i, j + 1) + R] = e / (Dy ** 2)
    Z[idx + R, bij(i, j - 1) + R] = e / (Dy ** 2)
    Z[idx + R, idx + R] = -2 * e * ((1 / (Dx ** 2) + 1 / (Dy ** 2)))
    
    # Troisième équation : relation entre les vitesses Ux et Uy
    Z[idx + 2 * R, bij(i + 1, j)] = 1 / (Dx * 2)
    Z[idx + 2 * R, bij(i - 1, j)] = -1 / (Dx * 2)
    Z[idx + 2 * R, bij(i, j + 1) + R] = 1 / (Dy * 2)
    Z[idx + 2 * R, bij(i, j - 1) + R] = -1 / (Dy * 2)

# Application des conditions aux limites pour les coins
for (i, j) in I:
    idx = bij(i, j)
    Z[idx, idx] = 1
    Z[idx + R, idx + R] = 1
    Z[idx + 2 * R, idx + 2 * R] = 1

# Application des conditions aux limites pour le bord supérieur
for (i, j) in A:
    idx = bij(i, j)
    Z[idx, idx] = 1
    Z[idx + R, idx + R] = 1
    Z[idx + 2 * R, bij(i + 1, j)] = 1 / (Dx * 2)
    Z[idx + 2 * R, bij(i - 1, j)] = -1 / (Dx * 2)
    Z[idx + 2 * R, idx + R] = 1 / (Dy)
    Z[idx + 2 * R, bij(i, j - 1) + R] = -1 / (Dy)

# Application des conditions aux limites pour le bord inférieur
for (i, j) in B:
    idx = bij(i, j)
    Z[idx, idx] = 1
    Z[idx + R, idx + R] = 1
    Z[idx + 2 * R, bij(i + 1, j)] = 1 / (Dx * 2)
    Z[idx + 2 * R, bij(i - 1, j)] = -1 / (Dx * 2)
    Z[idx + 2 * R, bij(i, j + 1) + R] = 1 / (Dy)
    Z[idx + 2 * R, idx + R] = -1 / (Dy)

# Application des conditions aux limites pour le bord gauche
for i, j in C:
    idx = bij(i, j)
    Z[idx, bij(i + 1, j) + 2 * R] = -1 / Dx
    Z[idx, bij(i, j) + 2 * R] = 1 / Dx
    Z[idx, bij(i + 1, j)] = e / (Dx ** 2)
    Z[idx, bij(M - 1, j)] = e / (Dx ** 2)
    Z[idx, bij(i, j + 1)] = e / (Dy ** 2)
    Z[idx, bij(i, j - 1)] = e / (Dy ** 2)
    Z[idx, idx] = -e * ((2 / (Dx ** 2) + 2 / (Dy ** 2)))
    Z[idx + R, idx + R] = 1
    Z[idx + 2 * R, idx + 2 * R] = 1
    Y[idx + 2 * R] = P1  # Condition de pression au bord gauche

# Application des conditions aux limites pour le bord droit
for i, j in D:
    idx = bij(i, j)
    Z[idx, bij(i, j) + 2 * R] = -1 / Dx
    Z[idx, bij(i - 1, j) + 2 * R] = 1 / Dx
    Z[idx, bij(2, j)] = e / (Dx ** 2)
    Z[idx, bij(i - 1, j)] = e / (Dx ** 2)
    Z[idx, bij(i, j + 1)] = e / (Dy ** 2)
    Z[idx, bij(i, j - 1)] = e / (Dy ** 2)
    Z[idx, idx] = -e * ((2 / (Dx ** 2) + 2 / (Dy ** 2)))
    Z[idx + R, idx + R] = 1
    Z[idx + 2 * R, idx + 2 * R] = 1
    Y[idx + 2 * R] = P2  # Condition de pression au bord droit

# Conditions de pression aux coins
Y[bij(1, 1) + 2 * R] = P1
Y[bij(1, N) + 2 * R] = P1
Y[bij(M, N) + 2 * R] = P2
Y[bij(M, 1) + 2 * R] = P2

# Conversion de la matrice Z en format CSC pour optimiser la résolution
Z = csc_matrix(Z)

# Résolution du système linéaire Z * X = Y
X = spsolve(Z, Y)

# Extraction des composantes de vitesse Ux, Uy et de la pression P à partir de la solution X
Ux = X[:M * N].reshape((M, N))
Uy = X[M * N:2 * M * N].reshape((M, N))
P = X[2 * M * N:].reshape((M, N))

# Création d'une copie de la pression pour un lissage éventuel
P_smoothed = P.copy()

# Création des figures pour l'affichage des résultats
fig, ax = plt.subplots(1, 3, figsize=(18, 6))

# Affichage de la variation de Ux
img1 = ax[0].imshow(Ux, cmap='viridis', aspect='auto')
fig.colorbar(img1, ax=ax[0])
ax[0].set_title('Variation de Ux')
ax[0].set_xlabel('Index Y')
ax[0].set_ylabel('Index X')

# Affichage de la variation de Uy
img2 = ax[1].imshow(Uy, cmap='viridis', aspect='auto')
fig.colorbar(img2, ax=ax[1])
ax[1].set_title('Variation de Uy')
ax[1].set_xlabel('Index Y')
ax[1].set_ylabel('Index X')

# Affichage de la pression P
img3 = ax[2].imshow(P_smoothed, cmap='viridis', aspect='auto')
fig.colorbar(img3, ax=ax[2])
ax[2].set_title('Pression P')
ax[2].set_xlabel('Index Y')
ax[2].set_ylabel('Index X')

# Création de la grille pour les valeurs X et Y
X_grid, Y_grid = np.meshgrid(np.arange(N), np.arange(M))

# Création des figures pour l'affichage en 3D
fig = plt.figure(figsize=(18, 6))

# Affichage 3D de la variation de Ux
ax1 = fig.add_subplot(131, projection='3d')
ax1.plot_surface(X_grid, Y_grid, Ux, cmap='viridis')
ax1.set_title('Variation de Ux (3D)')
ax1.set_xlabel('Index Y')
ax1.set_ylabel('Index X')
ax1.set_zlabel('Ux')

# Affichage 3D de la variation de Uy
ax2 = fig.add_subplot(132, projection='3d')
ax2.plot_surface(X_grid, Y_grid, Uy, cmap='viridis')
ax2.set_title('Variation de Uy (3D)')
ax2.set_xlabel('Index Y')
ax2.set_ylabel('Index X')
ax2.set_zlabel('Uy')

# Affichage 3D de la pression P
ax3 = fig.add_subplot(133, projection='3d')
ax3.plot_surface(X_grid, Y_grid, P, cmap='viridis')
ax3.set_title('Pression P (3D)')
ax3.set_xlabel('Index Y')
ax3.set_ylabel('Index X')
ax3.set_zlabel('Pression P')

# Création de la grille pour les valeurs X et Y (répétée pour clarté)
X_grid, Y_grid = np.meshgrid(np.arange(N), np.arange(M))

# Tracé de la variation de la pression en arrière-plan à l'aide de contours
fig, ax = plt.subplots(figsize=(8, 6))
contour = ax.contourf(Y_grid, X_grid, P, cmap='viridis', alpha=0.7)  # Variation de la pression en arrière-plan
fig.colorbar(contour, ax=ax, label='Pression P')

# Définition du pas de sous-échantillonnage pour le quiver plot
sampling_step = 3  # Ajustez cette valeur pour contrôler la densité des flèches

# Sous-échantillonnage des données de vitesse
Ux_subsampled = Ux[::sampling_step, ::sampling_step]
Uy_subsampled = Uy[::sampling_step, ::sampling_step]

# Sous-échantillonnage de la grille
X_grid_subsampled = X_grid[::sampling_step, ::sampling_step]
Y_grid_subsampled = Y_grid[::sampling_step, ::sampling_step]

# Tracé du contour de la pression avec les vecteurs de vitesse sous-échantillonnés
contour = ax.contourf(Y_grid, X_grid, P, cmap='viridis', alpha=0.7)
fig.colorbar(contour, ax=ax, label='Pression P')

# Tracé du quiver plot montrant les vecteurs de vitesse (Ux, Uy)
ax.quiver(Y_grid_subsampled, X_grid_subsampled, Ux_subsampled, Uy_subsampled, scale_units='xy', angles='xy', color='blue')
ax.set_title('Quiver plot: Vecteurs de vitesse (Ux, Uy) sous-échantillonnés')
ax.set_xlabel('Index Y')
ax.set_ylabel('Index X')

# Affichage de toutes les figures créées
plt.show()
