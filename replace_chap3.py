import os

filepath = "/Users/aizzat/Library/CloudStorage/GoogleDrive-maizzat2@gmail.com/My Drive/00 WORK FOLDER/POSTGRADUATE (2022 onwards)/Maryam/2026 Thesis Writing/V2 Latex Thesis folder/Chap3/chap3.tex"

with open(filepath, 'r') as f:
    content = f.read()

# 1. Real Platform Image
t1 = r"""\subsection{Reference Physical Platform}

To ground the virtual workspace boundaries within realistic operational limits,"""
r1 = r"""\subsection{Reference Physical Platform}

\begin{figure}[htbp]
\centering
\includegraphics[width=0.95\linewidth]{figures/pixplatform.JPG}
\caption{Autonomous platform used as the target deployment system.}
\label{fig:real_platform}
\end{figure}

To ground the virtual workspace boundaries within realistic operational limits,"""
content = content.replace(t1, r1)

# 2. Planning Pipeline diagram
t2 = r"""\section{Algorithmic Pipeline and Implementation Procedures}

\subsection{Point Cloud Rasterization and 2.5D Grid Generation}"""
r2 = r"""\section{Algorithmic Pipeline and Implementation Procedures}

\begin{figure*}[htbp]
\centering
\resizebox{\textwidth}{!}{%
\begin{tikzpicture}[
    node distance=0.9cm and 0.6cm,
    box/.style={rectangle, draw, rounded corners=2pt, align=center, minimum height=0.9cm, minimum width=0.78\linewidth, text width=0.74\linewidth, inner sep=4pt, fill=gray!8},
    hbox/.style={rectangle, draw, rounded corners=2pt, align=center, minimum height=0.9cm, minimum width=0.38\linewidth, text width=0.34\linewidth, inner sep=4pt, fill=gray!8},
    arr/.style={-{Latex[length=1.7mm]}, thick},
    small/.style={font=\scriptsize}
]
    \node[draw, rounded corners=3pt, minimum width=0.82\linewidth, minimum height=2.7cm, fill=green!5] (scene) {};

    \begin{scope}[shift={(scene.center)}, x=0.82cm, y=0.82cm]
        \coordinate (terrainStart) at (-3.9,-0.55);
        \coordinate (terrainA) at (-2.7,-0.08);
        \coordinate (terrainB) at (-1.6,-0.62);
        \coordinate (terrainC) at (-0.35,0.32);
        \coordinate (terrainD) at (0.95,-0.25);
        \coordinate (terrainE) at (2.3,0.12);
        \coordinate (terrainF) at (3.8,-0.05);

        \fill[green!18] (terrainStart) -- (terrainA) -- (terrainB) -- (terrainC) -- (terrainD) -- (terrainE) -- (terrainF) -- (3.8,-1.15) -- (-3.9,-1.15) -- cycle;
        \draw[thick] (terrainStart) -- (terrainA) -- (terrainB) -- (terrainC) -- (terrainD) -- (terrainE) -- (terrainF);

        \fill[green!45!black] (-2.25,0.02) circle (0.14);
        \fill[green!45!black] (-2.25,0.24) circle (0.1);
        \fill[green!45!black] (-2.43,0.1) circle (0.1);
        \fill[green!45!black] (-2.07,0.1) circle (0.1);
        \fill[green!45!black] (2.45,0.04) circle (0.14);
        \fill[green!45!black] (2.45,0.26) circle (0.1);
        \fill[green!45!black] (2.27,0.12) circle (0.1);
        \fill[green!45!black] (2.63,0.12) circle (0.1);

        \draw[orange!80!black, line width=1.2pt] (-3.35,-0.18) .. controls (-2.2,0.55) and (-1.1,-0.85) .. (0.05,-0.02) .. controls (1.1,0.72) and (2.0,-0.18) .. (3.2,0.05);
        \draw[blue!70!black, dashed, line width=1pt] (-3.35,-0.32) .. controls (-2.3,0.02) and (-1.05,-0.28) .. (0.02,-0.12) .. controls (1.08,0.08) and (2.0,-0.02) .. (3.2,-0.02);

        \draw[fill=gray!25] (-0.75,-0.12) circle (0.14);
        \draw[fill=gray!25] (-0.25,0.06) circle (0.14);
        \draw[fill=gray!35, rounded corners=1pt] (-0.95,0.02) rectangle (-0.02,0.44);
        \draw[thick] (-0.7,0.44) -- (-0.7,0.7);
        \draw[thick] (-0.28,0.44) -- (-0.28,0.7);
        \draw[thick] (-0.86,0.28) -- (-1.08,0.42);
        \draw[thick] (-0.12,0.28) -- (0.1,0.42);
        \fill[black] (-0.74,0.24) circle (0.02);
        \fill[black] (-0.26,0.24) circle (0.02);

        \node[small, align=center] at (-0.48,1.02) {Ground robot on uneven terrain};
        \node[small, align=center] at (2.7,0.82) {Vegetation region};
        \node[small, text=orange!80!black] at (2.3,-0.68) {raw path};
        \node[small, text=blue!70!black] at (0.95,-0.92) {smoothed path};
    \end{scope}

    \node[box, below=of scene] (pcd) {Point-cloud map input in .pcd format (e.g., Autoware or ROS2 mapping output)};
    \node[hbox, below left=0.9cm and 0.2cm of pcd] (ros2) {Conventional ROS2 planning branch: 2D occupancy-grid map and planar A*};
    \node[hbox, below right=0.9cm and 0.2cm of pcd] (grid) {Proposed branch: rasterization into a 2.5D elevation grid with vegetation layer};
    \node[hbox, below=of ros2] (ros2out) {Resulting baseline: computationally efficient route with limited terrain awareness};
    \node[hbox, below=of grid] (astar) {A* search with slope-feasibility filtering and terrain-aware traversal cost};
    \node[hbox, below=of astar] (smooth) {B-spline refinement followed by sampled boundary, vegetation, and slope validation};
    \node[hbox, below=of smooth] (metrics) {Evaluation of path length, energy proxy, travel-time proxy, runtime, and turn-angle reduction};

    \coordinate (split) at ([yshift=-0.35cm]pcd.south);
    \draw[arr] (scene.south) -- (pcd.north);
    \draw[arr] (pcd.south) -- (split);
    \fill (split) circle (1.1pt);
    \draw[arr] (split) -| node[pos=0.58, above, fill=white, inner sep=1pt] {\scriptsize 2D method} (ros2.north);
    \draw[arr] (split) -| node[pos=0.58, above, fill=white, inner sep=1pt] {\scriptsize 2.5D method} (grid.north);
    \draw[arr] (ros2.south) -- (ros2out.north);
    \draw[arr] (grid.south) -- (astar.north);
    \draw[arr] (astar.south) -- (smooth.north);
    \draw[arr] (smooth.south) -- (metrics.north);
\end{tikzpicture}
}
\caption{Planning overview with a terrain-scene diagram, followed by point-cloud map input in .pcd format (as commonly produced in Autoware/ROS2), and a split comparison between conventional 2D planning and the proposed 2.5D terrain-aware branch.}
\label{fig:planning_pipeline}
\end{figure*}

\subsection{Point Cloud Rasterization and 2.5D Grid Generation}"""
content = content.replace(t2, r2)

# 3. Image
t3 = r"""\subsection{Formulation of Terrain-Aware Step Traversal Cost (STC)}"""
r3 = r"""\begin{figure}[htbp]
\centering
\includegraphics[width=\linewidth]{figures/map3_high_seed42_pcd_vs_25d.png}
\caption{Example preprocessing result. Left: point-cloud visualization of the terrain source. Right: the corresponding 2.5D raster representation used by the planner, including the vegetation penalty region.}
\label{fig:pcd_example_compare}
\end{figure}

\subsection{Formulation of Terrain-Aware Step Traversal Cost (STC)}"""
content = content.replace(t3, r3)

# 4. Nomenclature Table
t4 = r"""\begin{equation}
    STC(P, C) = d_{3D}(P, C) + \lambda \cdot \theta(P, C) + V_{penalty}(C)
\end{equation}"""
r4 = r"""\begin{table}[htbp]
\caption{Nomenclature}
\label{tab:nomenclature}
\centering
\footnotesize
\begin{tabular}{p{0.16\columnwidth} p{0.72\columnwidth}}
\toprule
\textbf{Term} & \textbf{Definition} \\
\midrule
MCS & Maximum climbable slope constraint used to reject infeasible transitions. \\
SCW ($\lambda$) & Slope cost weight controlling the sensitivity of traversal cost to local gradient. \\
VTP ($P_{\mathrm{veg}}$) & Vegetation traversal penalty applied to cells inside the vegetation mask. \\
SM$_{i,j}$ ($\theta$) & Local slope magnitude between neighboring nodes $i$ and $j$. \\
3DSD$_{i,j}$ ($d_{3D}$) & Three-dimensional step distance between nodes $i$ and $j$. \\
STC$_{i,j}$ & Step traversal cost used in the accumulated A* cost. \\
$L_{\mathrm{3D}}$ & Total three-dimensional path length. \\
ECP & Energy consumption proxy. \\
TTP & Travel-time proxy. \\
$I^{\mathrm{veg}}_{i,j}$ & Vegetation indicator for the transition from node $i$ to node $j$. \\
$I^{\uparrow}_{k,k+1}$ & Uphill-motion indicator for path segment $k$ to $k+1$. \\
\bottomrule
\end{tabular}
\end{table}

\begin{equation}
    STC(P, C) = d_{3D}(P, C) + \lambda \cdot \theta(P, C) + V_{penalty}(C)
\end{equation}"""
content = content.replace(t4, r4)

# 5. Experimental setup
t5 = r"""\subsection{Performance Characterization Suite}"""
r5 = r"""\begin{table}[htbp]
\caption{Experimental configuration}
\label{tab:experiment_setup}
\centering
\footnotesize
\begin{tabular}{p{0.30\columnwidth} p{0.58\columnwidth}}
\toprule
\textbf{Parameter} & \textbf{Setting} \\
\midrule
Terrain profiles & Three synthetic deterministic 2.5D maps (flat, medium, high relief), seed $=42$ \\
Grid size & $500\times 500$ \\
Representative start-goal pair & $(5,5)\rightarrow(90,90)$ \\
Additional validation pairs & $(10,80)\rightarrow(85,20)$; $(15,15)\rightarrow(80,70)$ \\
MCS & $20^\circ$ \\
VTP & 3.5 \\
SCW sweep & $\{0.0, 0.25, 0.5, 0.75, 1.0\}$ \\
Connectivity & 8-neighborhood grid search \\
Reported runtimes & Planning time and B-spline smoothing plus validation time \\
\bottomrule
\end{tabular}
\end{table}

\subsection{Performance Characterization Suite}"""
content = content.replace(t5, r5)

with open(filepath, 'w') as f:
    f.write(content)

print("Replacement complete.")
