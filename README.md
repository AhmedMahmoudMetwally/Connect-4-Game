# Connect-4-game

#Game Description :
Connect 4 is a two-player game in which the players first choose a color and then take turns 
dropping their colored discs from the top into a grid. 
The pieces fall straight down, occupying the next available space within the column.
The objective of the game is to connect-four of one’s own discs of the same color next to each other vertically, horizontally, or diagonally. 
The two players keep playing until the board is full. The winner is the player having greater number of connected-fours.

#Algorithms You are required to support the following 2 algorithms as options for the AI agent: 

• Minimax without alpha-beta pruning 

• Minimax with alpha-beta pruning 




### Code Objectives
**Game Implementation: Creates a fully functional Connect Four game with graphical interface**

**AI Opponent: Implements an artificial intelligence player using advanced algorithms**

**User Experience: Provides an interactive setup menu for game customization**

**Educational Value: Demonstrates game AI concepts and minimax algorithm implementation**

 ### Key Outputs and Their Significance
**1. Interactive Game Board**
Visual representation of the Connect Four grid (6 rows × 7 columns)

Displays player pieces (red and yellow) and empty slots

Shows current player's piece during mouse movement

**Importance: Provides intuitive gameplay visualization matching physical Connect Four**

**2. AI Decision Information Panel**
Shows real-time AI thinking process including:

Algorithm type (Minimax/Alpha-Beta)

Search depth

Computation time

Move evaluations per column

Visual bar graph of move evaluations

**Importance: Helps understand AI decision-making and learn game strategy**

**3. Game Setup Interface**
Mode selection (Human vs Human, Human vs AI, AI vs AI)

Difficulty levels (Easy to Expert with depth 2-8)

Algorithm selection (Minimax vs Alpha-Beta Pruning)

Importance: Allows customization of gameplay experience and AI challenge level

**4. Game Outcome Display**
Clear victory announcement for winning player

Visual highlighting of winning combination

**Importance: Provides definitive game resolution and feedback**

Technical Components
Core Algorithms
Minimax Algorithm: Evaluates all possible moves to optimal depth

Alpha-Beta Pruning: Optimized minimax that skips irrelevant branches

Position Scoring: Heuristic evaluation of board states

**Game Features**
Valid move checking

Win condition detection (horizontal, vertical, diagonal)

Turn management

Visual effects and animations
